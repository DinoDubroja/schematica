"""Definition -> parameterized TeX -> XDV -> dvisvgm -> packaged SVG.

No symbol geometry is constructed in Python. The TeX recipes also emit resolved
dimensions, pins and part IDs, so inspection uses the same construction authority.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parent
SVG = "http://www.w3.org/2000/svg"
INK = "http://www.inkscape.org/namespaces/inkscape"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INK)
ET.register_namespace("xlink", XLINK)
MACROS = {"resistor-eu": "SCResistorEU", "resistor-us": "SCResistorUS",
          "inductor-coil": "SCInductorCoil", "capacitor": "SCCapacitor",
          "opamp": "SCOpamp", "opamp-supply": "SCOpampSupply"}
BP_MM = 25.4 / 72
ID_RE = re.compile(r"[a-z][a-z0-9-]*\Z")


class ValidationError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject YAML duplicate keys instead of silently losing definitions."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValidationError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def read_yaml(path):
    with Path(path).open(encoding="utf-8") as stream:
        return yaml.load(stream, Loader=UniqueLoader)


def _unique_ids(items, category):
    ids = [item["id"] for item in items]
    if any(not ID_RE.fullmatch(i) for i in ids):
        raise ValidationError(f"Invalid {category} identifier")
    if len(ids) != len(set(ids)):
        raise ValidationError(f"Duplicate {category} identifier")
    return set(ids)


def validate_definition(definition, presets):
    if definition.get("schema_version") != 1 or not ID_RE.fullmatch(definition.get("id", "")):
        raise ValidationError("Invalid schema or symbol ID")
    if type(definition.get("revision")) is not int or definition["revision"] < 1:
        raise ValidationError("Revision must be a positive integer")
    if definition.get("recipe") not in MACROS:
        raise ValidationError("Unknown recipe")
    parts = _unique_ids(definition["parts"], "part")
    _unique_ids(definition["pins"], "pin")
    for pin in definition["pins"]:
        if pin["lead_part"] not in parts:
            raise ValidationError(f"Unknown lead part: {pin['lead_part']}")
    for kind in ("sizes", "strokes"):
        supported = definition["presets"][kind]
        if not supported or len(supported) != len(set(supported)) or set(supported) - presets[kind].keys():
            raise ValidationError(f"Invalid supported {kind}")


def definitions():
    presets = read_yaml(ROOT / "presets.yaml")
    entries = [read_yaml(p) for p in sorted((ROOT / "definitions").glob("*.yaml"))]
    _unique_ids(entries, "symbol")
    for entry in entries:
        validate_definition(entry, presets)
    return entries


def find_symbols(query=""):
    words = query.casefold().split()
    return [d for d in definitions() if all(w in json.dumps(
        {k: d.get(k, []) for k in ("name", "description", "keywords", "types", "attributes")},
        ensure_ascii=False).casefold() for w in words)]


def get_definition(symbol_id):
    return next((d for d in definitions() if d["id"] == symbol_id), None) or _unknown(symbol_id)


def _unknown(symbol_id):
    raise ValidationError(f"Unknown symbol: {symbol_id}")


def resolve_settings(definition, size="medium", stroke="medium"):
    presets = read_yaml(ROOT / "presets.yaml")
    for kind, choice in (("sizes", size), ("strokes", stroke)):
        if choice not in definition["presets"][kind]:
            raise ValidationError(f"Unsupported {kind} preset: {choice}")
    return {"size": size, "stroke": stroke, "size_factor": presets["sizes"][size]["factor"],
            "stroke_mm": presets["strokes"][stroke]["width_mm"], "grid_mm": presets["grid_mm"]}


def tool(name):
    override = os.environ.get(f"SCHEMATICA_{name.upper()}")
    if override:
        candidate = Path(override)
        if not candidate.is_file():
            raise FileNotFoundError(f"Configured {name} is missing: {candidate}")
        return str(candidate)
    if found := shutil.which(name):
        return found
    workspace = ROOT.parents[1]
    candidates = {
        "dvisvgm": [workspace / "Local/tools/dvisvgm/bin/windows/dvisvgm.exe"],
        "inkscape": [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Inkscape/bin/inkscape.com"],
        "tectonic": [Path(p) / "tectonic/tectonic.exe" for p in os.environ.get("PATH", "").split(os.pathsep)] +
            sorted(Path(os.environ.get("ProgramFiles", "C:/Program Files")).glob(
            "WindowsApps/OpenAI.Codex_*/app/resources/tectonic/tectonic.exe"), reverse=True),
    }.get(name, [])
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(f"Install {name} or set SCHEMATICA_{name.upper()}")


def run(command, cwd):
    started = time.perf_counter()
    completed = subprocess.run([str(c) for c in command], cwd=cwd, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
    if completed.returncode:
        raise RuntimeError(f"Command failed: {command[0]}\n{completed.stdout}\n{completed.stderr}")
    return time.perf_counter() - started, completed.stdout + completed.stderr


def tex_document(definition, settings, instance, svg=True):
    driver = r"\def\pgfsysdriver{pgfsys-dvisvgm.def}" if svg else ""
    export = r"\SCsvgtrueexport" if svg else ""
    return rf"""% Generated from {definition['id']} revision {definition['revision']}.
