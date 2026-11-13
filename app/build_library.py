"""Render complete designs into a candidate library for validation before promotion."""
import argparse
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from core import ROOT, SVG, BP_MM, definitions, get_definition, render_symbol, read_yaml, configuration_choices, configuration_key
from verification import source_fingerprint

ORDER = ("resistor-eu", "resistor-us", "inductor-coil", "capacitor", "opamp", "opamp-supply")


def build(output=None, selected=None):
    library = Path(output or ROOT / "build/candidates/current").resolve()
    if library == (ROOT / "library").resolve():
        raise ValueError("Build candidates separately; promote only after technical and visual checks.")
    (library / "svg").mkdir(parents=True, exist_ok=True)
    presets = read_yaml(ROOT / "presets.yaml")
    entries = {d["id"]: d for d in definitions()}
    data = {"schema_version": 1, "presets": presets, "symbols": []}
    timings = []
    failures = []
    order = [sid for sid in ORDER if sid in entries] + sorted(set(entries) - set(ORDER))
    if selected:
        unknown = set(selected) - set(entries)
        if unknown:
            raise ValueError(f"Unknown designs: {unknown}")
        order = [sid for sid in order if sid in selected]
    for sid in order:
        entry = dict(entries[sid], configurations=[])
        started_from = source_fingerprint(entry)
        reports = []
        try:
            for size, stroke, options in configuration_choices(entry):
                reports.append(render_symbol(sid, size, stroke, options=options))
            if source_fingerprint(get_definition(sid)) != started_from:
                raise ValueError("Drawing sources changed during rendering; rebuild this design")
        except Exception as error:
            failures.append({"id": sid, "error": str(error)})
            print(f"Excluded {sid}: {error}", flush=True)
            continue
        for report in reports:
            size, stroke = report["settings"]["size"], report["settings"]["stroke"]
            key = configuration_key(sid, size, stroke, report["settings"].get("options"))
            path = library / "svg" / f"{key}.svg"
            shutil.copy2(report["output"], path)
            timings.append({**report, "output": str(path)})
            root = ET.parse(path).getroot()
            meta = json.loads(root.find(f"{{{SVG}}}metadata").text)
            vb = [float(v) for v in root.get("viewBox").split()]
            ox, oy = meta["origin_svg"]
            entry["configurations"].append({"key": key, "symbol_id": sid, "name": entry["name"],
                "revision": entry["revision"], "size": size, "stroke": stroke,
                "svg": f"svg/{key}.svg", "width_mm": float(root.get("width")[:-2]),
                "height_mm": float(root.get("height")[:-2]), "origin_svg": [ox,oy],
                "visual_center_from_origin_mm": [(vb[0]+vb[2]/2-ox)*BP_MM, (vb[1]+vb[3]/2-oy)*BP_MM],
                "pins_mm": report["pins_mm"], "dimensions_mm": report["dimensions_mm"],
                "parts": report["parts"], "svg_bytes": report["svg_bytes"],
                "settings": report["settings"]})
            if report["settings"].get("options"):
                entry["configurations"][-1]["options"] = report["settings"]["options"]
        entry["source_fingerprint"] = started_from
        data["symbols"].append(entry)
        print(f"Built {sid}: {len(reports)} configurations", flush=True)
    (library / "catalog.json").write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    report_path = ROOT / "build/library-measurements.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({"renders": timings, "excluded": failures}, indent=2)+"\n", encoding="utf-8")
    items = [c for s in data["symbols"] for c in s["configurations"]]
    print(json.dumps({"configurations":len(items),"compile_seconds":sum(t["compile_seconds"] for t in timings),
        "convert_seconds":sum(t["convert_seconds"] for t in timings), "excluded": failures},indent=2))
    return bool(failures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--symbols", nargs="+", help="Render only these designs into a separate candidate catalog")
    args = parser.parse_args()
    raise SystemExit(1 if build(args.output, args.symbols) else 0)
