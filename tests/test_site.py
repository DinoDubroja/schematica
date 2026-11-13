from support import APP, FIXTURES
"""Check the actual portable download bundle, not copies of viewer logic."""
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET

from build_site import payload, VIEWER_FILES
from core import SVG, validate_svg_references, configuration_choices
from exports import LIBRARY


class StaticSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = payload()
        cls.catalog = json.loads(cls.files['library/catalog.json'])

    def test_each_library_has_all_distinct_symbols_at_one_preset(self):
        self.assertEqual(len(self.catalog['exports']), 36)
        expected_ids = {s['id'] for s in self.catalog['symbols']}
        for preset, path in self.catalog['exports'].items():
            settings = self.catalog['export_settings'][preset]
            size, stroke = settings['size'], settings['stroke']
            root = ET.fromstring(self.files[path])
            validate_svg_references(root)
            symbols = root.findall(f'{{{SVG}}}defs/{{{SVG}}}symbol')
            self.assertEqual(len(symbols), len(self.catalog['symbols']))
            self.assertEqual(root.find(f'{{{SVG}}}title').text, f'Schematica · {size.title()} / {stroke.title()}')
            self.assertEqual({s.find(f'{{{SVG}}}title').text for s in symbols},
                             {s['name'] for s in self.catalog['symbols']})
            metadata = [json.loads(s.find(f'{{{SVG}}}metadata').text) for s in symbols]
            self.assertEqual({m['symbol_id'] for m in metadata}, expected_ids)
            self.assertTrue(all(m['size'] == size and m['stroke'] == stroke for m in metadata))
            self.assertTrue(root.get('width').endswith('mm'))
            self.assertFalse(any('inspection-grid' in e.get('class','') or 'pin-markers' in e.get('class','') for e in root.iter()), 'Preview markers leaked into export')
            for symbol, meta in zip(symbols, metadata):
                definition = next(s for s in self.catalog['symbols'] if s['id'] == meta['symbol_id'])
                self.assertEqual(meta.get('options', {}),
                    {key: settings['options'].get(key, spec['default']) for key, spec in definition.get('options', {}).items()})
                self.assertEqual({e.get('data-part') for e in symbol.iter() if e.get('data-part')},
                                 {p['id'] for p in definition['parts']})

    def test_individual_artwork_is_copied_without_changes(self):
        configs = [c for s in self.catalog['symbols'] for c in s['configurations']]
        self.assertEqual(len(configs), sum(len(configuration_choices(s)) for s in self.catalog['symbols']))
        for config in configs:
            self.assertEqual(self.files['library/' + config['svg']], (LIBRARY / config['svg']).read_bytes())

    def test_repeatable_build_and_publish_allowlist(self):
        self.assertEqual(self.files, payload())
        self.assertEqual(len(self.files), len(VIEWER_FILES) + 2 + len(self.catalog['exports']) +
                         sum(len(s['configurations']) for s in self.catalog['symbols']))
        manifest = json.loads(self.files['build.json'])
        for name, expected in manifest['files'].items():
            self.assertEqual(hashlib.sha256(self.files[name]).hexdigest(), expected)
        self.assertFalse(any(name.endswith(('.py', '.yaml', '.tex', '.pdf', '.zip')) for name in self.files))
        self.assertTrue(all(s['keywords'] and s['description'] for s in self.catalog['symbols']))


if __name__ == '__main__':
    unittest.main()
