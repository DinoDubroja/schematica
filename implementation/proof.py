"""Build only the two-appearance checkpoint; expansion requires user review."""
from __future__ import annotations
import copy
import json
import math
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile

from core import (ROOT, SVG, INK, XLINK, BP_MM, tool, run, render_symbol,
                  namespace_ids, write_svg, validate_svg_references)

REVIEW = ROOT / "review"


def svg_document(width, height, title):
    root = ET.Element(f"{{{SVG}}}svg", {"version": "1.1", "width": f"{width}mm",
        "height": f"{height}mm", "viewBox": f"0 0 {width} {height}"})
    ET.SubElement(root, f"{{{SVG}}}title").text = title
    return root


def text(root, x, y, value, size=2.5):
    ET.SubElement(root, f"{{{SVG}}}text", {"x": str(x), "y": str(y),
        "font-family": "Arial, sans-serif", "font-size": str(size), "fill": "#222"}).text = value


def add_artwork(root, path, x, y, prefix):
    """Place converter artwork. Only positioning, no new symbol geometry."""
    original = ET.parse(path).getroot()
    namespace_ids(original, prefix)
    vb = [float(v) for v in original.get("viewBox").split()]
    groups = original.findall(f"{{{SVG}}}g")
    assert len(groups) == 1
    group = copy.deepcopy(groups[0])
    tx, ty = x - (vb[0]+vb[2]/2)*BP_MM, y - (vb[1]+vb[3]/2)*BP_MM
    group.set("transform", f"translate({tx},{ty}) scale({BP_MM}) " + group.get("transform", ""))
    for defs in original.findall(f"{{{SVG}}}defs"):
        root.append(copy.deepcopy(defs))
    root.append(group)
    return group


def render_png(svg, width=1400, background=None):
    args = [tool("inkscape"), str(svg), f"--export-filename={svg.with_suffix('.png')}", f"--export-width={width}"]
    if background:
        args += [f"--export-background={background}", "--export-background-opacity=1"]
    run(args, svg.parent)


def symbols_library(paths):
    root = svg_document(60, 30, "Schematica rendering proof")
    defs = ET.SubElement(root, f"{{{SVG}}}defs")
    for i, path in enumerate(paths):
        source = ET.parse(path).getroot()
        metadata = json.loads(source.find(f"{{{SVG}}}metadata").text)
        sid = f"symbol-{metadata['symbol_id']}-{metadata['settings']['size']}-{metadata['settings']['stroke']}"
        sym = ET.SubElement(defs, f"{{{SVG}}}symbol", {"id": sid, "overflow": "visible"})
        ET.SubElement(sym, f"{{{SVG}}}title").text = f"{metadata['symbol_id']} / {metadata['settings']['size']} / {metadata['settings']['stroke']}"
        ET.SubElement(sym, f"{{{SVG}}}desc").text = "Whole symbol contains named editable parts. Unlink a placed clone before editing parts."
        # Inkscape creates SVG use instances: keep symbol content in mm user units.
        add_artwork(sym, path, 0, 0, f"library-{i}")
        ET.SubElement(root, f"{{{SVG}}}use", {f"{{{XLINK}}}href": f"#{sid}", "id": f"example-{i}",
            "transform": f"translate({15+30*i},15)"})
    write_svg(root, REVIEW / "symbols.svg")


