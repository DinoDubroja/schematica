from support import APP
import json
import base64
import sqlite3
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review_client import Client, digest, recovery_sql, write_json
from review_desktop import Connector


class ReviewImageTests(unittest.TestCase):
    def test_extended_target_source_export_retains_earlier_image_evidence(self):
        image={'hash':'a'*64,'mime':'image/png','bytes':10,'name':'reference.png'}
        revision={'id':'r2','source':{'definition':{},'recipe':'exact source'},'symbol':{'configurations':[]},'fingerprint':'f'}
        saved={'id':'comment','targets':[{'symbol':'pnp','revision':'r2'}],'attachments':[image]}
        events=[{'id':'event','action':'comment-extend','body':{'saved':saved,'input':{'comment':'comment','targets':saved['targets']}}}]
        client=Client({'url':'https://example.test','token':'test'})
        with tempfile.TemporaryDirectory() as directory, patch.object(client,'revision',return_value=revision),patch.object(client,'state',return_value={'comments':{}}),patch.object(client,'request',side_effect=[{'events':events,'next':1},{'events':[]}]),patch.object(client,'comment_images') as images:
            client.source_export('r2',Path(directory)/'source')
            self.assertTrue(any(c.get('attachments')==[image] for c in images.call_args.args[0]))
            self.assertEqual((Path(directory)/'source/recipe.tex').read_text(),'exact source')

    def test_private_image_backup_restores_exact_large_bytes(self):
        raw=bytes(range(256))*3072
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest={'consistent':True,'collections':{}}
            tables={name:[] for name in ['state','events','revisions','assets','requests','publication']}
            tables['images']=[{'hash':digest(raw),'mime':'image/png','bytes':len(raw),'width':10,'height':10,'body':base64.b64encode(raw).decode()}]
            for name,rows in tables.items():
                file=root/(name+'.json');write_json(file,rows);manifest['collections'][name]={'rows':len(rows),'sha256':digest(file.read_bytes())}
            write_json(root/'manifest.json',manifest);recovery_sql(root,root/'recovery.sql')
            db=sqlite3.connect(':memory:');db.executescript((root/'recovery.sql').read_text())
            restored=db.execute('SELECT hash,body FROM images').fetchone();db.close()
            self.assertEqual(base64.b64decode(restored[1]),raw);self.assertEqual(restored[0],digest(raw))

    def test_agent_receives_exact_private_image_bytes_and_target_manifest(self):
        raw=b'fixture image bytes'
        image={'hash':digest(raw),'mime':'image/png','bytes':len(raw),'name':'reference.png'}
        comments=[{'id':'comment','targets':[{'symbol':'fixture','revision':'r1'}],'attachments':[image]}]
        client=Client({'url':'https://example.test','token':'test'})
        with tempfile.TemporaryDirectory() as directory, patch.object(client,'request',return_value=raw) as request:
            paths=client.comment_images(comments,directory)
            self.assertEqual(paths[0].read_bytes(),raw)
            request.assert_called_once_with('/review/images/'+image['hash'])
            self.assertEqual(json.loads((Path(directory)/'manifest.json').read_text())[0]['targets'],comments[0]['targets'])
        with tempfile.TemporaryDirectory() as directory, patch.object(client,'request',return_value=b'wrong'):
            with self.assertRaisesRegex(ValueError,'checksum'): client.comment_images(comments,directory)

    def test_direct_connector_inspects_attached_file_and_returns_question_without_correction(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'config.json'
            config.write_text(json.dumps({'url':'https://example.test','token':'test','work':str(root/'private')}))
            connector=Connector(config)
            target={'symbol':'fixture','revision':'r1','signature':'a'*64,'comments':[]}
            job={'id':'j:1','workflow':2,'lease':'lease','publications':[],'corrections':[target],'results':[],'answers':[{'question':{'text':'Which bar?'},'comment':'answer'}]}
            revision={'id':'r1','symbol':{'id':'fixture'},'source':{'definition':{},'recipe':'source'}}
            def images(comments,output):
                output.mkdir(parents=True);image=output/'private.png';image.write_bytes(b'actual image content');(output/'manifest.json').write_text('[]');return [image]
            def interpret(config,work,prompt,schema,paths):
                self.assertEqual(paths[0].read_bytes(),b'actual image content')
                self.assertIn('"clarifications": [{"question": {"text": "Which bar?"}',prompt)
                return {'intent':'','question':'Which bar?','image_observations':['Three bars are visible']}
            with patch.object(connector,'heartbeat'),patch.object(connector.client,'revision',return_value=revision),patch.object(connector.client,'comment_images',side_effect=images),patch('review_desktop.run_codex',side_effect=interpret),patch.object(connector,'job_action') as action,patch('review_desktop.correct') as correct:
                connector.process(job)
                action.assert_called_once_with('question',{'question':'Which bar?'})
                correct.assert_not_called()
                self.assertTrue((root/'private/jobs/j-1/job.json').is_file())

    def test_images_require_visual_observations_before_work_continues(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'config.json';config.write_text(json.dumps({'url':'https://example.test','token':'test','work':str(root/'private')}));connector=Connector(config)
            target={'symbol':'fixture','revision':'r1','signature':'a'*64,'comments':[]}
            def images(comments,output):
                output.mkdir(parents=True);(output/'manifest.json').write_text('[]');return [output/'private.png']
            with patch.object(connector,'heartbeat'),patch.object(connector.client,'revision',return_value={'id':'r1','symbol':{'id':'fixture'},'source':{'definition':{},'recipe':'source'}}),patch.object(connector.client,'comment_images',side_effect=images),patch('review_desktop.run_codex',return_value={'intent':'Shorten bar','question':'','image_observations':[]}):
                with self.assertRaisesRegex(ValueError,'inspection evidence'):connector.process({'id':'j','workflow':2,'lease':'l','publications':[],'corrections':[target],'results':[]})


if __name__=='__main__': unittest.main()
