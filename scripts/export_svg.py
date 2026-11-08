"""Export transparent light/dark SVGs from one compiled monochrome drawing.

Requires PyMuPDF. Compile drawing.tex first; see PRESENTATION.md for usage.
The existing LaTeX and PNG are never modified.
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


def export(pdf: Path, destination: Path, title: str, description: str) -> None:
    with fitz.open(pdf) as document:
        if len(document) != 1:
            raise ValueError("Expected one figure on one PDF page")
        root = ET.fromstring(document[0].get_svg_image(text_as_path=True))
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
        (destination / f"preview-{theme}.svg").write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    args = parser.parse_args()
    export(args.pdf, args.destination, args.title, args.description)
