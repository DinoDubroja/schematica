"""Independent preservation, categorization and electrical lead checks for batch 02."""
from support import APP, FIXTURES
import hashlib
import json
import math
import re
import unittest
from core import SVG, definitions, configuration_choices
from exports import catalog, artwork, LIBRARY
from verification import read_ledger, publication_catalog

FAMILIES = {'resistors','capacitors','inductors-and-transformers','diodes','transistors',
            'analog','logic','sources-and-grounds','switches-and-relays',
            'connections-and-instruments','protection-and-resonators'}
NUMBER = r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'


def straight_points(path):
    """Decode the actual converter path, including its H/V optimizations."""
    points=[];x=y=0
    for command,values in re.findall(r'([MLHVZ])([^MLHVZ]*)',path.get('d')):
        values=[float(n)*25.4/72.27 for n in re.findall(NUMBER,values)]
        if command in ('M','L'):
            for i in range(0,len(values),2):
                x,y=values[i:i+2];points.append((x,y))
        elif command=='H':
            for x in values:points.append((x,y))
        elif command=='V':
            for y in values:points.append((x,y))
    return points


class Batch02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=catalog();cls.new=[s for s in cls.data['symbols'] if s.get('batch','').startswith('overnight-')]
        cls.baseline=json.loads((FIXTURES/'approved-before-batch-02.json').read_text(encoding='utf-8'))

    def test_previously_accepted_svg_bytes_and_approvals_unchanged(self):
        for path,expected in self.baseline['svg_sha256'].items():
            self.assertEqual(hashlib.sha256((LIBRARY/path).read_bytes()).hexdigest(),expected,path)
        ledger=read_ledger()['approvals']
        for sid,expected in self.baseline['approvals'].items():self.assertEqual(ledger[sid],expected,sid)
        ids={s['id'] for s in self.data['symbols']}
        self.assertTrue(set(self.baseline['approvals'])<=ids)
        self.assertFalse(any('varistor' in sid or 'resistor-tapped' in sid for sid in ids))

    def test_every_design_has_one_supported_family(self):
        for definition in definitions():
            self.assertIn(definition.get('family'),FAMILIES,definition['id'])
            self.assertTrue(definition['description'].strip())
            self.assertTrue(definition['keywords'])
        for symbol in self.new:
            self.assertEqual(symbol['batch'],'overnight-'+symbol['family']+'-02')
            self.assertIn('overnight',symbol['keywords'])
            self.assertTrue(symbol['reference']['symbol'])
            self.assertEqual(len(symbol['configurations']),len(configuration_choices(symbol)))

    def test_new_leads_end_at_declared_electrical_pins(self):
        # Compare actual path endpoints to semantics; do not trust emitted pin metadata alone.
        for symbol in self.new:
            for config in symbol['configurations']:
                root=artwork(config)
                parts={g.get('data-part'):g for g in root.iter() if g.get('data-part')}
                for pin in symbol['pins']:
                    path=next(parts[pin['lead_part']].iter(f'{{{SVG}}}path'))
                    start=re.match(r'M\s*('+NUMBER+r')[,\s]*('+NUMBER+r')',path.get('d'))
                    self.assertIsNotNone(start,config['key']+'/'+pin['id'])
                    # TeX coordinates are points (72.27/in), before the converter transform.
                    actual=[float(start[i])*25.4/72.27 for i in (1,2)]
                    for a,b in zip(actual,config['pins_mm'][pin['id']]):self.assertAlmostEqual(a,b,delta=.0001)
                self.assertEqual(len({tuple(xy) for xy in config['pins_mm'].values()}),len(symbol['pins']))

    def test_new_adjustment_options_never_move_electrical_parts(self):
        for symbol in self.new:
            if not symbol.get('options'):continue
            for size in symbol['presets']['sizes']:
                for stroke in symbol['presets']['strokes']:
                    choices=[c for c in symbol['configurations'] if c['size']==size and c['stroke']==stroke]
                    shapes=[]
                    for c in choices:
                        shapes.append([(g.get('data-part'),[p.attrib for p in g.iter(f'{{{SVG}}}path')])
                                       for g in artwork(c).iter() if g.get('data-part') and g.get('data-part')!='adjustment'])
                        self.assertEqual(c['pins_mm'],choices[0]['pins_mm'])
                    self.assertTrue(all(s==shapes[0] for s in shapes[1:]),symbol['id'])

    def test_diode_polarity_and_actual_light_arrow_direction(self):
        for symbol in self.new:
            if symbol['family']!='diodes':continue
            expected={'a','b'} if symbol['id']=='diode-tvs-bidirectional' else {'a','k'}
            self.assertEqual({p['id'] for p in symbol['pins']},expected)
            for config in symbol['configurations']:
                self.assertLess(config['pins_mm']['a'][0],config['pins_mm']['b' if 'b' in expected else 'k'][0])
                if symbol['id'] not in ('diode-led','diode-photo'):continue
                rays=next(g for g in artwork(config).iter() if g.get('data-part')=='light-arrows')
                paths=list(rays.iter(f'{{{SVG}}}path'));self.assertEqual(len(paths),4)
                direction=1 if symbol['id']=='diode-led' else -1
                shafts=[]
                for shaft,head in [(paths[0],paths[1]),(paths[2],paths[3])]:
                    points=lambda path:list(zip(*[iter([float(n)*25.4/72.27 for n in re.findall(NUMBER,path.get('d'))])]*2))
                    s,h=points(shaft),points(head);self.assertEqual(len(s),2);self.assertEqual(len(h),3)
                    self.assertGreater(direction*(s[1][0]-s[0][0]),0)
                    self.assertGreater(direction*(s[1][1]-s[0][1]),0)
                    self.assertLess(math.dist(s[1],h[1]),.0003)
                    self.assertAlmostEqual(math.dist(h[0],h[1]),math.dist(h[2],h[1]),delta=.0003)
                    self.assertAlmostEqual(math.dist(*s),10/3*config['settings']['size_factor'],delta=.0003)
                    shafts.append(s)
                self.assertAlmostEqual(math.dist(shafts[0][0],shafts[1][0]),2.5*config['settings']['size_factor'],delta=.0003)

    def test_transistor_terminals_channels_and_actual_arrow_polarity(self):
        for symbol in self.new:
            if symbol['family']!='transistors':continue
            sid=symbol['id'];device=symbol['attributes']['device'];pchannel=symbol['attributes'].get('channel')=='p'
            bjt=device=='bjt';igbt=device=='igbt';photo=sid=='phototransistor-npn';bulk=sid.endswith('-bulk')
            expected=({'collector','emitter'} if photo else {'collector','emitter','base'} if bjt else
                      {'collector','emitter','gate'} if igbt else {'drain','source','gate','bulk'} if bulk else {'drain','source','gate'})
            self.assertEqual({p['id'] for p in symbol['pins']},expected,sid)
            for config in symbol['configurations']:
                pins=config['pins_mm'];upper='collector' if bjt or igbt else 'drain';lower='emitter' if bjt or igbt else 'source'
                self.assertGreater(pins[upper][1],0);self.assertLess(pins[lower][1],0)
                if not photo:self.assertLess(pins['base' if bjt else 'gate'][0],min(pins[upper][0],pins[lower][0]))
                if bulk:self.assertGreater(pins['bulk'][0],pins[lower][0])
                parts={g.get('data-part'):g for g in artwork(config).iter() if g.get('data-part')}
                arrow_part='emitter-arrow' if bjt or igbt else 'gate-arrow' if device=='jfet' else 'body-arrow'
                points=straight_points(next(parts[arrow_part].iter(f'{{{SVG}}}path')))
                self.assertEqual(len(points),3)
                direction=points[1][0]-(points[0][0]+points[2][0])/2
                positive=(symbol['attributes'].get('polarity')!='pnp') if bjt else True if igbt else (not pchannel) if device=='jfet' else pchannel
                self.assertGreater(direction if positive else -direction,0,sid)
                if device=='mosfet':
                    self.assertEqual(len(list(parts['channel'].iter(f'{{{SVG}}}path'))),1 if 'depletion' in sid else 3)
                    self.assertEqual('body-source-link' in parts,not bulk)
                if photo:
                    rays=list(parts['light-arrows'].iter(f'{{{SVG}}}path'));self.assertEqual(len(rays),4)
                    for shaft in rays[::2]:
                        pts=straight_points(shaft)
                        self.assertGreater(pts[1][0],pts[0][0]);self.assertLess(pts[1][1],pts[0][1])


if __name__=='__main__':unittest.main()
