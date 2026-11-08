"""Export the compiled preference comparison as transparent, theme-aware assets.

Usage: python render.py /absolute/path/to/drawing.pdf
Requires PyMuPDF. Build the TeX outside this folder; PDF/logs are temporary.
"""
from pathlib import Path
import re
import sys
import fitz

root = Path(__file__).resolve().parent
pdf = Path(sys.argv[1]).resolve()
doc = fitz.open(pdf)
assert len(doc) == 1, "Expected one comparison page"
page = doc[0]
text = page.get_text()
assert "Before" in text and "After" in text
assert text.count("signal I/O") == 2
# Keep identical panels: the page midpoint separates the two TeX scopes.
width, height = page.rect.width, page.rect.height
regions = {
    "comparison": page.rect,
    "before": fitz.Rect(0, 0, width / 2, height),
    "after": fitz.Rect(width / 2, 0, width, height),
}
for name, crop in regions.items():
    single = fitz.open(pdf)
    pg = single[0]
    pg.set_cropbox(crop)
    pg.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=True).save(root / f"{name}.png")
    svg = pg.get_svg_image(text_as_path=True)
    # One monochrome foreground; preserve fill="none" and transparency.
    svg = re.sub(r'(fill|stroke)="#[0-9a-fA-F]{6}"', r'\1="currentColor"', svg)
    title = f"{name.capitalize()}: supply arrows and hollow signal terminals"
    at = svg.index(">") + 1
    for variant, css in {
        "light": "svg { color: #242124; }",
        "dark": "svg { color: #ededeb; }",
        "adaptive": "svg { color: #242124; } @media (prefers-color-scheme: dark) { svg { color: #ededeb; } }",
    }.items():
        out = svg[:at] + f"<title>{title}</title><style>{css}</style>" + svg[at:]
        filename = f"{name}.svg" if variant == "adaptive" else f"{name}-{variant}.svg"
        (root / filename).write_text(out, encoding="utf-8")
    single.close()
print("Exported before, after, and comparison as transparent PNG and light/dark/adaptive SVG.")
