"""Independent PDF geometry measurements and Inkscape serialization checks."""
from __future__ import annotations
import json
import math
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import fitz

from core import ROOT, SVG, INK, BP_MM, tool, run, validate_svg_references


def segments(drawings, center=None):
    lines, widths = [], []
    for drawing in drawings:
        if drawing["type"] != "s":
            continue
        widths.append(drawing["width"] * BP_MM)
        first, last = None, None
        for item in drawing["items"]:
            if item[0] == "l":
                a, b = item[1:3]
                first = first or a
                last = b
                lines.append((tuple(a), tuple(b)))
            elif item[0] == "re":
                rect = item[1]
                points = [rect.tl, rect.tr, rect.br, rect.bl, rect.tl]
                lines.extend((tuple(a), tuple(b)) for a, b in zip(points, points[1:]))
            elif item[0] == "c":
                points = item[1:]
                first = first or points[0]
                last = points[-1]
                lines.append(tuple(tuple(p) for p in points))
            else:
                raise AssertionError(f"Unexpected geometry {item[0]}")
        if drawing.get("closePath") and first and last and first != last:
            lines.append((tuple(last), tuple(first)))
    points = [p for line in lines for p in line]
    if center is None:
        center = ((min(p[0] for p in points)+max(p[0] for p in points))/2,
                  (min(p[1] for p in points)+max(p[1] for p in points))/2)
    normalized = []
    for line in lines:
        points = tuple(((a[0]-center[0])*BP_MM, (a[1]-center[1])*BP_MM) for a in line)
        normalized.append(min(points, tuple(reversed(points))))
    return normalized, widths


def nearest_error(actual, expected):
    assert len(actual) == len(expected), (len(actual), len(expected))
    unmatched = list(expected)
    error = 0
    for line in actual:
        def distance(other):
            if len(line) != len(other):
                return float("inf")
            return max(abs(a-b) for p,q in zip(line, other) for a,b in zip(p,q))
        best = min(unmatched, key=distance)
        error = max(error, distance(best))
        unmatched.remove(best)
    return error


def verify():
    review = ROOT / "review"
    work = ROOT / "build/verification"
    work.mkdir(parents=True, exist_ok=True)
    palette = fitz.open(ROOT / "references/accepted-palette/preset-comparison-10mm-shorter-opamp.pdf")
    drawings = [d for d in palette[0].get_drawings() if d["color"] and max(d["color"]) < 0.01]
    first_body = drawings[0]["rect"]
    origin = ((first_body.x0+first_body.x1)/2, (first_body.y0+first_body.y1)/2)
    rows = [(0,"small","medium"), (23,"medium","medium"), (46,"large","medium"),
            (80,"medium","thin"), (103,"medium","medium"), (126,"medium","thick"), (160,"small","thick")]
    fidelity = []
    for symbol, offset in (("resistor-eu",0), ("opamp-supply",140)):
        for y, size, stroke in rows:
            cx, cy = origin[0]+offset/BP_MM, origin[1]+y/BP_MM
            rect = fitz.Rect(cx-12/BP_MM, cy-10/BP_MM, cx+12/BP_MM, cy+10/BP_MM)
            reference = [d for d in drawings if rect.contains(d["rect"])]
            expected, expected_widths = segments(reference, (cx,cy))
            source = review / "configurations" / f"{symbol}-{size}-{stroke}.svg"
            pdf = work / f"{symbol}-{size}-{stroke}.pdf"
            run([tool("inkscape"), str(source), f"--export-filename={pdf}"], work)
            document = fitz.open(pdf)
            actual, actual_widths = segments(document[0].get_drawings())
            deviation = nearest_error(actual, expected)
            stroke_error = max(abs(a-b) for a in actual_widths for b in expected_widths)
            # Cairo PDF serialization quantizes coordinates; use a 5 micrometre
            # tolerance for this independent round-trip comparison.
            assert deviation < 0.005, (source.name, deviation)
            assert stroke_error < 0.001, (source.name, stroke_error)
            fidelity.append({"configuration": source.stem, "max_coordinate_deviation_mm": deviation,
                             "max_stroke_deviation_mm": stroke_error})
    # Prove named-part targeting through Inkscape, save, open and export again.
    source = review / "configurations/opamp-supply-small-thick.svg"
    original = ET.parse(source).getroot()
    body = next(p for p in original.iter() if p.get("data-part") == "body")
    edited = review / "parts-saved.svg"
    actions = f"select-by-id:{body.get('id')};object-set-attribute:data-edit-proof,selected-in-inkscape;export-filename:{edited};export-do"
    run([tool("inkscape"), str(source), f"--actions={actions}"], work)
    saved = ET.parse(edited).getroot()
    validate_svg_references(saved)
    parts = {p.get("data-part"): p for p in saved.iter() if p.get("data-part")}
    assert len(parts) == 8
    assert parts["body"].get("data-edit-proof") == "selected-in-inkscape"
    assert all(p.get(f"{{{INK}}}label") == pid for pid,p in parts.items())
    reopened = review / "parts-reopened.svg"
    run([tool("inkscape"), str(edited), f"--export-filename={reopened}"], work)
    again = ET.parse(reopened).getroot()
    assert {p.get("data-part") for p in again.iter() if p.get("data-part")} == set(parts)
    run([tool("inkscape"), str(reopened), f"--export-filename={review / 'parts-reopened.png'}", "--export-width=800"], work)
    # Repeated symbols and all their references must survive Inkscape serialization.
    run([tool("inkscape"), str(review / "repeated.svg"), f"--export-filename={review / 'repeated-saved.svg'}"], work)
    validate_svg_references(ET.parse(review / "repeated-saved.svg").getroot())
    results = {"palette_comparisons": fidelity, "max_coordinate_deviation_mm": max(r["max_coordinate_deviation_mm"] for r in fidelity),
        "max_stroke_deviation_mm": max(r["max_stroke_deviation_mm"] for r in fidelity),
        "named_part_selection_save_reopen": "passed", "repeated_ids_after_save": "passed"}
    (review / "verification.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    verify()
