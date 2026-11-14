from support import APP, FIXTURES
import copy
import json
import tempfile
import unittest
from unittest.mock import patch

from core import ROOT, ValidationError
from agent_store import initialize, Store, checked_root
from agent_service import AgentService
from creation import Creation
from custom_renderer import validate_custom


INTENT = {"meaning": "ground", "elements": "bars and lead", "terminals": "one, a", "labels": "none", "options": "full or compact bars"}


class AgentTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "build").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "build", prefix="agent-test-")
        initialize(self.temp.name)
        self.service = AgentService(self.temp.name)
        self.creation = Creation(self.service)

    def tearDown(self):
        self.temp.cleanup()

    def test_natural_search_and_followups(self):
        first = self.service.search("Show me normal resistor symbols you have.")
        self.assertEqual(first["match_ids"], ["resistor-eu", "resistor-us"])
        sid = first["session_id"]
        eu = self.service.search("Only European ones.", sid)
        self.assertEqual(eu["match_ids"], ["resistor-eu"])
        variable = self.service.search("Show variable ones instead.", sid)
        self.assertEqual(variable["match_ids"], ["resistor-variable-eu"])
        thick = self.service.search("Use a thicker stroke.", sid)
        self.assertEqual(thick["match_ids"], variable["match_ids"])
        self.assertEqual(thick["filters"]["stroke"], "thick")
        self.assertEqual(self.service.search("Browse the whole library.", sid)["count"], len(self.service.catalog()["symbols"]))

    def test_unknown_search_never_substitutes_or_creates(self):
        result = self.service.search("quantum unicorn")
        self.assertEqual(result["count"], 0)
        self.assertIn("viewer_url", result)
        self.assertEqual(self.service.store.current_versions(), [])

    def test_integrated_families_clear_unrelated_followup_filters(self):
        session = self.service.search("normal European resistors")["session_id"]
        capacitors = self.service.search("variable capacitors", session)
        self.assertEqual(capacitors["match_ids"], ["capacitor-variable"])
        self.assertNotIn("style", capacitors["filters"])
        diodes = self.service.search("Show me diodes", session)
        self.assertEqual(set(diodes["match_ids"]), {"diode", "diode-led", "diode-photo", "diode-schottky",
            "diode-tvs-bidirectional", "diode-varactor", "diode-zener"})
        self.assertNotIn("variant", diodes["filters"])

    def test_filters_reject_wrong_types(self):
        for filters in ({"style": "martian"}, {"ids": "resistor-eu"}, {"size": []}, {"mystery": "x"}):
            with self.assertRaises(ValidationError):
                self.service.search(filters=filters)

    def test_selection_is_exact_and_persists(self):
        session = self.service.search("variable resistors")
        choice = self.service.select("resistor-variable-eu", 2, "small", "thick", {"orientation": "down-left"}, session["session_id"])
        self.assertIn("down-left", choice["configuration"]["key"])
        restarted = AgentService(self.temp.name)
        self.assertEqual(restarted.search_result(session["session_id"])["selection"], choice)
        self.assertTrue(restarted.asset(choice["asset"]).startswith(b"<?xml"))
        with self.assertRaises(ValidationError):
            self.service.select("resistor-variable-eu", 1)
        with self.assertRaises(ValidationError):
            self.service.select("resistor-eu", 1, options={"fictional": "x"})

    def test_store_cannot_target_source_or_other_checkouts(self):
        for path in (ROOT / "library", ROOT.parent.parent / "other/app/build/test", ROOT / "build/../library"):
            with self.assertRaises(ValidationError):
                checked_root(path)

    def test_store_does_not_adopt_existing_data(self):
        target = ROOT / "build" / "agent-test-occupied"
        target.mkdir(exist_ok=True)
        (target / "keep.txt").write_text("keep")
        with self.assertRaises(ValidationError):
            initialize(target)
        self.assertEqual((target / "keep.txt").read_text(), "keep")
        (target / "keep.txt").unlink()
        target.rmdir()

    def test_assets_reject_traversal_and_unlisted_files(self):
        for asset in ("../verification.json", "base/../verification.json", "state.sqlite3"):
            with self.assertRaises(ValidationError):
                self.service.asset(asset)

    def test_description_and_confirmation_are_required(self):
        with self.assertRaisesRegex(ValidationError, "textual description"):
            self.creation.prepare("", INTENT)
        draft = self.creation.prepare("ground", INTENT)
        with patch("creation.render_all") as renderer:
            with self.assertRaises(ValidationError):
                self.creation.render(draft["draft_id"], "invented", {}, "", [])
            renderer.assert_not_called()
        with self.assertRaises(ValidationError):
            self.creation.confirm(draft["draft_id"], "stale", "yes")
        confirmed = self.creation.confirm(draft["draft_id"], draft["interpretation_digest"], "Yes, use that interpretation.")
        self.assertTrue(confirmed["confirmation_token"])
        self.assertEqual(self.service.store.current_versions(), [])

    def test_unresolved_questions_block_generation(self):
        draft = self.creation.prepare("ground", INTENT, uncertainties=["Which terminal?"])
        with self.assertRaisesRegex(ValidationError, "uncertainties"):
            self.creation.confirm(draft["draft_id"], draft["interpretation_digest"], "yes")

    def test_reference_image_validation(self):
        draft = self.creation.prepare("ground sketch", INTENT)
        with self.assertRaises(ValidationError):
            self.creation.attach_image(draft["draft_id"], "sketch", "image/png", "c2VjcmV0")

    def test_custom_options_and_tex_are_validated(self):
        definition = json.loads((FIXTURES / "individual-ground.json").read_text())
        recipe = (FIXTURES / "individual-ground.tex").read_text()
        validate_custom(definition, recipe)
        for extra in (r"\input{private}", r"\write18{command}", r"\special{raw code}", r"\csname input\endcsname", "^^5cinput"):
            with self.assertRaises(ValidationError):
                validate_custom(definition, recipe + extra)
        bad = copy.deepcopy(definition)
        bad["options"]["bars"]["affected_parts"] = ["missing"]
        with self.assertRaises(ValidationError):
            validate_custom(bad, recipe)

    def test_revisions_are_immutable_and_conflicts_rejected(self):
        self.service.store.save_version({"id": "demo", "revision": 1}, None)
        self.service.store.save_version({"id": "demo", "revision": 2}, 1)
        self.assertEqual(self.service.store.version("demo", 1)["revision"], 1)
        with self.assertRaises(ValidationError):
            self.service.store.save_version({"id": "demo", "revision": 3}, 1)


if __name__ == "__main__":
    unittest.main()
