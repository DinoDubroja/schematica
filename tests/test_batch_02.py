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
        cls.data=catalog();cls.new=[s for s in cls.data['symbols'] if s.get('batch','').startswith('overnight-') and s['batch'].endswith('-02')]
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

    def test_sources_have_explicit_polarity_and_distinct_ground_references(self):
        ground_shapes={}
        for symbol in self.new:
            if symbol['family']!='sources-and-grounds':continue
            sid=symbol['id']
            for config in symbol['configurations']:
                pins=config['pins_mm'];parts={g.get('data-part'):g for g in artwork(config).iter() if g.get('data-part')}
                if sid.startswith('source-'):
                    if 'current' in sid or sid.endswith('-ac'):self.assertEqual(set(pins),{'a','b'})
                    else:
                        self.assertEqual(set(pins),{'positive','negative'})
                        self.assertGreater(pins['positive'][1],pins['negative'][1])
                    if 'current' in sid:
                        shaft,head=parts['current-direction'].iter(f'{{{SVG}}}path')
                        pts=straight_points(shaft);tri=straight_points(head)
                        self.assertGreater(pts[1][1],pts[0][1])
                        self.assertGreater(tri[1][1],(tri[0][1]+tri[2][1])/2)
                    if sid.endswith('-ac'):self.assertTrue('ac-wave' in parts and 'positive-mark' not in parts)
                elif sid in ('cell','battery'):
                    self.assertLess(pins['positive'][0],pins['negative'][0])
                    plates=[next(g.iter(f'{{{SVG}}}path')) for pid,g in parts.items() if pid.startswith('plate-')]
                    self.assertEqual(len(plates),4 if sid=='battery' else 2)
                    heights=[abs(straight_points(p)[1][1]-straight_points(p)[0][1]) for p in plates]
                    self.assertTrue(all(heights[i]>heights[i+1] for i in range(0,len(heights),2)))
                elif sid.startswith('ground-'):
                    self.assertEqual(set(pins),{'reference'});self.assertGreater(pins['reference'][1],0)
                    paths=[p.get('d') for p in parts['ground-mark'].iter(f'{{{SVG}}}path')]
                    self.assertEqual(len(paths),{'ground-earth':3,'ground-signal':1,'ground-chassis':4}[sid])
                    if config['size']=='medium' and config['stroke']=='medium':ground_shapes[sid]=tuple(paths)
                else:self.assertEqual(set(pins),{'net'})
        self.assertEqual(len(set(ground_shapes.values())),len(ground_shapes))

    def test_transformer_windings_stay_isolated_and_center_tap_meets_secondary(self):
        for symbol in self.new:
            if not symbol['id'].startswith('transformer-'):continue
            tapped=symbol['id']=='transformer-center-tap'
            for config in symbol['configurations']:
                pins=config['pins_mm'];self.assertEqual(len(pins),5 if tapped else 4)
                parts={g.get('data-part'):g for g in artwork(config).iter() if g.get('data-part')}
                winding_points={}
                for prefix,sign in [('primary',-1),('secondary',1)]:
                    self.assertGreater(sign*pins[prefix+'-1'][0],0)
                    self.assertEqual(pins[prefix+'-1'][0],pins[prefix+'-2'][0])
                    self.assertGreater(pins[prefix+'-1'][1],0);self.assertLess(pins[prefix+'-2'][1],0)
                    path=next(parts[prefix+'-winding'].iter(f'{{{SVG}}}path'))
                    coords=[float(n)*25.4/72.27 for n in re.findall(NUMBER,path.get('d'))]
                    points=list(zip(coords[::2],coords[1::2]));winding_points[prefix]=points
                    # All cubic controls and endpoints stay on their own side of the core.
                    self.assertTrue(all(sign*x>1.1*config['settings']['size_factor'] for x,y in points))
                    self.assertIn(prefix+'-polarity',parts)
                self.assertEqual('magnetic-core' in parts,symbol['id']!='transformer-air')
                if tapped:
                    self.assertEqual(pins['secondary-center'][1],0)
                    path=next(parts['lead-secondary-center'].iter(f'{{{SVG}}}path'))
                    join=straight_points(path)[-1]
                    self.assertTrue(any(math.dist(join,p)<.0003 for p in winding_points['secondary']))

    def test_analog_functional_terminal_sets_and_polarity(self):
        expected={
            'comparator':{'in-plus','in-minus','out'},
            'comparator-supply':{'in-plus','in-minus','out','supply-plus','supply-minus'},
            'amplifier-fully-differential':{'in-plus','in-minus','out-plus','out-minus'},
            'amplifier-instrumentation':{'in-plus','in-minus','out','reference','gain-1','gain-2'},
            'ota':{'in-plus','in-minus','out','bias'},'regulator':{'in','out','common'}}
        for symbol in self.new:
            if symbol['id'] not in expected:continue
            sid=symbol['id'];self.assertEqual({p['id'] for p in symbol['pins']},expected[sid])
            for config in symbol['configurations']:
                pins=config['pins_mm']
                if sid=='regulator':
                    self.assertLess(pins['in'][0],pins['out'][0]);self.assertLess(pins['common'][1],0)
                    continue
                self.assertEqual(pins['in-plus'][1],3);self.assertEqual(pins['in-minus'][1],-3)
                if sid=='amplifier-fully-differential':
                    self.assertGreater(pins['out-plus'][1],pins['out-minus'][1])
                    self.assertGreater(pins['out-plus'][0],pins['in-plus'][0])
                else:self.assertGreater(pins['out'][0],pins['in-plus'][0])
                if sid=='comparator-supply':
                    self.assertGreater(pins['supply-plus'][1],3);self.assertLess(pins['supply-minus'][1],-3)
                elif sid=='amplifier-instrumentation':
                    self.assertLess(pins['reference'][1],-3)
                    self.assertGreater(pins['gain-1'][1],3);self.assertGreater(pins['gain-2'][1],3)
                elif sid=='ota':
                    self.assertLess(pins['bias'][1],0)
                    group=next(g for g in artwork(config).iter() if g.get('data-part')=='current-output')
                    head=straight_points(next(group.iter(f'{{{SVG}}}path')))
                    self.assertGreater(head[1][0],(head[0][0]+head[2][0])/2)

    def test_logic_inversion_input_anchors_and_active_high_enable(self):
        bodies={}
        inverted={'nand','nor','xnor','not','schmitt-inverter','tristate-inverter'}
        two_inputs={'and','nand','or','nor','xor','xnor'}
        for symbol in self.new:
            if symbol['family']!='logic':continue
            kind=symbol['id'].removeprefix('logic-');two=kind in two_inputs;tri=kind.startswith('tristate')
            expected=({'a','b','out'} if two else {'in','out','enable'} if tri else {'in','out'})
            self.assertEqual({p['id'] for p in symbol['pins']},expected)
            for config in symbol['configurations']:
                factor=config['settings']['size_factor'];pins=config['pins_mm']
                parts={g.get('data-part'):g for g in artwork(config).iter() if g.get('data-part')}
                self.assertEqual('inversion' in parts,kind in inverted)
                self.assertEqual('exclusive-mark' in parts,kind in ('xor','xnor'))
                self.assertEqual('hysteresis' in parts,kind.startswith('schmitt'))
                self.assertGreater(pins['out'][0],0)
                body=next(parts['body'].iter(f'{{{SVG}}}path'))
                bodies[kind,config['size'],config['stroke']]=body.get('d')
                for pin in ('a','b') if two else ('in',):
                    self.assertLess(pins[pin][0],0)
                    endpoint=straight_points(next(parts['lead-'+pin].iter(f'{{{SVG}}}path')))[-1]
                    if kind in ('or','nor','xor','xnor'):
                        # Concave input edge is a quadratic parabola; the lead must meet it.
                        expected_x=-2.5*factor-endpoint[1]**2/(8*factor)
                        self.assertAlmostEqual(endpoint[0],expected_x,delta=.0003)
                    else:self.assertAlmostEqual(endpoint[0],-4.5*factor,delta=.0003)
                if two:self.assertEqual([pins['a'][1],pins['b'][1]],[2,-2])
                if tri:
                    self.assertEqual(symbol['attributes']['enable_active'],'high')
                    self.assertLess(pins['enable'][1],0)
                    endpoint=straight_points(next(parts['lead-enable'].iter(f'{{{SVG}}}path')))[-1]
                    self.assertLess(math.dist(endpoint,(0,-2*factor)),.0003)
        for a,b in [('and','nand'),('or','nor'),('xor','xnor'),('buffer','not'),('schmitt-buffer','schmitt-inverter'),('tristate-buffer','tristate-inverter')]:
            for kind,size,stroke in list(bodies):
                if kind==a:self.assertEqual(bodies[kind,size,stroke],bodies[b,size,stroke])


if __name__=='__main__':unittest.main()
