from support import APP, FIXTURES
import io
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
import sys
from core import ROOT, SVG, ValidationError, validate_svg_references, find_symbols, definitions, configuration_choices
from exports import LIBRARY, catalog, choose, export, artwork, place, document


class LibraryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=catalog()
        cls.items=[c for s in cls.data['symbols'] for c in s['configurations']]

    def test_complete_definitions_and_unique_configurations(self):
        self.assertEqual({s['id'] for s in self.data['symbols']}, {s['id'] for s in definitions()})
        self.assertEqual(len(self.items),sum(len(configuration_choices(s)) for s in self.data['symbols']))
        self.assertEqual(len({c['key'] for c in self.items}),len(self.items))
        self.assertEqual({p.name for p in (LIBRARY/'svg').glob('*.svg')},
                         {c['key']+'.svg' for c in self.items}, 'Obsolete or missing catalog SVGs')
        for symbol in self.data['symbols']:
            self.assertEqual(len(symbol['configurations']),len(configuration_choices(symbol)))
            self.assertTrue(all(c['symbol_id']==symbol['id'] for c in symbol['configurations']))
        for config in self.items:
            data = (LIBRARY / config['svg']).read_bytes()
            self.assertEqual(len(data), config['svg_bytes'], config['key'])

    def test_semantics_and_search(self):
        zigzags = find_symbols('zigzag')
        self.assertIn('resistor-us',[s['id'] for s in zigzags])
        self.assertTrue(all(s['attributes']['body']=='zigzag' for s in zigzags))
        self.assertEqual([s['id'] for s in find_symbols('coil')],['inductor-coil'])
        amp=next(s for s in self.data['symbols'] if s['id']=='opamp')
        self.assertEqual({p['id'] for p in amp['pins']},{'in-plus','in-minus','out'})

    def test_all_strokes_preserve_geometry_and_grid(self):
        for symbol in self.data['symbols']:
            settings = {(c['size'], tuple(sorted(c.get('options', {}).items()))) for c in symbol['configurations']}
            for size, options in settings:
                group=[c for c in symbol['configurations'] if c['size']==size and tuple(sorted(c.get('options', {}).items()))==options]
                drawings=[]
                for c in group:
                    root=artwork(c)
                    drawings.append([p.get('d') for p in root.iter(f'{{{SVG}}}path')])
                    self.assertEqual(c['pins_mm'],group[0]['pins_mm'])
                    self.assertEqual(c['dimensions_mm'],group[0]['dimensions_mm'])
                    self.assertTrue(all(float(v).is_integer() for xy in c['pins_mm'].values() for v in xy))
                    width=float(root.find(f'{{{SVG}}}g').get('stroke-width'))*25.4/72.27
                    self.assertAlmostEqual(width,c['settings']['stroke_mm'],delta=.00001)
                self.assertEqual(drawings[0],drawings[1]);self.assertEqual(drawings[1],drawings[2])

    def test_grid_footprints(self):
        for c in self.items:
            if c['symbol_id'] in ('resistor-eu','resistor-us','inductor-coil'):
                end={'small':7,'medium':8,'large':10}[c['size']]
                self.assertEqual(c['pins_mm'],{'a':[-end,0],'b':[end,0]})
                self.assertAlmostEqual(c['dimensions_mm']['body-width'],{'small':7.5,'medium':10,'large':12.5}[c['size']],delta=.0001)
            if c['symbol_id']=='capacitor':
                end={'small':4,'medium':4,'large':5}[c['size']]
                self.assertEqual(c['pins_mm'],{'a':[-end,0],'b':[end,0]})

    def test_export_repeated_instances_no_ids_or_markers(self):
        key='inductor-coil-small-thick'
        for kind in ('sheet','symbols'):
            _,_,body=export(kind,[key,key,'opamp-large-thin'])
            root=ET.fromstring(body);validate_svg_references(root)
            self.assertEqual(len(list(root.iter(f'{{{SVG}}}circle'))),0)
            self.assertEqual(len(list(root.iter(f'{{{SVG}}}symbol'))),3 if kind=='symbols' else 0)
            self.assertEqual(len([e for e in root.iter() if e.get('data-symbol')]),3)

    def test_zip_files_and_individual_match(self):
        keys=['capacitor-small-thick','capacitor-small-thick','opamp-medium-medium']
        _,_,body=export('zip',keys)
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            self.assertEqual(len(archive.namelist()),3);self.assertIsNone(archive.testzip())
            for key,name in zip(keys,archive.namelist()):
                self.assertEqual(archive.read(name),export('svg',[key])[2])

    def test_spacing_columns_change_layout_not_artwork(self):
        keys=['opamp-large-thick','inductor-coil-small-thin','capacitor-medium-medium']
        a=ET.fromstring(export('sheet',keys,columns=3,spacing=2)[2])
        b=ET.fromstring(export('sheet',keys,columns=1,spacing=10)[2])
        self.assertNotEqual(a.get('width'),b.get('width'))
        self.assertNotEqual(a.get('height'),b.get('height'))
        self.assertEqual([e.get('d') for e in a.iter(f'{{{SVG}}}path')],[e.get('d') for e in b.iter(f'{{{SVG}}}path')])

    def test_invalid_inputs(self):
        for keys in ([],['missing'],['../core.py'],[None]):
            with self.assertRaises(ValidationError):choose(keys)
        for cols,gap in ((0,6),(2.5,6),(3,-1),(3,float('nan')),(3,51)):
            with self.assertRaises(ValidationError):export('sheet',['opamp-medium-medium'],cols,gap)
        with self.assertRaises(ValidationError):export('svg',['opamp-medium-medium']*2)

    def test_approved_paths_unchanged(self):
        accepted = json.loads((FIXTURES / 'accepted-geometry.json').read_text())
        checked = set()
        for config in self.items:
            if config['key'] not in accepted:
                continue
            checked.add(config['key'])
            self.assertEqual(accepted[config['key']]['paths'],
                             [p.get('d') for p in artwork(config).iter(f'{{{SVG}}}path')])
            self.assertEqual(accepted[config['key']]['sha256'], hashlib.sha256((LIBRARY/config['svg']).read_bytes()).hexdigest())
        self.assertEqual(checked,set(accepted))



if __name__=='__main__':unittest.main()
