"""Generate the approved six appearances and their 54 preset combinations."""
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from core import ROOT, SVG, BP_MM, definitions, render_symbol, read_yaml, write_svg
from exports import LIBRARY, document, place, sheet
from proof import render_png, text, native_circuitikz

ORDER = ("resistor-eu", "resistor-us", "inductor-coil", "capacitor", "opamp", "opamp-supply")


def build():
    (LIBRARY / "svg").mkdir(parents=True, exist_ok=True)
    (LIBRARY / "tex").mkdir(exist_ok=True)
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
                # Every exported configuration has a matching standalone TeX bundle.
                bundle = LIBRARY / "tex" / key
                bundle.mkdir(exist_ok=True)
                for helper in (ROOT / "tex").glob("*"):
                    shutil.copy2(helper, bundle / helper.name)
                shutil.copy2(Path(report["output"]).with_suffix(".tex"), bundle / "symbol.tex")
        data["symbols"].append(entry)
        print(f"Built {sid}: 9 configurations", flush=True)
    (LIBRARY / "catalog.json").write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    (ROOT / "review/library-measurements.json").write_text(json.dumps(timings, indent=2)+"\n", encoding="utf-8")
    items = [c for s in data["symbols"] for c in s["configurations"]]
    (ROOT / "review/library-sheet.svg").write_bytes(sheet(items, 6, 6))
    (ROOT / "review/library-symbols.svg").write_bytes(sheet(items, 6, 6, True))
    # Review-only grid and markers, same pin origin and scale in every cell.
    proof = document(218, 252, "Schematica · 54 configurations")
    text(proof, 6, 8, "Schematica · complete preset library", 4)
    text(proof, 6, 15, "Six appearances · independent size and stroke · 1 mm inspection grid", 2.5)
    labels = ("EU resistor", "US resistor", "Coil inductor", "Capacitor", "Op-amp", "With supplies")
    for col, name in enumerate(labels):
        text(proof, 42+29*col-11, 24, name, 2.2)
    for row, (size, stroke) in enumerate((s,w) for s in presets["sizes"] for w in presets["strokes"]):
        y = 39+24*row
        text(proof, 4, y-1, size.title(), 2.5)
        text(proof, 4, y+3, stroke.title(), 2.1)
        for col, symbol in enumerate(data["symbols"]):
            x=42+29*col
            grid = ET.SubElement(proof, f"{{{SVG}}}g", {"stroke":"#d8dfe4","stroke-width":"0.035","fill":"none"})
            for dx in range(-13,14):
                ET.SubElement(grid, f"{{{SVG}}}path", {"d":f"M{x+dx},{y-10}v20"})
            for dy in range(-10,11):
                ET.SubElement(grid, f"{{{SVG}}}path", {"d":f"M{x-13},{y+dy}h26"})
            item=next(c for c in symbol["configurations"] if c["size"]==size and c["stroke"]==stroke)
            place(proof,item,x,y,f"proof-{row}-{col}",origin=True)
            for px,py in item["pins_mm"].values():
                ET.SubElement(proof, f"{{{SVG}}}circle", {"cx":str(x+px),"cy":str(y-py),"r":"0.14","fill":"#2d69a5"})
    write_svg(proof, ROOT / "review/library-proof.svg")
    render_png(ROOT / "review/library-proof.svg", width=2000, background="white")
    native_circuitikz()
    print(json.dumps({"configurations":len(items),"compile_seconds":sum(t["compile_seconds"] for t in timings),
        "convert_seconds":sum(t["convert_seconds"] for t in timings)},indent=2))


if __name__ == "__main__":
    build()
