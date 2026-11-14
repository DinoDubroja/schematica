"""Drawing invariants, exact option selection, and physical family proportions."""
from support import APP
import copy
import math
import re
import unittest
from core import SVG, ValidationError, get_definition, resolve_options, validate_definition, read_yaml
from exports import catalog, artwork, library_selection


def paths(config, part):
    return [e.get('d') for g in artwork(config).iter() if g.get('data-part') == part
            for e in g.iter(f'{{{SVG}}}path')]


def points(path):
    # The tested adjustment/arrow paths contain absolute M/L commands only.
    values = [float(v) for v in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', path)]
    return list(zip(values[::2], values[1::2]))


class SymbolOptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.symbols = catalog()['symbols']

    def test_options_are_validated(self):
        definition = get_definition('resistor-variable-eu')
        self.assertEqual(resolve_options(definition), {'orientation': 'up-right'})
        for selection in ({'orientation': 'sideways'}, {'unknown': 'up-right'}):
            with self.assertRaises(ValidationError): resolve_options(definition, selection)
        with self.assertRaises(ValidationError): resolve_options(get_definition('resistor-eu'), {'orientation':'up-right'})
        for change in ('missing', 'duplicate', 'default'):
            bad = copy.deepcopy(definition)
            if change == 'missing': bad['options']['orientation']['values'].pop()
            if change == 'duplicate': bad['options']['orientation']['values'].append(bad['options']['orientation']['values'][0])
            if change == 'default': bad['options']['orientation']['default'] = 'unknown'
            with self.assertRaises(ValidationError): validate_definition(bad, read_yaml(APP / 'presets.yaml'))

    def test_reflections_change_only_adjustment_and_preserve_pin_identity(self):
        for symbol in self.symbols:
            if not symbol.get('options'): continue
            self.assertEqual(len(symbol['configurations']), 36)
            for size in symbol['presets']['sizes']:
                for stroke in symbol['presets']['strokes']:
                    base = library_selection(symbol, size, stroke)
                    for orientation, (sx, sy) in {'up-right':(1,1),'up-left':(-1,1),'down-right':(1,-1),'down-left':(-1,-1)}.items():
                        current = library_selection(symbol, size, stroke, {'orientation':orientation})
                        self.assertEqual(current['pins_mm'], base['pins_mm'])
                        for part in ('body','lead-a','lead-b'): self.assertEqual(paths(current, part), paths(base, part))
                        for a, b in zip(paths(base, 'adjustment'), paths(current, 'adjustment')):
                            for (x,y), (xx,yy) in zip(points(a), points(b)):
                                self.assertAlmostEqual(xx, sx*x, delta=.00015)
                                self.assertAlmostEqual(yy, sy*y, delta=.00015)

    def test_centered_potentiometer_gap_and_vertical_lead(self):
        for symbol in self.symbols:
            if symbol.get('drawing', {}).get('variant') not in ('potentiometer','trimmer-potentiometer'): continue
            for config in symbol['configurations']:
                dimensions = config['dimensions_mm']
                self.assertEqual(dimensions['wiper-tip-x'], 0)
                self.assertAlmostEqual(dimensions['wiper-tip-y'] - dimensions['body-height']/2, 1, delta=.00002)
                self.assertEqual(dimensions['wiper-body-gap'], 1)
                self.assertRegex(paths(config, 'lead-wiper')[0], r'^M0\s+[-\d.]+(?:V[-\d.]+|L0\s+[-\d.]+)$')

    def test_photo_arrows_are_symmetric_parallel_and_equally_spaced(self):
        for symbol in self.symbols:
            if not symbol.get('drawing', {}).get('variant', '').startswith('photo'): continue
            for config in symbol['configurations']:
                shaft1, head1, shaft2, head2 = map(points, paths(config, 'light-arrows'))
                s = config['settings']['size_factor']*5/3
                mm = 25.4/72.27
                vectors = [(a[0]-b[0],a[1]-b[1]) for a,b in (shaft1,shaft2)]
                # PGF fixed-point arithmetic is quantized below 0.0003 mm.
                self.assertAlmostEqual(math.dist(*shaft1)*mm, 2*s, delta=.0003)
                for x,y in vectors: self.assertAlmostEqual(x,y,delta=.0001)
                self.assertAlmostEqual(math.dist(shaft1[1],shaft2[1])*mm, 1.5*s,delta=.0003)
                for head in (head1,head2):
                    self.assertAlmostEqual(math.dist(head[0],head[1]),math.dist(head[2],head[1]),delta=.0001)

    def test_variable_arrowheads_clear_body_at_small_thick(self):
        for symbol in self.symbols:
            if symbol.get('drawing', {}).get('variant') != 'variable': continue
            for value in symbol['options']['orientation']['values']:
                config = library_selection(symbol,'small','thick',{'orientation':value['id']})
                head = points(paths(config, 'adjustment')[1])
                clearance = min(abs(y) for x,y in head)*25.4/72.27 - config['dimensions_mm']['body-height']/2 - config['settings']['stroke_mm']
                self.assertGreater(clearance, .38, config['key'])

    def test_new_marks_and_no_varistors(self):
        self.assertFalse(any('varistor' in s['id'] for s in self.symbols))
        for symbol in self.symbols:
            variant = symbol.get('drawing', {}).get('variant')
            for config in symbol['configurations']:
                if variant == 'nonlinear':
                    mark = paths(config, 'nonlinear-mark')
                    self.assertEqual(len(mark), 1)
                    # The user selected B: one smooth cubic, not two joined lobes.
                    self.assertEqual(re.findall(r'[A-Za-z]', mark[0]), ['M', 'C'])
                    actual = points(mark[0])
                    self.assertEqual(len(actual), 4)
                    f = config['settings']['size_factor']
                    expected = [(-5.6, 0), (-5.6/3, 3.4), (5.6/3, -3.4), (5.6, 0)]
                    for (x, y), (u, v) in zip(actual, expected):
                        # Stored paths use y-up TeX points; the chat proof used mm.
                        self.assertAlmostEqual(x*25.4/72.27, f*(u+v)/math.sqrt(2), delta=.0002)
                        self.assertAlmostEqual(y*25.4/72.27, f*(u-v)/math.sqrt(2), delta=.0002)
                if variant in ('ntc','ptc'):
                    root = artwork(config)
                    part = next(e for e in root.iter() if e.get('data-part') == 'temperature-mark')
                    self.assertEqual(len(list(part.iter(f'{{{SVG}}}use'))), 3)
                    self.assertFalse(list(part.iter(f'{{{SVG}}}text')))


if __name__ == '__main__': unittest.main()
