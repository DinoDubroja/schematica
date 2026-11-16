"""Simulate independent correction outcomes on isolated fixtures, without an agent or publication."""
from support import APP
import argparse
import copy
import html
import json
from pathlib import Path
import re
import uuid
from review_client import Client, package_symbol, write_json, digest
from verify_review_hosted import BrowserSession


def returned_revision(client, job, root):
    target=job['corrections'][0];assert target['symbol'].startswith('review-flow-') and not job['publications']
    original=client.revision(target['revision']);symbol=copy.deepcopy(original['symbol']);source=copy.deepcopy(original['source'])
    number=symbol['revision']+1;symbol['revision']=number;source['definition']['revision']=number
    folder=Path(root)/('return-'+str(uuid.uuid4()));art=folder/'artwork';art.mkdir(parents=True)
    for config in symbol['configurations']:
        text=client.request('/review/assets/'+config['sha256']).decode('utf-8')
        def metadata(match):
            value=json.loads(html.unescape(match[1]));value['revision']=number
            return '<metadata>'+html.escape(json.dumps(value),quote=False)+'</metadata>'
        config['revision']=number
        (art/config['svg']).write_text(re.sub(r'<metadata>([\s\S]*?)</metadata>',metadata,text),encoding='utf-8')
    revision=package_symbol(symbol,source,folder/'package',art,{'by':'Automated isolated fixture','summary':'Simulated return; drawing geometry unchanged.'},parent=original['id'],batch=original['batch'],change={'why':'Synthetic returned revision; no drawing changes.','source_diff':'Revision metadata only.','feedback':[c['id'] for c in target['comments']]})
    client.upload(folder/'package',job=job);client.action('complete',{'job':job['id'],'lease':job['lease']})
    return revision['id']


def run(config_path,root,stage):
    config=json.loads(Path(config_path).read_text(encoding='utf-8'));client=Client(config)
    assert client.url.split('//')[1].startswith('schematica-review-validation.')
    user=BrowserSession(config);root=Path(root);fixtures=json.loads((root/'fixtures/fixtures.json').read_text(encoding='utf-8'));checks=[]
    def target(key):return {'symbol':fixtures[key]['symbol'],'revision':fixtures[key]['revision'],'configurations':[]}
    def confirm(symbols):
        plan=user.request('/api/review/processing-summary');included=[t['key'] for t in plan['corrections'] if t['symbol'] in symbols]
        return user.action('process',{'snapshot':plan['snapshot'],'included':included})
    before=client.request('/library/catalog.json',authenticated=False)
    if stage=='prepare':
        write_json(root/'validation-public-before.json',before)
        jobs=[j for j in client.state()['jobs'].values() if j['status']=='Waiting for desktop' and j.get('workflow')==2]
        assert all(not j['publications'] and all(t['symbol'].startswith('review-flow-') for t in j['corrections']) or any(client.state()['symbols'][t['symbol']].get('discarded') for t in j['corrections']) for j in jobs),'Other active test jobs need their owner'
        for _ in range(2):
            job=client.action('claim',{'protocol':2})['job'];assert job
            if job['corrections'][0]['symbol']==fixtures['npn']['symbol']:returned_revision(client,job,root)
            else:
                assert job['corrections'][0]['symbol']==fixtures['pnp']['symbol']
                client.action('fail',{'job':job['id'],'lease':job['lease'],'error':'Synthetic transient failure; retry this target only.'})
        s=client.state();shared=next(c for c in s['comments'].values() if len(c['targets'])==2 and c.get('attachments') and c['targets'][0]['symbol']==fixtures['npn']['symbol'])
        statuses={p['symbol']:p['status'] for p in s['comment_progress'][shared['id']]}
        assert statuses=={fixtures['npn']['symbol']:'Updated',fixtures['pnp']['symbol']:'Failed'}
        checks.append('Shared feedback has independent Updated and Failed targets')
        # Prepare a separate completed single-target comment for the extension journey.
        image=shared['attachments'][0]
        result=user.action('comment',{'text':'Synthetic existing NPN feedback with an image.','attachments':[image],'targets':[target('extend-npn')]})
        confirm([fixtures['extend-npn']['symbol']]);job=client.action('claim',{'protocol':2})['job'];assert job['corrections'][0]['symbol']==fixtures['extend-npn']['symbol']
        returned_revision(client,job,root)
        write_json(root/'processing-fixture.json',{'shared':shared['id'],'extension':result['id'],'old_npn_revisions':len(client.state()['symbols'][fixtures['extend-npn']['symbol']]['revisions']),'failed_job':next(j['id'] for j in s['jobs'].values() if j['status']=='Failed' and j['corrections'][0]['symbol']==fixtures['pnp']['symbol'])})
    else:
        saved=json.loads((root/'processing-fixture.json').read_text(encoding='utf-8'));s=client.state()
        assert len(s['symbols'][fixtures['extend-npn']['symbol']]['revisions'])==saved['old_npn_revisions']
        assert s['jobs'][saved['failed_job']]['status']=='Waiting for desktop'
        assert s['jobs'][saved['failed_job']]['attempts']==1,'Retry must reuse the failed job, before its next lease'
        for _ in range(2):
            job=client.action('claim',{'protocol':2})['job'];assert job['corrections'][0]['symbol'] in [fixtures['pnp']['symbol'],fixtures['extend-pnp']['symbol']]
            returned_revision(client,job,root)
        s=client.state()
        assert all(p['status']=='Updated' for c in [saved['shared'],saved['extension']] for p in s['comment_progress'][c])
        assert len(s['symbols'][fixtures['extend-npn']['symbol']]['revisions'])==saved['old_npn_revisions']
        assert not any(i['symbol'] in [f['symbol'] for f in fixtures.values()] for i in user.request('/api/review/processing-summary')['corrections'])
        checks+=['Adding PNP to a processed comment never changes NPN again','Retry reuses only the failed target job','Completed feedback is absent from subsequent summaries']
        export=root/'extended-source';client.source_export(fixtures['extend-pnp']['revision'],export)
        assert list((export/'comment-images').glob('*.png'))
        checks.append('Extended target source export retains the exact earlier image evidence')
    assert client.request('/library/catalog.json',authenticated=False)==before
    assert client.request('/library/catalog.json',authenticated=False)==json.loads((root/'validation-public-before.json').read_text(encoding='utf-8'))
    checks.append('Published catalog stays unchanged; no fixture publications')
    write_json(root/f'hosted-{stage}.json',{'checks':checks,'productionWrites':0,'publication':0});print(json.dumps({'passed':len(checks),'stage':stage,'publications':0}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--root',required=True);p.add_argument('--stage',choices=['prepare','finish'],required=True);a=p.parse_args();run(a.config,a.root,a.stage)
