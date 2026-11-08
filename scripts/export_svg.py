"""Export transparent light/dark SVGs from one compiled monochrome drawing.

Requires PyMuPDF. Compile drawing.tex first; see PRESENTATION.md for usage.
The existing LaTeX is never modified; PNG export is opt-in.
"""

import argparse
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

import fitz

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)
INK = {"light": "#231f20", "dark": "#e6edf3"}


def export(pdf: Path, destination: Path, title: str, description: str,
           page: int | None = None, stem: str = "preview", png: bool = False) -> None:
    if not stem or Path(stem).name != stem or any(c in stem for c in '/\\:'):
        raise ValueError("Stem must be a simple filename without a path")
    with fitz.open(pdf) as document:
        if page is None and len(document) != 1:
            raise ValueError("Expected one figure on one PDF page")
        selected = 0 if page is None else page - 1
        if selected < 0 or selected >= len(document):
            raise ValueError("Page number is outside the PDF")
        root = ET.fromstring(document[selected].get_svg_image(text_as_path=True))
        raster = document[selected].get_pixmap(matrix=fitz.Matrix(3, 3), alpha=True) if png else None
    if root.findall(f".//{{{SVG}}}image"):
        raise ValueError("Expected vector paths, not embedded raster images")
    # Refuse to recolor multicolor figures or intentional white masks. Such
    # drawings need semantic color mapping, not blanket foreground replacement.
    for node in root.iter():
        for attribute in ("fill", "stroke"):
            color = node.get(attribute)
            if color and color.lower() not in {"none", "#231f20", "#000000", "black"}:
                raise ValueError(f"Review unsupported {attribute} color: {color}")
    root.set("role", "img")
    root.set("aria-labelledby", "figure-title figure-description")
    heading = ET.Element(f"{{{SVG}}}title", {"id": "figure-title"})
    heading.text = title
    desc = ET.Element(f"{{{SVG}}}desc", {"id": "figure-description"})
    desc.text = description
    root.insert(0, heading)
    root.insert(1, desc)
    destination.mkdir(parents=True, exist_ok=True)
    for theme, ink in INK.items():
        themed = deepcopy(root)
        themed.set("fill", ink)  # Also covers SVG's implicit black fill.
        for node in themed.iter():
            for attribute in ("fill", "stroke"):
                if node.get(attribute) and node.get(attribute) != "none":
                    node.set(attribute, ink)
        content = ET.tostring(themed, encoding="unicode") + "\n"
        (destination / f"{stem}-{theme}.svg").write_text(content, encoding="utf-8", newline="\n")
    if raster is not None:
        raster.save(destination / f"{stem}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--page", type=int, help="One-based PDF page (required for multi-page sources)")
    parser.add_argument("--stem", default="preview", help="Output basename, e.g. good or bad")
    parser.add_argument("--png", action="store_true", help="Also export a transparent PNG from the selected page")
    args = parser.parse_args()
    export(args.pdf, args.destination, args.title, args.description, args.page, args.stem, args.png)
