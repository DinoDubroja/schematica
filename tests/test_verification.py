from support import APP
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from core import SVG, ValidationError, definitions
from exports import catalog, LIBRARY
from verification import apply_approvals, design_fingerprint, publication_catalog, read_ledger, source_fingerprint


class ApprovalWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.library = self.root / 'library'
        shutil.copytree(LIBRARY, self.library)
        shutil.copytree(APP / 'tex', self.root / 'tex')
        shutil.copy2(APP / 'presets.yaml', self.root / 'presets.yaml')
        self.sources = definitions()
        self.data = catalog()
        self.empty = {'schema_version': 1, 'approvals': {}}

    def publish(self, ledger=None):
        with patch('verification.ROOT', self.root):
            return publication_catalog(self.data, self.sources, self.library, ledger or self.empty)

    def handoff(self, data):
        symbol = data['symbols'][0]
        return {'schema_version': 1, 'library': 'schematica', 'approvals': [
            {'id': symbol['id'], 'revision': symbol['revision'], 'fingerprint': symbol['verification']['fingerprint']}]}

    def test_round_trip_and_idempotence(self):
        initial = self.publish()
        self.assertTrue(all(s['verification']['status'] == 'unverified' for s in initial['symbols']))
        ledger, changed = apply_approvals(self.handoff(initial), initial, self.empty)
        self.assertEqual(changed, [initial['symbols'][0]['id']])
        rebuilt = self.publish(ledger)
        self.assertEqual(rebuilt['symbols'][0]['verification']['status'], 'verified')
        same, changed = apply_approvals(self.handoff(rebuilt), rebuilt, ledger)
        self.assertEqual(same, ledger); self.assertEqual(changed, [])
        self.assertEqual(self.empty['approvals'], {})

    def test_invalid_handoffs_are_atomic(self):
        data = self.publish(); valid = self.handoff(data)
        for bad in ({'id':'unknown', 'revision':1, 'fingerprint':'x'},
                    {**valid['approvals'][0], 'revision':999},
                    {**valid['approvals'][0], 'fingerprint':'stale'}):
            payload = copy.deepcopy(valid); payload['approvals'] = [bad]
            with self.assertRaises(ValidationError): apply_approvals(payload, data, self.empty)
            self.assertEqual(self.empty['approvals'], {})
        for bad in ({'id':'unknown', 'revision':1, 'fingerprint':'x'}, valid['approvals'][0]):
            mixed = copy.deepcopy(valid); mixed['approvals'].append(bad)
            with self.assertRaises(ValidationError): apply_approvals(mixed, data, self.empty)
            self.assertEqual(self.empty['approvals'], {})

    def test_geometry_and_connections_invalidate_approval(self):
        data = self.publish(); handoff = self.handoff(data)
        ledger, _ = apply_approvals(handoff, data, self.empty)
        symbol = self.data['symbols'][0]; file = self.library / symbol['configurations'][0]['svg']
        tree = ET.parse(file); path = next(tree.getroot().iter(f'{{{SVG}}}path'))
        path.set('transform', 'translate(1,0)'); tree.write(file)
        rebuilt = self.publish(ledger)
        self.assertEqual(rebuilt['symbols'][0]['verification']['status'], 'unverified')
        with self.assertRaises(ValidationError): apply_approvals(handoff, rebuilt, ledger)
        before = design_fingerprint(symbol, self.library)
        symbol['configurations'][0]['pins_mm']['a'][0] += 1
        self.assertNotEqual(before, design_fingerprint(symbol, self.library))

    def test_editorial_edits_preserve_visual_approval(self):
        data = self.publish(); ledger, _ = apply_approvals(self.handoff(data), data, self.empty)
        source = next(s for s in self.sources if s['id'] == data['symbols'][0]['id'])
        source['description'] += ' Editorial correction.'; source['keywords'].append('corrected')
        for c in self.data['symbols'][0]['configurations']:
            file = self.library / c['svg']; tree = ET.parse(file)
            tree.getroot().find(f'{{{SVG}}}desc').text = source['description']; tree.write(file)
        rebuilt = self.publish(ledger)
        self.assertEqual(rebuilt['symbols'][0]['verification']['status'], 'verified')
        self.assertIn('corrected', rebuilt['symbols'][0]['keywords'])

    def test_stale_sources_cannot_publish_old_artwork(self):
        source = next(s for s in self.sources if s['id'] == self.data['symbols'][0]['id'])
        file = self.root / 'tex' / (source['recipe'] + '.tex')
        file.write_text(file.read_text(encoding='utf-8') + '\n% Changed drawing source\n', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, 'Stale artwork'): self.publish()

    def test_existing_accepted_designs_have_matching_official_records(self):
        published = publication_catalog(catalog(), definitions(), LIBRARY, read_ledger())
        approvals = read_ledger()['approvals']
        self.assertLessEqual(set(approvals), {s['id'] for s in published['symbols']})
        for symbol in published['symbols']:
            if symbol['id'] in approvals:
                self.assertEqual(symbol['verification']['status'], 'verified')
            else:
                self.assertEqual(symbol['verification']['status'], 'unverified')

    def test_options_and_nondefault_artwork_invalidate_approval(self):
        symbol = next(s for s in self.data['symbols'] if s.get('options'))
        source = next(s for s in self.sources if s['id'] == symbol['id'])
        initial = self.publish()
        published = next(s for s in initial['symbols'] if s['id'] == symbol['id'])
        handoff = {'schema_version':1, 'library':'schematica', 'approvals':[
            {'id':symbol['id'], 'revision':symbol['revision'], 'fingerprint':published['verification']['fingerprint']}]}
        ledger, _ = apply_approvals(handoff, initial, self.empty)
        config = next(c for c in symbol['configurations'] if c['options']['orientation']=='down-left')
        file = self.library / config['svg']; tree = ET.parse(file)
        next(tree.getroot().iter(f'{{{SVG}}}path')).set('transform', 'translate(.01,0)'); tree.write(file)
        changed = self.publish(ledger)
        with self.assertRaisesRegex(ValidationError, 'Stale approval'): apply_approvals(handoff, changed, ledger)
        before = design_fingerprint(symbol, self.library)
        symbol['options']['orientation']['default'] = 'down-left'
        self.assertNotEqual(before, design_fingerprint(symbol, self.library))
        source['options']['orientation']['default'] = 'down-left'
        with self.assertRaisesRegex(ValidationError, 'Stale artwork'): self.publish()

    def test_all_orientation_combinations_are_required(self):
        symbol = next(s for s in self.data['symbols'] if s.get('options'))
        symbol['configurations'].pop()
        with self.assertRaisesRegex(ValidationError, 'Incomplete configurations'): self.publish()


if __name__ == '__main__': unittest.main()
