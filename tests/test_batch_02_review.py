"""Regressions for the user's 14 November Batch 02 artwork review."""
from support import APP, FIXTURES
import hashlib
import json
import math
import re
import unittest

from core import SVG, ValidationError, definitions
from exports import LIBRARY, artwork, catalog
from recipe_registry import BATCH_MACROS, BATCH_LABEL_RECIPES
from verification import apply_approvals, publication_catalog, read_ledger
from test_batch_02 import NUMBER, straight_points


def parts(config):
    return {g.get('data-part'): g for g in artwork(config).iter() if g.get('data-part')}


def paths(group):
    return list(group.iter(f'{{{SVG}}}path'))


def part_hash(group):
    return hashlib.sha256(json.dumps([p.attrib for p in paths(group)], sort_keys=True).encode()).hexdigest()


class Batch02Review(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((FIXTURES/'batch-02-review.json').read_text(encoding='utf-8'))
        cls.data = publication_catalog(catalog(), definitions(), LIBRARY, read_ledger())
        cls.symbols = {s['id']: s for s in cls.data['symbols']}

    def configs(self, *ids):
        return [c for sid in ids for c in self.symbols[sid]['configurations']]

    def near(self, a, b):
        self.assertLess(math.dist(a, b), .0004, (a, b))

    def test_retained_inventory_removed_registrations_and_assets(self):
        original = json.loads((FIXTURES/'approved-before-batch-02.json').read_text())
        expected = set(original['approvals']) | {a['id'] for a in self.fixture['reviewed_approvals']} | set(self.fixture['changed']) | {'mosfet-p-enhancement-bulk'}
        self.assertEqual(set(self.symbols), expected)
        self.assertEqual(len(expected), 91)
        self.assertEqual(sum(len(s['configurations']) for s in self.symbols.values()), 1035)
        self.assertEqual({d['id'] for d in definitions()}, expected)
        for sid in self.fixture['removed']:
            self.assertNotIn(sid, BATCH_MACROS)
            self.assertNotIn(sid, BATCH_LABEL_RECIPES)
            self.assertFalse((APP/'definitions'/f'{sid}.yaml').exists())
            self.assertFalse((APP/'tex'/f'{sid}.tex').exists())
            self.assertFalse(list((LIBRARY/'svg').glob(sid+'-*.svg')))

    def test_approvals_exact_unchanged_artwork_and_replacement_identity(self):
        for relative, digest in self.fixture['unchanged_svg_sha256'].items():
            self.assertEqual(hashlib.sha256((LIBRARY/relative).read_bytes()).hexdigest(), digest, relative)
        verified = {s['id'] for s in self.symbols.values() if s['verification']['status']=='verified'}
        # The later 13-record handoff explicitly accepts every retained design.
        self.assertEqual(len(verified), 91)
        for approval in self.fixture['reviewed_approvals']:
            symbol = self.symbols[approval['id']]
            if symbol['id']=='logic-xor':
                with self.assertRaises(ValidationError):
                    apply_approvals({'schema_version':1,'library':'schematica','approvals':[approval]}, self.data, read_ledger())
            else:
                self.assertIn(symbol['id'], verified)
                self.assertEqual(symbol['revision'], approval['revision'])
                self.assertEqual(symbol['verification']['fingerprint'], approval['fingerprint'])
        for sid in self.fixture['changed']:
            self.assertEqual(self.symbols[sid]['revision'], 2)
            self.assertEqual(self.symbols[sid]['verification']['status'], 'verified')
        self.assertEqual(self.symbols['mosfet-p-enhancement-bulk']['revision'], 1)
        self.assertIn('mosfet-p-enhancement-bulk', verified)

    def test_jfet_bent_connections_source_side_gate_and_polarity(self):
        for sid, sign in [('jfet-n',1), ('jfet-p',-1)]:
            for c in self.configs(sid):
                p=parts(c);f=c['settings']['size_factor']
                channel=straight_points(paths(p['channel'])[0])
                self.near(channel[0], (0,-sign*f));self.near(channel[-1], (0,sign*5*f))
                ends={}
                for terminal in ('drain','source'):
                    lead=straight_points(paths(p['lead-'+terminal])[0])
                    self.assertEqual(len(lead),3)  # Vertical lead, real elbow, horizontal connection.
                    self.near(lead[0],c['pins_mm'][terminal])
                    self.assertGreater(lead[1][0],2*f)
                    self.assertAlmostEqual(lead[0][0],lead[1][0],delta=.0004)
                    self.assertAlmostEqual(lead[-1][0],0,delta=.0004)
                    ends[terminal]=lead[-1]
                gate=straight_points(paths(p['lead-gate'])[0])
                self.near(gate[-1],ends['source'])
                self.assertGreater(sign*(ends['drain'][1]-ends['source'][1]),3.9*f)
                arrow=straight_points(paths(p['gate-arrow'])[0])
                middle=tuple((a+b)/2 for a,b in zip(arrow[0],arrow[2]))
                self.assertGreater(sign*(arrow[1][0]-middle[0]),0)
                self.near(arrow[1] if sign==1 else middle, gate[-1])
                for xy in c['pins_mm'].values():
                    self.assertTrue(all(abs(v-round(v))<.0001 for v in xy))

    def test_mosfet_dots_removed_without_changing_other_parts(self):
        ids=[sid for sid in self.symbols if sid.startswith('mosfet-')]
        self.assertEqual(len(ids),6)
        for c in self.configs(*ids):
            p=parts(c)
            # Only straight line/triangle paths: no filled circular Bezier or circle element.
            self.assertFalse(list(artwork(c).iter(f'{{{SVG}}}circle')))
            for group in p.values():
                for path in paths(group):self.assertNotRegex(path.get('d'),r'[CcAa]')
            if c['symbol_id'].endswith('-bulk'):continue
            before=self.fixture['before_changed'][c['key']]
            self.assertEqual(len(paths(p['body-source-link'])),1)
            self.assertEqual(paths(p['body-source-link'])[0].attrib,before['body_source_line'])
            self.assertEqual(c['pins_mm'],before['pins_mm'])
            for name,group in p.items():
                if name!='body-source-link':self.assertEqual(part_hash(group),before['part_hashes'][name],c['key']+'/'+name)

    def test_bjt_fixed_one_mm_shift_and_arrow_at_branch_end(self):
        for c in self.configs('transistor-npn','transistor-pnp','phototransistor-npn'):
            p=parts(c);old=self.fixture['before_changed'][c['key']]
            for terminal in ('collector','emitter'):
                branch=straight_points(paths(p[terminal+'-branch'])[0])
                prior=old['branches'][terminal+'-branch']
                self.near(branch[0],prior[0])
                self.near(branch[-1],(prior[-1][0]-1,prior[-1][1]))
                self.near(c['pins_mm'][terminal],(old['pins_mm'][terminal][0]-1,old['pins_mm'][terminal][1]))
                lead=straight_points(paths(p['lead-'+terminal])[0])
                self.near(lead[0],c['pins_mm'][terminal]);self.near(lead[-1],branch[-1])
            for name in ('base','lead-base','enclosure','light-arrows'):
                if name in p:self.assertEqual(part_hash(p[name]),old['part_hashes'][name])
            if 'base' in c['pins_mm']:self.assertEqual(c['pins_mm']['base'],old['pins_mm']['base'])
            branch=straight_points(paths(p['emitter-branch'])[0])
            arrow=straight_points(paths(p['emitter-arrow'])[0])
            midpoint=tuple((a+b)/2 for a,b in zip(arrow[0],arrow[2]))
            pnp=c['symbol_id']=='transistor-pnp'
            self.near(midpoint if pnp else arrow[1],branch[-1])
            axis=[arrow[1][i]-midpoint[i] for i in (0,1)]
            direction=[branch[-1][i]-branch[0][i] for i in (0,1)]
            self.assertAlmostEqual(axis[0]*direction[1]-axis[1]*direction[0],0,delta=.002)
            dot=sum(a*b for a,b in zip(axis,direction))
            self.assertGreater(-dot if pnp else dot,0)

    def test_chassis_bar_meets_outer_hatches_with_butt_caps(self):
        for c in self.configs('ground-chassis'):
            bar,*hatches=paths(parts(c)['ground-mark'])
            ends=straight_points(bar)
            self.near(ends[0],straight_points(hatches[0])[0])
            self.near(ends[-1],straight_points(hatches[-1])[0])
            self.assertEqual(bar.get('stroke-linecap'),'butt')

    def test_xor_input_ends_on_actual_outer_bezier(self):
        for c in self.configs('logic-xor','logic-xnor'):
            p=parts(c);old=self.fixture['before_changed'][c['key']]
            for name in ('body','exclusive-mark','inversion','lead-out'):
                if name in p:self.assertEqual(part_hash(p[name]),old['part_hashes'][name])
            self.assertEqual(c['pins_mm'],old['pins_mm'])
            curve=paths(p['exclusive-mark'])[0]
            coords=[float(n)*25.4/72.27 for n in re.findall(NUMBER,curve.get('d'))]
            self.assertEqual(len(coords),8)
            points=list(zip(coords[::2],coords[1::2]))
            def at(t):
                return [sum(w*p[i] for w,p in zip(((1-t)**3,3*t*(1-t)**2,3*t*t*(1-t),t**3),points)) for i in (0,1)]
            for name in ('lead-a','lead-b'):
                lead=straight_points(paths(p[name])[0]);self.assertEqual(len(lead),2)
                lo,hi=0.,1.
                for _ in range(45):
                    mid=(lo+hi)/2
                    if at(mid)[1]<lead[-1][1]:lo=mid
                    else:hi=mid
                self.near(lead[-1],at((lo+hi)/2))
                self.assertLess(lead[0][0],lead[-1][0])
            # No white/background masks; the unwanted lead segments really ended.
            self.assertFalse(list(artwork(c).iter(f'{{{SVG}}}rect')))


if __name__=='__main__':unittest.main()
