"""Generate the approved six appearances and their 54 preset combinations."""
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from core import ROOT, SVG, BP_MM, definitions, render_symbol, read_yaml, write_svg
from exports import LIBRARY

ORDER = ("resistor-eu", "resistor-us", "inductor-coil", "capacitor", "opamp", "opamp-supply")


def build():
    (LIBRARY / "svg").mkdir(parents=True, exist_ok=True)
    presets = read_yaml(ROOT / "presets.yaml")
    entries = {d["id"]: d for d in definitions()}
    data = {"schema_version": 1, "presets": presets, "symbols": []}
    timings = []
    for sid in ORDER:
        entry = dict(entries[sid], configurations=[])
        for size in presets["sizes"]:
            for stroke in presets["strokes"]:
                report = render_symbol(sid, size, stroke)
                key = f"{sid}-{size}-{stroke}"
                path = LIBRARY / "svg" / f"{key}.svg"
                shutil.copy2(report["output"], path)
                timings.append({**report, "output": path.relative_to(ROOT).as_posix()})
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
        data["symbols"].append(entry)
        print(f"Built {sid}: 9 configurations", flush=True)
    (LIBRARY / "catalog.json").write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    (ROOT / "build/library-measurements.json").write_text(json.dumps(timings, indent=2)+"\n", encoding="utf-8")
    items = [c for s in data["symbols"] for c in s["configurations"]]
    print(json.dumps({"configurations":len(items),"compile_seconds":sum(t["compile_seconds"] for t in timings),
        "convert_seconds":sum(t["convert_seconds"] for t in timings)},indent=2))


if __name__ == "__main__":
    build()
