"""Batch scope and electrical contracts; no rendering or live service writes."""
from support import APP
import collections
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

from core import configuration_choices
from custom_renderer import validate_custom

BATCH = APP / 'batches/batch-03'
read = lambda path: json.loads(path.read_text(encoding='utf-8'))
ROWS = read(BATCH / 'manifest.json')['targets']
DEFINITIONS = {r['id']: read(BATCH / 'symbols' / r['id'] / 'definition.json') for r in ROWS}
GROUPS = {'Data conversion': 6, 'Filters': 6, 'Signal processing': 8,
          'Digital building blocks': 10, 'RF': 8, 'Optoelectronics': 8,
          'Power semiconductors': 6, 'Transducers and basic motors': 6,
          'Additional transistor styles': 12, 'Additional motors': 4,
          'Generators': 2, 'Relays and contactors': 6, 'Pushbuttons': 2}


class Batch03Tests(unittest.TestCase):
    def test_complete_scoped_inventory_stays_out_of_public_library(self):
        self.assertEqual(len(ROWS), 84)
        self.assertEqual(len(DEFINITIONS), 84)
        self.assertEqual(dict(collections.Counter(r['group'] for r in ROWS)), GROUPS)
        self.assertEqual({p.name for p in (BATCH / 'symbols').iterdir()}, set(DEFINITIONS))
        published = {s['id'] for s in read(APP / 'library/catalog.json')['symbols']}
        self.assertFalse(published & set(DEFINITIONS))

    def test_sources_validate_with_independent_size_and_stroke(self):
        total = 0
        for id, definition in DEFINITIONS.items():
            with self.subTest(symbol=id):
                recipe = (BATCH / 'symbols' / id / 'custom.tex').read_text(encoding='utf-8')
                validate_custom(definition, recipe)
                self.assertEqual(definition['id'], id)
                self.assertEqual(definition['batch'], 'Batch 03')
                choices = configuration_choices(definition)
                self.assertEqual({(s, w) for s, w, _ in choices},
                                 {(s, w) for s in ('small', 'medium', 'large') for w in ('thin', 'medium', 'thick')})
                self.assertEqual(len(choices), 27 if id in ('bandpass-two-port', 'filter-band-pass-tunable') else 9)
                self.assertTrue(definition.get('reference') or definition.get('lineage'))
                total += len(choices)
        self.assertEqual(total, 792)

    def test_electrically_distinct_terminal_contracts(self):
        counts = {'adc-single-ended': 2, 'adc-differential-n-bit': 3,
                  'diac': 2, 'triac': 3, 'thyristor-scr': 3, 'bridge-rectifier': 4,
                  'led-bicolour-2pin': 2, 'led-bicolour-common-anode': 3,
                  'motor-stepper-bipolar': 4, 'motor-stepper-unipolar': 6,
                  'relay-coil': 2, 'relay-spst-no': 4, 'relay-spst-nc': 4,
                  'relay-spdt': 5, 'relay-dpdt': 8, 'contactor-3pole': 8,
                  'pushbutton-no': 2, 'pushbutton-nc': 2}
        for id, count in counts.items():
            self.assertEqual(len(DEFINITIONS[id]['pins']), count, id)
        for id in ('motor-bldc', 'motor-ac-3phase'):
            self.assertEqual({p['id'] for p in DEFINITIONS[id]['pins']}, {'u', 'v', 'w'})
        self.assertEqual({p['id'] for p in DEFINITIONS['motor-stepper-unipolar']['pins']},
                         {'a1', 'a2', 'a0', 'b1', 'b2', 'b0'})

    def test_accepted_parent_and_draft_lineage_are_retained(self):
        pnp = DEFINITIONS['transistor-pnp-enclosed']['lineage']
        self.assertEqual(pnp['revision_id'], 'aade4544-ddc3-50f3-b89e-6510eb114858')
        self.assertIs(pnp['internal_drawing_changes'], False)
        for id in ('adc-differential-n-bit', 'bandpass-two-port'):
            lineage = DEFINITIONS[id]['lineage']
            self.assertIs(lineage['drawing_changes'], False)
            self.assertIs(lineage['human_verified'], False)
            self.assertTrue(lineage['render_id'])
        for id, d in DEFINITIONS.items():
            if id.startswith('mosfet-') and id.endswith('-enclosed'):
                self.assertIs(d['lineage']['internal_drawing_changes'], False)
                self.assertEqual('terminal_change' in d['lineage'], '-bulk-' in id)

    def test_manifest_has_immutable_submitted_revisions_without_approval(self):
        identities = set()
        for row in ROWS:
            self.assertEqual(row['status'], 'submitted')
            self.assertEqual(uuid.UUID(row['revision_id']).version, 5)
            self.assertRegex(row['fingerprint'], r'^[a-f0-9]{64}$')
            self.assertEqual(row['configurations'], len(configuration_choices(DEFINITIONS[row['id']])))
            self.assertNotIn('verification', row)
            self.assertNotIn('approved', row)
            identities.add(row['revision_id'])
        self.assertEqual(len(identities), 84)

    def test_submit_rejects_a_render_from_different_source_before_upload(self):
        spec = importlib.util.spec_from_file_location('batch03_runner', BATCH / 'run.py')
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, 'Client') as client:
            client.return_value.state.return_value = {'symbols': {}}
            target = Path(directory)
            (target / 'symbol.json').write_text('{"revision":1}', encoding='utf-8')
            (target / 'technical.json').write_text('{"source_sha256":"stale"}', encoding='utf-8')
            with self.assertRaisesRegex(AssertionError, 'Render current source'):
                runner.submit('relay-coil', target, {}, 'Actual inspection note')
            client.return_value.upload.assert_not_called()


if __name__ == '__main__':
    unittest.main()
