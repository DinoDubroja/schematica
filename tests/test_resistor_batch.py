"""Electrical structure and accepted-body regression for resistor batch 01."""
from support import APP
import unittest
from core import SVG, RESISTOR_VARIANTS
from exports import catalog, artwork


class ResistorBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.symbols = {s['id']: s for s in catalog()['symbols']}
        cls.batch = [s for s in cls.symbols.values() if s.get('batch') == 'resistors-01']

    def test_inventory_has_both_appearances_without_duplicate_fixed_symbols(self):
        self.assertEqual(len(self.batch), 22)
        self.assertEqual({(s['drawing']['body'], s['drawing']['variant']) for s in self.batch},
                         {(body, variant) for body in ('eu','us') for variant in RESISTOR_VARIANTS})
        self.assertEqual(sum('resistor' in s['types'] for s in self.symbols.values()), 24)

    def test_electrical_terminals_and_accepted_body_geometry(self):
        for symbol in self.batch:
            variant = symbol['drawing']['variant']
            third = 'tap' if variant == 'tapped' else 'wiper' if variant in ('potentiometer','trimmer-potentiometer') else None
            expected = {'a','b'} | ({third} if third else set())
            self.assertEqual({p['id'] for p in symbol['pins']}, expected)
            base = self.symbols['resistor-' + symbol['drawing']['body']]
            for config in symbol['configurations']:
                reference = next(c for c in base['configurations'] if c['size']==config['size'] and c['stroke']==config['stroke'])
                self.assertEqual({p: config['pins_mm'][p] for p in ('a','b')}, reference['pins_mm'])
                self.assertEqual(config['dimensions_mm']['body-width'], reference['dimensions_mm']['body-width'])
                if third:
                    self.assertEqual(config['pins_mm'][third], [0, {'small':5,'medium':6,'large':8}[config['size']]])
                for part in ('body','lead-a','lead-b'):
                    paths = lambda c: [p.get('d') for g in artwork(c).iter() if g.get('data-part')==part for p in g.iter(f'{{{SVG}}}path')]
                    self.assertEqual(paths(config),paths(reference),config['key']+'/'+part)

    def test_marks_are_separate_editable_parts(self):
        for symbol in self.batch:
            variant = symbol['drawing']['variant']; parts = {p['id'] for p in symbol['parts']}
            if variant in ('ntc','ptc'): self.assertIn('temperature-mark', parts)
            if variant == 'nonlinear': self.assertIn('nonlinear-mark', parts)
            if variant.startswith('photo'): self.assertIn('light-arrows', parts)
            if variant == 'photo-enclosed': self.assertIn('enclosure', parts)
            if variant == 'tapped': self.assertNotIn('wiper-arrow', parts)
            for config in symbol['configurations']:
                actual = [p.get('data-part') for p in artwork(config).iter() if p.get('data-part')]
                self.assertEqual(set(actual), parts)
                self.assertEqual(len(actual),len(parts))


if __name__ == '__main__': unittest.main()
