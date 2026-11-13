"""Check saved GUI evidence, physical placement, clipping and tight clearances.

Run after the documented manual Inkscape checks have produced the evidence files.
This script validates those files; it does not claim to perform the GUI actions.
"""
import json
import math
import xml.etree.ElementTree as ET

import fitz

from core import ROOT, SVG, INK, BP_MM, tool, run, validate_svg_references
from verify_render import segments, nearest_error


def point_segment_distance(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy)


def segment_distance(a, b):
    # These known fixture segments do not intersect; check that premise below.
    def side(p, q, r):
        return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    if side(*a, b[0])*side(*a, b[1]) < 0 and side(*b, a[0])*side(*b, a[1]) < 0:
        return 0
    return min(*(point_segment_distance(p, *b) for p in a),
               *(point_segment_distance(p, *a) for p in b))


def verify():
    review = ROOT / "review"
    work = ROOT / "build/verification"
    work.mkdir(parents=True, exist_ok=True)
    expected = {"body", "lead-in-plus", "lead-in-minus", "lead-out", "sign-plus",
                "sign-minus", "lead-supply-plus", "lead-supply-minus"}
    for name in ("symbols-placed", "symbols-unlinked", "symbols-reopened"):
        root = ET.parse(review / f"{name}.svg").getroot()
        validate_svg_references(root)
        if name != "symbols-placed":
            layer = next(g for g in root.findall(f"{{{SVG}}}g") if g.get(f"{{{INK}}}groupmode") == "layer")
            parts = [p for p in layer.iter() if p.get("data-part")]
            assert len(parts) == 8 and {p.get("data-part") for p in parts} == expected
            assert all(p.get(f"{{{INK}}}label") == p.get("data-part") for p in parts)
            assert not list(layer.iter(f"{{{SVG}}}use"))
        run([tool("inkscape"), str(review / f"{name}.svg"), f"--export-filename={work / (name+'.pdf')}"], work)
    original = fitz.open(work / "opamp-supply-medium-medium.pdf")
    expected_lines, expected_widths = segments(original[0].get_drawings())
    placement = []
    for name in ("symbols-placed", "symbols-unlinked", "symbols-reopened"):
        document = fitz.open(work / f"{name}.pdf")
        lines, widths = segments(document[0].get_drawings())
        error = nearest_error(lines, expected_lines)
        assert error < 0.005
        assert max(abs(a-b) for a in widths for b in expected_widths) < 0.001
        placement.append({"file": f"{name}.svg", "max_geometry_deviation_mm": error})
    label = ET.parse(review / "editable-label-reopened.svg").getroot()
    assert ["".join(t.itertext()) for t in label.iter(f"{{{SVG}}}text")] == ["Label B"]
    original_strings = json.loads((review / "editable-label.strings.json").read_text())
    assert original_strings["label"] == "Label A"
    margins = []
    for path in sorted((review / "configurations").glob("*.svg")):
        root = ET.parse(path).getroot()
        group = root.find(f"{{{SVG}}}g")
        _, output = run([tool("inkscape"), str(path), "--query-all"], work)
        bounds = next(line.split(",")[1:] for line in output.splitlines() if line.startswith(group.get("id")+","))
        x, y, width, height = [float(v)*25.4/96 for v in bounds]
        page_width, page_height = [float(root.get(k).removesuffix("mm")) for k in ("width", "height")]
        margin = min(x, y, page_width-x-width, page_height-y-height)
        assert margin > 0.9, (path.name, margin)
        margins.append({"file": path.name, "minimum_page_margin_mm": margin})
    small = fitz.open(work / "opamp-supply-small-thick.pdf")
    drawings = small[0].get_drawings()
    # SVG order is body, three signal leads, plus, minus, two supply leads.
    assert len(drawings) == 8
    body, _ = segments([drawings[0]], (0, 0))
    signs, _ = segments(drawings[4:6], (0, 0))
    gap = min(segment_distance(a, b) for a in body for b in signs) - drawings[0]["width"]*BP_MM
    assert gap > 0.3, gap
    run([tool("inkscape"), str(review / "symbols-reopened.svg"), "--export-area-drawing",
         f"--export-filename={review / 'symbols-reopened.png'}", "--export-width=800"], work)
    report = {"saved_gui_evidence": "validated; GUI actions documented separately in CHECKPOINT.md",
              "placement_geometry": placement, "unlinked_named_parts": sorted(expected),
              "editable_text_after_reopen": "Label B", "preserved_original_text": "Label A",
              "configuration_margins": margins, "small_thick_opamp_sign_to_body_clearance_mm": gap}
    (review / "inkscape-checks.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    verify()
