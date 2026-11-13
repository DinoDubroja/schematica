"""Compose pre-rendered converter artwork at physical scale; never draw symbols."""
import copy
import io
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

from core import ROOT, SVG, XLINK, BP_MM, ValidationError, namespace_ids, validate_svg_references

LIBRARY = ROOT / "library"


def catalog():
    path = LIBRARY / "catalog.json"
    if not path.is_file():
        raise ValidationError("Library is not built. Run build_library.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def choose(selections, data=None):
    if not isinstance(selections, list) or not 1 <= len(selections) <= 108:
        raise ValidationError("Select between 1 and 108 configurations.")
    lookup = {c["key"]: c for s in (data or catalog())["symbols"] for c in s["configurations"]}
    if any(not isinstance(k, str) or k not in lookup for k in selections):
        raise ValidationError("Unknown configuration.")
    return [lookup[k] for k in selections]


def artwork(item):
    # Paths come from the build manifest, never an HTTP or user-supplied pathname.
    path = (LIBRARY / item["svg"]).resolve()
    if not path.is_relative_to(LIBRARY.resolve()):
        raise ValidationError("Artwork must be inside the library.")
    return ET.parse(path).getroot()


def document(width, height, title):
    root = ET.Element(f"{{{SVG}}}svg", {"version": "1.1", "width": f"{width:.8f}mm",
        "height": f"{height:.8f}mm", "viewBox": f"0 0 {width:.8f} {height:.8f}"})
    ET.SubElement(root, f"{{{SVG}}}title").text = title
    return root


def place(root, item, x, y, prefix, origin=False):
    source = artwork(item)
    namespace_ids(source, prefix)
    meta = json.loads(source.find(f"{{{SVG}}}metadata").text)
    vb = [float(v) for v in source.get("viewBox").split()]
    ox, oy = meta["origin_svg"] if origin else (vb[0]+vb[2]/2, vb[1]+vb[3]/2)
    groups = source.findall(f"{{{SVG}}}g")
    if len(groups) != 1:
        raise ValidationError("Expected one whole-symbol group.")
    group = copy.deepcopy(groups[0])
    group.set("transform", f"translate({x-ox*BP_MM},{y-oy*BP_MM}) scale({BP_MM}) " + group.get("transform", ""))
    for defs in source.findall(f"{{{SVG}}}defs"):
        root.append(copy.deepcopy(defs))
    root.append(group)
    return group


def svg_bytes(root):
    validate_svg_references(root)
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sheet(items, columns=3, spacing=6, symbols=False, title=None, compact_titles=False):
    if type(columns) is not int or not 1 <= columns <= 12:
        raise ValidationError("Columns must be an integer from 1 to 12.")
    if type(spacing) not in (int, float) or not math.isfinite(spacing) or not 0 <= spacing <= 50:
        raise ValidationError("Spacing must be from 0 to 50 mm.")
    columns = min(columns, len(items))
    widths = [max(i["width_mm"] for i in items[c::columns]) for c in range(columns)]
    rows = [items[r:r+columns] for r in range(0, len(items), columns)]
    heights = [max(i["height_mm"] for i in row) for row in rows]
    margin = 4
    root = document(2*margin+sum(widths)+spacing*(columns-1),
                    2*margin+sum(heights)+spacing*(len(rows)-1),
                    title or ("Schematica symbol library" if symbols else "Schematica arranged symbols"))
    defs = ET.SubElement(root, f"{{{SVG}}}defs") if symbols else None
    y = margin
    for row_index, row in enumerate(rows):
        x = margin
        for col, item in enumerate(row):
            prefix = f"instance-{row_index*columns+col+1}"
            cx, cy = x+widths[col]/2, y+heights[row_index]/2
            if symbols:
                sid = f"{prefix}-{item['key']}"
                sym = ET.SubElement(defs, f"{{{SVG}}}symbol", {"id": sid, "overflow": "visible"})
                ET.SubElement(sym, f"{{{SVG}}}title").text = item['name'] if compact_titles else f"{item['name']} · {item['size'].title()} / {item['stroke'].title()}"
                ET.SubElement(sym, f"{{{SVG}}}desc").text = "Unlink the placed instance to edit its named parts."
                ET.SubElement(sym, f"{{{SVG}}}metadata").text = json.dumps({k:item[k] for k in ('symbol_id','revision','size','stroke','pins_mm')})
                place(sym, item, 0, 0, prefix, origin=True)
                # Symbols themselves have their TeX/pin origin at (0,0).
                dx, dy = item["visual_center_from_origin_mm"]
                ET.SubElement(root, f"{{{SVG}}}use", {"id": prefix+"-placement",
                    f"{{{XLINK}}}href": "#"+sid, "transform": f"translate({cx-dx},{cy-dy})"})
            else:
                place(root, item, cx, cy, prefix)
            x += widths[col]+spacing
        y += heights[row_index]+spacing
    return svg_bytes(root)


def export(kind, selections, columns=3, spacing=6):
    items = choose(selections)
    if kind == "svg":
        if len(items) != 1:
            raise ValidationError("Individual SVG export needs exactly one configuration.")
        return f"{items[0]['key']}.svg", "image/svg+xml", svg_bytes(artwork(items[0]))
    if kind == "zip":
        stream = io.BytesIO()
        names = set()
        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
            for index, item in enumerate(items):
                name = f"{item['key']}.svg"
                if name in names:
                    name = f"{item['key']}-copy-{index+1}.svg"
                names.add(name)
                archive.writestr(name, svg_bytes(artwork(item)))
        return "schematica-symbols.zip", "application/zip", stream.getvalue()
    if kind in ("sheet", "symbols"):
        return f"schematica-{kind}.svg", "image/svg+xml", sheet(items, columns, spacing, kind == "symbols")
    raise ValidationError("Unknown export format.")
