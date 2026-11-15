from support import APP
import copy
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from review_client import Client, digest, package_symbol, recovery_sql, write_json
from core import get_definition
from exports import catalog, LIBRARY


class ReviewClientTests(unittest.TestCase):
    def test_recovery_preserves_crlf_unicode_and_large_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = '<svg>\r\nπ & text\r\n</svg>' + '\nlong row ' * 15000
            h = digest(body)
            data = {"state": [{"id": 1, "version": 7, "token": "saved", "body": '{"symbols":{}}'}],
                    "assets": [{"hash": h, "mime": "image/svg+xml", "body": body}],
                    "events": [], "revisions": [], "requests": [], "publication": []}
            manifest = {"consistent": True, "collections": {}}
            for table, rows in data.items():
                path = root / (table + '.json'); write_json(path, rows)
                manifest["collections"][table] = {"rows": len(rows), "sha256": digest(path.read_bytes())}
            write_json(root / 'manifest.json', manifest)
            output = root / 'restore.sql'; recovery_sql(root, output)
            db = sqlite3.connect(':memory:'); db.executescript(output.read_text(encoding='utf-8'))
            self.assertEqual(db.execute('SELECT body FROM assets').fetchone()[0], body)
            self.assertEqual(db.execute('SELECT version FROM state').fetchone()[0], 7)
            self.assertLess(max(len(line.encode()) for line in output.read_text().splitlines()), 100000)
            db.close()
            manifest['consistent'] = False; write_json(root / 'manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'consistent'):
                recovery_sql(root, root / 'invalid.sql')

    def test_package_preserves_exact_artwork_and_resolves_physical_center(self):
        symbol = copy.deepcopy(catalog()['symbols'][0])
        for c in symbol['configurations']:
            c.pop('visual_center_from_origin_mm', None)
        source = {'definition': get_definition(symbol['id']), 'recipe': 'fixture source'}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'package'
            revision = package_symbol(symbol, source, root, LIBRARY, {'by': 'test', 'summary': 'Packaging only'})
            for c in revision['symbol']['configurations']:
                self.assertEqual((root / 'assets' / (c['sha256'] + '.svg')).read_bytes(), (LIBRARY / c['svg']).read_bytes())
                self.assertEqual(len(c['visual_center_from_origin_mm']), 2)
                self.assertLess(max(abs(v) for v in c['visual_center_from_origin_mm']), .001)

    def test_client_requires_encrypted_remote_transport(self):
        with self.assertRaises(ValueError):
            Client({'url': 'http://remote.example', 'token': 'test'})
        self.assertEqual(Client({'url': 'https://example.test/', 'token': 'test'}).url, 'https://example.test')


if __name__ == '__main__':
    unittest.main()
