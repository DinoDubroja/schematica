import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core


class DefinitionFailures(unittest.TestCase):
    def setUp(self):
        self.definition = core.get_definition("opamp-supply")
        self.presets = core.read_yaml(core.ROOT / "presets.yaml")

    def test_duplicate_yaml_key(self):
        with self.assertRaises(core.ValidationError):
            core.yaml.load("id: a\nid: b\n", Loader=core.UniqueLoader)

    def test_duplicate_parts(self):
        self.definition["parts"].append(self.definition["parts"][0])
        with self.assertRaises(core.ValidationError):
            core.validate_definition(self.definition, self.presets)

    def test_unknown_lead(self):
        self.definition["pins"][0]["lead_part"] = "missing"
        with self.assertRaises(core.ValidationError):
            core.validate_definition(self.definition, self.presets)

    def test_missing_unknown_duplicate_emitted_part(self):
        source = Path(__file__).parent / "fixtures/opamp-supply.scmeta"
        content = source.read_text()
        for modified in (content.replace("part|body\n", ""), content+"part|unknown\n", content+"part|body\n"):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "metadata"
                path.write_text(modified)
                with self.assertRaises(core.ValidationError):
                    core.parse_metadata(path, self.definition)

    def test_unlisted_presets(self):
        with self.assertRaises(core.ValidationError):
            core.resolve_settings(self.definition, "tiny", "medium")

    def test_svg_reference_namespace(self):
        root = ET.fromstring(f'<svg xmlns="{core.SVG}"><defs><clipPath id="clip"/></defs><g id="body" clip-path="url(#clip)"/><use href="#body"/></svg>')
        core.namespace_ids(root, "copy-a")
        core.validate_svg_references(root)
        self.assertEqual(root[-1].get("href"), "#copy-a--body")
        root[-1].set("href", "#missing")
        with self.assertRaises(core.ValidationError):
            core.validate_svg_references(root)


class RenderProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = json.loads((core.ROOT / "library/catalog.json").read_text())
        cls.reports = [dict(c, output=core.ROOT / 'library' / c['svg'])
                       for s in catalog['symbols'] if s['id'] in ('resistor-eu', 'opamp-supply')
                       for c in s['configurations']]

    def test_accepted_dimensions_and_grid(self):
        for r in self.reports:
            s = r["settings"]["size"]
            if r["symbol_id"] == "resistor-eu":
                width, terminal = {"small": (7.5, 7), "medium": (10, 8), "large": (12.5, 10)}[s]
                self.assertAlmostEqual(r["dimensions_mm"]["body-width"], width, delta=0.0001)
                self.assertEqual(r["pins_mm"], {"a": [-terminal, 0], "b": [terminal, 0]})
            else:
                end, supply = {"small": (8, 5), "medium": (9, 6), "large": (11, 7)}[s]
                self.assertEqual(r["pins_mm"], {"in-plus": [-end,3], "in-minus": [-end,-3], "out": [end,0], "supply-plus": [0,supply], "supply-minus": [0,-supply]})

    def test_stroke_does_not_change_geometry(self):
        for symbol in ("resistor-eu", "opamp-supply"):
            for size in ("small", "medium", "large"):
                records = [r for r in self.reports if r["symbol_id"] == symbol and r["settings"]["size"] == size]
                for record in records[1:]:
                    self.assertEqual(record["pins_mm"], records[0]["pins_mm"])
                    self.assertEqual(record["dimensions_mm"], records[0]["dimensions_mm"])
                paths = []
                for record in records:
                    root = ET.parse(record["output"]).getroot()
                    paths.append([e.get("d") for e in root.iter(f"{{{core.SVG}}}path")])
                    group = root.find(f"{{{core.SVG}}}g")
                    width = float(group.get("stroke-width")) * 25.4 / 72.27
                    self.assertAlmostEqual(width, record["settings"]["stroke_mm"], delta=0.00001)
                self.assertEqual(paths[0], paths[1])
                self.assertEqual(paths[1], paths[2])

    def test_shallow_named_parts_and_repeated_ids(self):
        for r in self.reports:
            root = ET.parse(r["output"]).getroot()
            group = root.find(f"{{{core.SVG}}}g")
            self.assertEqual({p.get("data-part") for p in group}, set(r["parts"]))
            self.assertTrue(all(not p.findall(f"{{{core.SVG}}}g") for p in group))
        for file in ("repeated.svg", "symbols.svg"):
            core.validate_svg_references(ET.parse(core.ROOT / "review" / file).getroot())


if __name__ == "__main__":
    unittest.main()