def editable_text_fixture():
    work = ROOT / "build/text-fixture"
    work.mkdir(parents=True, exist_ok=True)
    # Local font staging is necessary for this Tectonic build; never redistribute it.
    font = Path("C:/Windows/Fonts/arial.ttf")
    if not font.is_file():
        raise FileNotFoundError("Text proof needs Arial; use an installed equivalent and document it")
    shutil.copy2(font, work / "arial.ttf")
    tex = r"""\documentclass[border=2mm]{standalone}
\def\pgfsysdriver{pgfsys-dvisvgm.def}
\usepackage{fontspec}
\setmainfont{arial.ttf}[Path=./]
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[x=1mm,y=1mm]
\special{dvisvgm:raw <g id="label" data-original-text="Label A">}
\node[anchor=base west,inner sep=0,font=\fontsize{10}{12}\selectfont] at (0,0) {Label A};
\special{dvisvgm:raw </g>}
\end{tikzpicture}
\end{document}
"""
    (work / "label.tex").write_text(tex, encoding="utf-8")
    run([tool("tectonic"), "-X", "compile", "--outfmt", "xdv", "--untrusted", "label.tex"], work)
    run([tool("dvisvgm"), "--font-format=woff", "--exact-bbox", "--bbox=2mm",
         "--output=label.raw.svg", "label.xdv"], work)
    raw = ET.parse(work / "label.raw.svg").getroot()
    style = raw.find(f"{{{SVG}}}style")
    fontsize = re.search(r"font-size:([0-9.]+)px", style.text)[1]
    raw.remove(style)
    for t in raw.iter(f"{{{SVG}}}text"):
        if "".join(t.itertext()).replace(" ", "") != "LabelA":
            raise ValueError("Unexpected converter text; normalization is limited to this simple fixture")
        # Normalize the converter's subset font and absolute tspan spacing for editing.
        for child in list(t):
            t.remove(child)
        t.text = "Label A"
        t.attrib.pop("class", None)
        t.set("font-family", "Arial")
        t.set("font-size", fontsize)
        t.set("id", "editable-label")
    vb = [float(v) for v in raw.get("viewBox").split()]
    raw.set("width", f"{vb[2]*BP_MM}mm")
    raw.set("height", f"{vb[3]*BP_MM}mm")
    namespace_ids(raw, "text-fixture")
    write_svg(raw, REVIEW / "editable-label.svg")
    shutil.copy2(work / "label.tex", REVIEW / "editable-label.tex")
    (REVIEW / "editable-label.strings.json").write_text(json.dumps({"label": "Label A",
        "font": "Arial", "normalization": "Preserve converter text position and font size; replace subset font with installed Arial; restore literal source string."}, indent=2)+"\n", encoding="utf-8")


def native_circuitikz():
    work = ROOT / "build/native-circuitikz"
    work.mkdir(parents=True, exist_ok=True)
    for helper in (ROOT / "tex").glob("*"):
        shutil.copy2(helper, work / helper.name)
    source = r"""% Run with Tectonic or a LaTeX installation with CircuitikZ.
\documentclass[border=2mm]{standalone}
\usepackage{schematica}
\begin{document}
\begin{circuitikz}[x=1mm,y=1mm]
  \SCResistorEU{R1}{1}{0.20}
  \draw (R1-a) -- ++(-5,0) to[C] ++(0,-15) -- ++(5,0);
  \begin{scope}[shift={(30,0)}]
    \SCOpampSupply{U1}{1}{0.20}
  \end{scope}
  \draw (R1-b) -- (U1-in-plus);
  \draw (U1-out) -- ++(5,0);
\end{circuitikz}
\end{document}
"""
    (work / "native-circuitikz.tex").write_text(source, encoding="utf-8")
    seconds, log = run([tool("tectonic"), "-X", "compile", "--keep-logs", "--untrusted", "native-circuitikz.tex"], work)
    (work / "commands.log").write_text(log, encoding="utf-8")
    tex_bundle = REVIEW / "tex"
    tex_bundle.mkdir(exist_ok=True)
    for path in work.glob("*"):
        if path.suffix in (".tex", ".sty", ".pdf"):
            shutil.copy2(path, tex_bundle / path.name)
    return seconds