% Bundle includes schematica.sty and the parameterized recipes.
\documentclass[border=1mm]{{standalone}}
{driver}
\usepackage{{schematica}}
{export}
\begin{{document}}
\SCrecordto{{symbol.scmeta}}
\begin{{tikzpicture}}
\{MACROS[definition['recipe']]}{{{instance}}}{{{settings['size_factor']}}}{{{settings['stroke_mm']}}}
\end{{tikzpicture}}
\SCrecordend
\end{{document}}
"""


def parse_metadata(path, definition):
    pins, parts, dimensions = {}, [], {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        fields = line.split("|")
        if fields[0] == "pin":
            if fields[1] in pins:
                raise ValidationError(f"Duplicate emitted pin {fields[1]}")
            pins[fields[1]] = [float(v) for v in fields[2:]]
        elif fields[0] == "part":
            parts.append(fields[1])
        elif fields[0] == "dimension":
            dimensions[fields[1]] = float(fields[2])
    expected_parts = {p["id"] for p in definition["parts"]}
    if len(parts) != len(set(parts)) or set(parts) != expected_parts:
        raise ValidationError(f"Recipe part mismatch: expected {expected_parts}, emitted {parts}")
    if set(pins) != {p["id"] for p in definition["pins"]}:
        raise ValidationError("Recipe pin mismatch")
    grid = read_yaml(ROOT / "presets.yaml")["grid_mm"]
    if any(abs(v / grid - round(v / grid)) > 1e-5 for xy in pins.values() for v in xy):
        raise ValidationError("Off-grid connection coordinate")
    return {"pins_mm": pins, "dimensions_mm": dimensions, "parts": parts}


def namespace_ids(root, prefix):
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    if len(ids) != len(set(ids)):
        raise ValidationError("Duplicate SVG IDs before namespacing")
    remap = {old: f"{prefix}--{old}" for old in ids}
    for element in root.iter():
        for key, value in list(element.attrib.items()):
            if key == "id":
                element.set(key, remap[value])
            else:
                value = re.sub(r"url\(\s*(['\"]?)#([^)'\"\s]+)\1\s*\)",
                               lambda m: f"url(#{remap.get(m[2], m[2])})", value)
                if key in ("href", f"{{{XLINK}}}href") and value.startswith("#"):
                    value = "#" + remap.get(value[1:], value[1:])
                element.set(key, value)
        if element.tag == f"{{{SVG}}}style":
            raise ValidationError("Embedded CSS requires explicit reference handling")
    validate_svg_references(root)


def validate_svg_references(root):
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    if len(ids) != len(set(ids)):
        raise ValidationError("Duplicate SVG identifiers")
    references = []
    for e in root.iter():
        for key, value in e.attrib.items():
            references += re.findall(r"url\(['\"]?#([^)'\"\s]+)", value)
            if key in ("href", f"{{{XLINK}}}href") and value.startswith("#"):
                references.append(value[1:])
    if set(references) - set(ids):
        raise ValidationError(f"Unknown SVG reference: {set(references) - set(ids)}")


def package_svg(raw_path, definition, settings, metadata, instance):
    """Hoist only anonymous converter wrappers; retain every named part."""
    raw = ET.parse(raw_path).getroot()
    viewbox = [float(v) for v in raw.get("viewBox").split()]
    result = ET.Element(f"{{{SVG}}}svg", {"version": "1.1", "viewBox": raw.get("viewBox"),
        "width": f"{viewbox[2]*BP_MM:.8f}mm", "height": f"{viewbox[3]*BP_MM:.8f}mm"})
    ET.SubElement(result, f"{{{SVG}}}title").text = definition["name"]
    ET.SubElement(result, f"{{{SVG}}}desc").text = definition["description"]
    metadata_element = ET.SubElement(result, f"{{{SVG}}}metadata")
    symbol = ET.SubElement(result, f"{{{SVG}}}g", {"id": instance,
        f"{{{INK}}}label": f"{definition['name']} / {settings['size']} / {settings['stroke']}",
        "data-symbol": definition["id"], "data-revision": str(definition["revision"]),
        "data-size": settings["size"], "data-stroke": settings["stroke"]})
    found = []
    descriptions = {p["id"]: p["description"] for p in definition["parts"]}

    def walk(element, inherited, transforms):
        attrs = dict(inherited)
        attrs.update({k: v for k, v in element.attrib.items() if k not in ("id", "transform", "data-part")})
        transforms = transforms + ([element.get("transform")] if element.get("transform") else [])
        if part_id := element.get("data-part"):
            if part_id not in descriptions or part_id in found:
                raise ValidationError(f"Unknown or duplicate SVG part: {part_id}")
            found.append(part_id)
            part = copy.deepcopy(element)
            part.attrib.update(attrs)
            part.set("transform", " ".join(transforms))
            part.set(f"{{{INK}}}label", part_id)
            ET.SubElement(part, f"{{{SVG}}}desc").text = descriptions[part_id]
            symbol.append(part)
        elif element.tag == f"{{{SVG}}}g":
            for child in element:
                walk(child, attrs, transforms)
        elif element.tag == f"{{{SVG}}}defs":
            result.insert(0, copy.deepcopy(element))
        else:
            raise ValidationError(f"Unexpected artwork outside a named part: {element.tag}")

    for child in raw:
        walk(child, {}, [])
    if set(found) != set(descriptions):
        raise ValidationError(f"Missing SVG parts: {set(descriptions)-set(found)}")
    # The converter's inherited presentation/transform are identical for this proof.
    # Move shared values to the symbol, leaving symbol -> named part -> path.
    common = dict(symbol[0].attrib)
    for part in symbol[1:]:
        common = {k: v for k, v in common.items() if part.get(k) == v}
    for key in ("id", "data-part", f"{{{INK}}}label"):
        common.pop(key, None)
    symbol.attrib.update(common)
    for part in symbol:
        for key in common:
            del part.attrib[key]
    # Locate the TeX coordinate origin, not the visual bounding-box centre.
    # This matters for asymmetric artwork such as the coil above its pin row.
    transform = symbol.get("transform", "")
    origin = re.fullmatch(r"translate\(([-+0-9.eE]+),([-+0-9.eE]+)\)scale\(([-+0-9.eE]+),([-+0-9.eE]+)\)", transform)
    if not origin:
        raise ValidationError(f"Unsupported converter transform: {transform}")
    metadata_element.text = json.dumps({"symbol_id": definition["id"],
        "revision": definition["revision"], "settings": settings, **metadata,
        "origin_svg": [float(origin[1]), float(origin[2])]}, sort_keys=True)
    namespace_ids(result, instance)
    return result


def write_svg(root, path):
    validate_svg_references(root)
    ET.indent(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def render_symbol(symbol_id, size="medium", stroke="medium", output=None):
    definition = get_definition(symbol_id)
    settings = resolve_settings(definition, size, stroke)
    instance = f"sc-{symbol_id}-r{definition['revision']}-{size}-{stroke}"
    output = Path(output or ROOT / "build" / instance).resolve()
    output.mkdir(parents=True, exist_ok=True)
    for helper in (ROOT / "tex").glob("*"):
        shutil.copy2(helper, output / helper.name)
    (output / "symbol.tex").write_text(tex_document(definition, settings, instance), encoding="utf-8")
    compile_seconds, compile_log = run([tool("tectonic"), "-X", "compile", "--outfmt", "xdv",
        "--keep-logs", "--untrusted", "symbol.tex"], output)
    convert_seconds, convert_log = run([tool("dvisvgm"), "--no-fonts", "--exact-bbox", "--bbox=1mm",
        "--output=symbol.raw.svg", "symbol.xdv"], output)
    (output / "commands.log").write_text(compile_log + convert_log, encoding="utf-8")
    resolved = parse_metadata(output / "symbol.scmeta", definition)
    packaged = package_svg(output / "symbol.raw.svg", definition, settings, resolved, instance)
    write_svg(packaged, output / "symbol.svg")
    report = {"symbol_id": symbol_id, "revision": definition["revision"], "settings": settings,
        **resolved, "output": str(output / "symbol.svg"), "compile_seconds": round(compile_seconds, 4),
        "convert_seconds": round(convert_seconds, 4), "svg_bytes": (output / "symbol.svg").stat().st_size,
        "definition_sha256": hashlib.sha256((ROOT / "definitions" / f"{symbol_id}.yaml").read_bytes()).hexdigest()}
    (output / "resolved.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def inspect_symbol(symbol_id, size="medium", stroke="medium"):
    definition = get_definition(symbol_id)
    # Resolve by recompilation: never return stale geometry from edited recipes.
    return {"definition": definition, "resolved": render_symbol(symbol_id, size, stroke)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("find")
    search.add_argument("query", nargs="?", default="")
    for command in ("inspect", "render"):
        cmd = commands.add_parser(command)
        cmd.add_argument("symbol_id")
        cmd.add_argument("--size", default="medium")
        cmd.add_argument("--stroke", default="medium")
        if command == "render":
            cmd.add_argument("--output", type=Path)
    args = vars(parser.parse_args())
    command = args.pop("command")
    result = {"find": find_symbols, "inspect": inspect_symbol, "render": render_symbol}[command](**args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
