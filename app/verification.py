"""Validate browser approval handoffs; official records are changed only by this CLI."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

from core import ROOT, SVG, INK, ValidationError, definitions, read_yaml

LEDGER = ROOT / "verification.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False).encode()).hexdigest()


def source_fingerprint(definition):
    """Detect stale rendered artwork; editorial corrections are deliberately excluded."""
    recipe = definition["recipe"]
    names = ["schematica.sty", f"{recipe}.tex"]
    if recipe.startswith("opamp"):
        names.append("opamp-common.tex")
    sources = {name: (ROOT / "tex" / name).read_text(encoding="utf-8") for name in names}
    return digest({"recipe": recipe, "drawing": definition.get("drawing", {}),
                   "revision": definition["revision"], "presets": read_yaml(ROOT / "presets.yaml"),
                   "supported": definition["presets"],
                   "pins": [{k: p[k] for k in ("id", "kind", "lead_part")} for p in definition["pins"]],
                   "parts": [p["id"] for p in definition["parts"]], "sources": sources})


def _geometry(element):
    if element.tag in {f"{{{SVG}}}{tag}" for tag in ("title", "desc", "metadata")}:
        return None
    attrs = {k: v for k, v in element.attrib.items() if k != f"{{{INK}}}label"}
    return [element.tag, attrs, (element.text or "").strip(),
            [value for child in element if (value := _geometry(child)) is not None]]


def design_fingerprint(symbol, library):
    """Hash all nine actual drawings and electrical connections, excluding prose."""
    shapes = []
    for config in sorted(symbol["configurations"], key=lambda item: item["key"]):
        path = (Path(library) / config["svg"]).resolve()
        if not path.is_relative_to(Path(library).resolve()) or not path.is_file():
            raise ValidationError("Missing or invalid library artwork. Rebuild the library.")
        shapes.append({"size": config["size"], "stroke": config["stroke"],
                       "pins": config["pins_mm"], "geometry": _geometry(ET.parse(path).getroot())})
    return digest({"id": symbol["id"], "revision": symbol["revision"], "shapes": shapes,
                   "pins": [{k: p[k] for k in ("id", "kind", "lead_part")} for p in symbol["pins"]]})


def read_ledger(path=LEDGER):
    if not Path(path).exists():
        return {"schema_version": 1, "approvals": {}}
    result = json.loads(Path(path).read_text(encoding="utf-8"))
    if result.get("schema_version") != 1 or not isinstance(result.get("approvals"), dict):
        raise ValidationError("Invalid official verification file")
    return result


def publication_catalog(data, source_definitions, library, ledger):
    data = copy.deepcopy(data)
    sources = {s["id"]: s for s in source_definitions}
    seen = set()
    for symbol in data["symbols"]:
        sid = symbol["id"]
        if sid in seen or sid not in sources:
            raise ValidationError(f"Duplicate or unknown catalog design: {sid}")
        seen.add(sid)
        source = sources[sid]
        if symbol.get("source_fingerprint") != source_fingerprint(source):
            raise ValidationError(f"Stale artwork for {sid}; rebuild the affected design before publishing.")
        expected = {(size, stroke) for size in source["presets"]["sizes"]
                    for stroke in source["presets"]["strokes"]}
        configs = symbol["configurations"]
        if len(configs) != len(expected) or {(c["size"], c["stroke"]) for c in configs} != expected:
            raise ValidationError(f"Incomplete configurations for {sid}")
        if symbol["revision"] != source["revision"] or any(c["revision"] != source["revision"] or c["symbol_id"] != sid for c in configs):
            raise ValidationError(f"Stale configuration revision for {sid}")
        for field in ("name", "description", "keywords", "types", "pins", "parts"):
            symbol[field] = source[field]
        symbol["family"] = source.get("family", "resistors" if "resistor" in source["types"] else
                                       "amplifiers" if "active" in source["types"] else "passive")
        symbol["batch"] = source.get("batch", "starter")
        fingerprint = design_fingerprint(symbol, library)
        approval = ledger["approvals"].get(sid, {})
        verified = approval.get("revision") == symbol["revision"] and approval.get("fingerprint") == fingerprint
        symbol["verification"] = {"status": "verified" if verified else "unverified",
                                  "fingerprint": fingerprint}
    return data


def apply_approvals(payload, data, ledger):
    """Validate the whole handoff before changing anything; repeated application is harmless."""
    if not isinstance(payload, dict) or payload.get("schema_version") != 1 or payload.get("library") != "schematica":
        raise ValidationError("Expected a Schematica approvals handoff (schema_version 1)")
    entries = payload.get("approvals")
    if not isinstance(entries, list) or not 1 <= len(entries) <= 10000:
        raise ValidationError("The handoff must contain at least one approval")
    symbols = {s["id"]: s for s in data["symbols"]}
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ValidationError("Invalid approval entry")
        sid = entry["id"]
        if sid not in symbols or sid in seen:
            raise ValidationError(f"Unknown or duplicate design: {sid}")
        seen.add(sid)
        symbol = symbols[sid]
        if type(entry.get("revision")) is not int or entry["revision"] != symbol["revision"] or \
                entry.get("fingerprint") != symbol["verification"]["fingerprint"]:
            raise ValidationError(f"Stale approval for {sid}; review its current design again")
    result = copy.deepcopy(ledger)
    changed = []
    for entry in entries:
        sid = entry["id"]
        current = result["approvals"].get(sid, {})
        if current.get("revision") == entry["revision"] and current.get("fingerprint") == entry["fingerprint"]:
            continue
        result["approvals"][sid] = {"revision": entry["revision"], "fingerprint": entry["fingerprint"],
                                     "evidence": "User approval supplied through the chat handoff"}
        changed.append(sid)
    return result, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    try:
        from exports import catalog, LIBRARY
        before = LEDGER.read_bytes() if LEDGER.exists() else None
        ledger = read_ledger()
        data = publication_catalog(catalog(), definitions(), LIBRARY, ledger)
        result, changed = apply_approvals(json.loads(args.handoff.read_text(encoding="utf-8-sig")), data, ledger)
        if args.action == "apply" and changed:
            if (LEDGER.read_bytes() if LEDGER.exists() else None) != before:
                raise ValidationError("Official verification changed concurrently; retry after reviewing it")
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=LEDGER.parent,
                                             suffix=".tmp", delete=False) as output:
                temporary = Path(output.name)
                output.write(json.dumps(result, indent=2) + "\n")
            try:
                os.replace(temporary, LEDGER)
            finally:
                temporary.unlink(missing_ok=True)
        print(json.dumps({"action": args.action, "changed": changed,
                          "next": "Rebuild, test and publish to make official status visible" if changed else "No changes needed"}, indent=2))
    except (ValidationError, OSError, ValueError) as error:
        parser.exit(1, f"Approval rejected: {error}\n")


if __name__ == "__main__":
    main()
