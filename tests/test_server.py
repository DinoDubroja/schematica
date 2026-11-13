from support import APP, FIXTURES
"""Exercise HTTP boundaries and export requests against an ephemeral local server."""
import http.client
import json
import threading
import tempfile
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from server import Handler
from build_site import payload


class QuietHandler(Handler):
    def log_message(self, *args):
        pass


class LocalServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.files = payload()
        for name, body in cls.files.items():
            path = Path(cls.temp.name) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        cls.server.site_root = cls.temp.name
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def request(self, path, body=None, headers=None):
        client = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        client.request('GET' if body is None else 'POST', path, body, headers or {})
        response = client.getresponse()
        status, data, fields = response.status, response.read(), dict(response.getheaders())
        client.close()
        return status, data, fields

    def test_catalogue_and_viewer(self):
        status, body, _ = self.request('/library/catalog.json')
        self.assertEqual(status, 200)
        self.assertEqual(sum(len(s['configurations']) for s in json.loads(body)['symbols']), 54)
        status, body, headers = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'Schematica', body)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])

    def test_unrelated_source_files_are_not_served(self):
        for path in ('/core.py', '/%2e%2e/core.py', '/library/%2e%2e/core.py', '/_headers', '/api/catalog'):
            self.assertEqual(self.request(path)[0], 404)

    def test_cross_origin_and_unknown_hosts_rejected(self):
        self.assertEqual(self.request('/library/catalog.json', headers={'Host':'outside.invalid'})[0], 403)
        self.assertEqual(self.request('/library/catalog.json', headers={'Origin':'https://outside.invalid'})[0], 403)

    def test_all_downloads_match_static_build(self):
        for name, expected in self.files.items():
            if name.endswith('.svg'):
                status, body, headers = self.request('/' + name)
                self.assertEqual(status, 200, name)
                self.assertEqual(body, expected, name)
                self.assertEqual(headers['Content-Type'], 'image/svg+xml')
        self.assertEqual(self.request('/api/export', '{}')[0], 405)


if __name__ == '__main__':
    unittest.main()
