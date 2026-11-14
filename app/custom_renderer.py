"""Render one confirmed custom parameterized TeX recipe with existing packaging."""
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from core import (ROOT, SVG, INK, BP_MM, ID_RE, MACROS, ValidationError, read_yaml, validate_definition,
                  configuration_choices, configuration_key, resolve_settings, parse_metadata,
                  package_svg, write_svg, run, tool)
from verification import digest, design_fingerprint
from recipe_registry import BATCH_MACROS


def validate_custom(definition, recipe):
    if definition.get("recipe") != "custom":
        raise ValidationError("Individual creation uses a custom parameterized TeX recipe")
    check = copy.deepcopy(definition)
    check["recipe"] = "resistor-eu"
    check.pop("options", None)
    validate_definition(check, read_yaml(ROOT / "presets.yaml"))
    for field in ("name", "description", "family"):
        if not isinstance(definition.get(field), str) or not definition[field].strip():
            raise ValidationError(f"A nonempty {field} is required")
    for field in ("keywords", "types"):
        if not isinstance(definition.get(field), list) or not definition[field] or any(not isinstance(s, str) or not s.strip() for s in definition[field]):
            raise ValidationError(f"Provide meaningful {field}")
    for kind in ("sizes", "strokes"):
        if set(definition["presets"][kind]) != set(read_yaml(ROOT / "presets.yaml")[kind]):
            raise ValidationError("Custom symbols must support all three independent size/stroke choices")
    parts = {p["id"] for p in definition["parts"]}
    for name, spec in definition.get("options", {}).items():
        if not ID_RE.fullmatch(name) or not isinstance(spec, dict) or not spec.get("name"):
            raise ValidationError("Invalid named option")
        values = spec.get("values", [])
        ids = [v.get("id") for v in values]
        if not 2 <= len(ids) <= 8 or any(not isinstance(i, str) or not ID_RE.fullmatch(i) for i in ids) or len(set(ids)) != len(ids):
            raise ValidationError("Options need 2–8 distinct named values")
        if spec.get("default") not in ids or any(not v.get("name") for v in values):
            raise ValidationError("Options need display names and a supported default")
        if not spec.get("affected_parts") or set(spec["affected_parts"]) - parts:
            raise ValidationError("Every option must declare its affected parts")
    if len(configuration_choices(definition)) > 288:
        raise ValidationError("At most 288 configurations per individual design")
    if not isinstance(recipe, str) or not 1 <= len(recipe) <= 50000:
        raise ValidationError("Provide a bounded TeX recipe")
    source = re.sub(r"(?<!\\)%[^\n]*", "", recipe)
    if "^^" in source or "\\csname" in source:
        raise ValidationError("TeX character/command construction is not supported")
    allowed = {"newcommand", "SCCustom", "SCresolve", "SCpin", "SCdimension", "SCscale", "SCstroke", "SCinstance", "SCoption",
               "begin", "end", "draw", "path", "fill", "filldraw", "node", "coordinate", "pgfmathsetmacro", "pgfmathtruncatemacro",
               "ifcase", "or", "else", "fi", "ifnum", "relax", "tiny", "small", "scriptsize", "sffamily", "mathrm", "text", "Omega",
               "alpha", "beta", "gamma", "theta", "mu", "pi", "rho", "phi", "omega", "Delta", "cdot", "pm", "frac", "sqrt"}
    # Scratch numeric macros are defined only through pgfmath, never arbitrary TeX.
    scratch = set(re.findall(r"\\pgfmath(?:set|truncatemacro)\{\\(SC[a-zA-Z]+)\}", source))
    # Correct extraction for both pgfmathsetmacro and pgfmathtruncatemacro.
    scratch |= set(re.findall(r"\\(?:pgfmathsetmacro|pgfmathtruncatemacro)\{\\(SC[a-zA-Z]+)\}", source))
    if scratch & {"SCresolve", "SCpin", "SCdimension", "SCscale", "SCstroke", "SCinstance", "SCoption", "SCCustom"}:
        raise ValidationError("Cannot redefine drawing infrastructure")
    commands = set(re.findall(r"\\([A-Za-z]+)", source))
    allowed |= set(MACROS.values())
    if commands - allowed - scratch:
        raise ValidationError("Unsupported TeX commands: " + ", ".join(sorted(commands - allowed - scratch)))
    if len(re.findall(r"\\newcommand", source)) != 1 or not re.match(r"\s*\\newcommand\{\\SCCustom\}\[3\]", source):
        raise ValidationError("Recipe must define exactly one three-argument SCCustom macro")
    if any(env not in {"scope", "SCpart"} for env in re.findall(r"\\(?:begin|end)\{([^}]+)\}", source)):
        raise ValidationError("Only scope and SCpart environments are supported")
    for name in re.findall(r"\\SCoption\{([^}]+)\}", source):
        if name not in definition.get("options", {}):
            raise ValidationError("Recipe refers to an undefined option")