def build():
    REVIEW.mkdir(exist_ok=True)
    configurations = REVIEW / "configurations"
    configurations.mkdir(exist_ok=True)
    reports = []
    paths = {}
    for symbol in ("resistor-eu", "opamp-supply"):
        for size in ("small", "medium", "large"):
            for stroke in ("thin", "medium", "thick"):
                result = render_symbol(symbol, size, stroke)
                key = f"{symbol}-{size}-{stroke}"
                dest = configurations / f"{key}.svg"
                shutil.copy2(result["output"], dest)
                reports.append({**result, "output": dest.relative_to(ROOT).as_posix()})
                paths[key] = dest
    # A compact review sheet, not the deferred browser catalogue.
    root = svg_document(137, 165, "Two-symbol rendering checkpoint")
    text(root, 5, 7, "Rendering proof · EU resistor and supply-pin op-amp", 3.5)
    text(root, 5, 13, "1 mm inspection grid · same physical scale in every cell", 2.5)
    for i, stroke in enumerate(("thin", "medium", "thick")):
        text(root, 16+43*i, 21, f"{stroke.title()} · {dict(thin='0.15',medium='0.20',thick='0.30')[stroke]} mm")
    for row, (symbol, size) in enumerate((s, z) for s in ("resistor-eu", "opamp-supply") for z in ("small", "medium", "large")):
        y = 32+23*row
        for col, stroke in enumerate(("thin", "medium", "thick")):
            x = 24+43*col
            grid = ET.SubElement(root, f"{{{SVG}}}g", {"stroke": "#d8dfe4", "stroke-width": "0.035", "fill": "none"})
            for dx in range(-13, 14):
                ET.SubElement(grid, f"{{{SVG}}}path", {"d": f"M{x+dx},{y-10}v20"})
            for dy in range(-10, 11):
                ET.SubElement(grid, f"{{{SVG}}}path", {"d": f"M{x-13},{y+dy}h26"})
            key = f"{symbol}-{size}-{stroke}"
            add_artwork(root, paths[key], x, y, f"review-{row}-{col}")
            report = next(r for r in reports if r["symbol_id"] == symbol and r["settings"]["size"] == size and r["settings"]["stroke"] == stroke)
            for px, py in report["pins_mm"].values():
                ET.SubElement(root, f"{{{SVG}}}circle", {"cx": str(x+px), "cy": str(y-py), "r": "0.14", "fill": "#2d69a5"})
            text(root, x-12, y+12, f"{'EU resistor' if row<3 else 'Op-amp'} · {size.title()}", 2)
    write_svg(root, REVIEW / "proof.svg")
    render_png(REVIEW / "proof.svg", background="white")
    # Duplicate the same configuration twice, plus a different size/stroke.
    repeat = svg_document(100, 30, "Repeated symbol identity proof")
    for i, key in enumerate(("opamp-supply-medium-medium", "opamp-supply-medium-medium", "opamp-supply-small-thick")):
        add_artwork(repeat, paths[key], 17+33*i, 15, f"copy-{i}")
    write_svg(repeat, REVIEW / "repeated.svg")
    symbols_library([paths["resistor-eu-medium-medium"], paths["opamp-supply-medium-medium"]])
    editable_text_fixture()
    native_seconds = native_circuitikz()
    (REVIEW / "measurements.json").write_text(json.dumps({"configurations": reports,
        "native_circuitikz_compile_seconds": native_seconds}, indent=2)+"\n", encoding="utf-8")
    for symbol in ("resistor-eu", "opamp-supply"):
        folder = REVIEW / "tex" / symbol
        folder.mkdir(exist_ok=True)
        source = ROOT / f"build/sc-{symbol}-r1-medium-medium"
        for p in source.glob("*"):
            if p.suffix in (".tex", ".sty"):
                shutil.copy2(p, folder / p.name)
    print(json.dumps({"renders": len(reports), "total_compile_seconds": sum(r["compile_seconds"] for r in reports),
        "total_convert_seconds": sum(r["convert_seconds"] for r in reports), "svg_bytes": [min(r["svg_bytes"] for r in reports), max(r["svg_bytes"] for r in reports)]}, indent=2))


if __name__ == "__main__":
    build()