def signature(path, part_id):
    root = ET.parse(path).getroot()
    group = root.find(f"{{{SVG}}}g")
    part = next(p for p in group if p.get("data-part") == part_id)
    def tree(node):
        if node.tag in {f"{{{SVG}}}desc", f"{{{SVG}}}title"}:
            return None
        attrs = {k: v for k, v in node.attrib.items() if k not in ("id", f"{{{INK}}}label")}
        # Converter IDs include revision; paths and references retain actual shape.
        attrs = {k: re.sub(r"sc-[^#\s)]+--(?=glyph)", "", v) for k, v in attrs.items()}
        return [node.tag, attrs, (node.text or "").strip(), [v for c in node if (v := tree(c)) is not None]]
    inherited = {k: v for k, v in group.attrib.items() if not k.startswith("data-") and k not in ("id", f"{{{INK}}}label", "transform")}
    transform = re.sub(r"^translate\([^)]*\)", "", group.get("transform", ""))
    return digest([inherited, transform, tree(part)])


def render_all(definition, recipe, output):
    validate_custom(definition, recipe)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "definition.json").write_text(json.dumps(definition, indent=2), encoding="utf-8")
    (output / "custom.tex").write_text(recipe, encoding="utf-8")
    symbol = copy.deepcopy(definition)
    symbol["configurations"] = []
    symbol["batch"] = "individual"
    symbol["source_fingerprint"] = digest({"definition": definition, "recipe": recipe})
    paths = {}
    for size, stroke, options in configuration_choices(definition):
        settings = resolve_settings(definition, size, stroke, options)
        key = configuration_key(definition["id"], size, stroke, options)
        work = output / key
        work.mkdir()
        for helper in (ROOT / "tex").glob("*"):
            shutil.copy2(helper, work / helper.name)
        (work / "custom.tex").write_text(recipe, encoding="utf-8")
        choices = "\n".join(r"\expandafter\def\csname SCoption@" + name + r"\endcsname{" + str([v["id"] for v in definition["options"][name]["values"]].index(value)) + "}"
                            for name, value in options.items())
        # Only trusted, explicitly registered recipes may supply helper macros.
        imports = "\n".join(r"\input{" + name + ".tex}" for name, macro in BATCH_MACROS.items()
                            if re.search(r"\\" + re.escape(macro) + r"\b", recipe))
        instance = f"sc-{definition['id']}-r{definition['revision']}-{size}-{stroke}"
        document = r"""\documentclass[border=1mm]{standalone}
\def\pgfsysdriver{pgfsys-dvisvgm.def}
\usepackage{schematica}
\SCsvgtrueexport
\newcommand{\SCoption}[1]{\csname SCoption@#1\endcsname}
""" + choices + "\n" + imports + "\n" + r"\input{custom.tex}" + r"""
\begin{document}
\SCrecordto{symbol.scmeta}
\begin{tikzpicture}
""" + rf"\SCCustom{{{instance}}}{{{settings['size_factor']}}}{{{settings['stroke_mm']}}}" + r"""
\end{tikzpicture}
\SCrecordend
\end{document}
"""
        (work / "symbol.tex").write_text(document, encoding="utf-8")
        _, log = run([tool("tectonic"), "-X", "compile", "--outfmt", "xdv", "--keep-logs", "--untrusted", "symbol.tex"], work)
        # Outline text using the same font lookup as the authoritative renderer.
        import subprocess
        font = subprocess.run([tool("tectonic"), "-X", "bundle", "cat", "--only-cached", "lmsans10-regular.otf"], cwd=work, capture_output=True, timeout=120)
        if font.returncode == 0 and font.stdout.startswith(b"OTTO"):
            (work / "lmsans10-regular.otf").write_bytes(font.stdout)
        _, conversion = run([tool("dvisvgm"), "--no-fonts", "--exact-bbox", "--bbox=1mm", "--output=symbol.raw.svg", "symbol.xdv"], work)
        (work / "commands.log").write_text(log + conversion, encoding="utf-8")
        metadata = parse_metadata(work / "symbol.scmeta", definition)
        svg = package_svg(work / "symbol.raw.svg", definition, settings, metadata, instance)
        path = output / f"{key}.svg"
        write_svg(svg, path)
        paths[key] = path
        stored_meta = json.loads(svg.find(f"{{{SVG}}}metadata").text)
        symbol["configurations"].append({"key": key, "symbol_id": definition["id"], "name": definition["name"],
            "revision": definition["revision"], "size": size, "stroke": stroke, "options": options,
            "settings": settings, "svg": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "svg_bytes": path.stat().st_size, "width_mm": float(svg.get("width")[:-2]),
            "height_mm": float(svg.get("height")[:-2]), "origin_svg": stored_meta["origin_svg"], **metadata})
    configs = symbol["configurations"]
    for config in configs:
        same_size = [c for c in configs if c["size"] == config["size"]]
        if any(c["pins_mm"] != config["pins_mm"] for c in same_size):
            raise ValidationError("Stroke and options must preserve terminal coordinates")
        for name, spec in definition.get("options", {}).items():
            siblings = [c for c in same_size if c["stroke"] == config["stroke"] and
                        all(c["options"][k] == v for k, v in config["options"].items() if k != name)]
            for part in {p["id"] for p in definition["parts"]} - set(spec["affected_parts"]):
                if any(signature(paths[c["key"]], part) != signature(paths[config["key"]], part) for c in siblings):
                    raise ValidationError(f"Option {name} changed unrelated part {part}")
    symbol["verification"] = {"status": "unverified", "fingerprint": design_fingerprint(symbol, output)}
    return symbol


def preserve_base(symbol, base, paths, base_paths, affected_parts):
    if {p["id"]: (p["kind"], p["lead_part"]) for p in symbol["pins"]} != {p["id"]: (p["kind"], p["lead_part"]) for p in base["pins"]}:
        raise ValidationError("Options/refinement must preserve connection identities")
    base_parts = {p["id"] for p in base["parts"]}
    if not base_parts.issubset({p["id"] for p in symbol["parts"]}):
        raise ValidationError("Existing parts must be preserved")
    for config in symbol["configurations"]:
        selected = {k: v for k, v in config.get("options", {}).items() if k in base.get("options", {})}
        candidates = [c for c in base["configurations"] if c["size"] == config["size"] and c["stroke"] == config["stroke"] and c.get("options", {}) == selected]
        if len(candidates) != 1:
            raise ValidationError("Existing option values and configurations must be preserved")
        original = candidates[0]
        if original["pins_mm"] != config["pins_mm"]:
            raise ValidationError("Refinement moved existing terminals")
        for part in base_parts - set(affected_parts):
            if signature(paths[config["key"]], part) != signature(base_paths[original["key"]], part):
                raise ValidationError(f"Refinement changed unrelated part {part}")
