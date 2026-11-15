"""Private Review submission, evidence export and reproducible source packages.

Uses the existing renderer; never changes the working library or its approval ledger.
Credentials and working output belong outside the repository.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path
import time
import urllib.error
import urllib.request
import uuid
import xml.etree.ElementTree as ET

import core
import exports
from custom_renderer import render_all, validate_custom


def canonical(value):
    # Match JSON.stringify's integer representation for cross-language fingerprints.
    def normalized(item):
        if isinstance(item, float) and item.is_integer():
            return int(item)
        if isinstance(item, dict):
            return {k: normalized(v) for k, v in item.items()}
        if isinstance(item, list):
            return [normalized(v) for v in item]
        return item
    return json.dumps(normalized(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256((value if isinstance(value, bytes) else value.encode() if isinstance(value, str) else canonical(value).encode())).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


class Client:
    def __init__(self, config):
        self.config = json.loads(Path(config).read_text(encoding="utf-8")) if not isinstance(config, dict) else config
        self.url = self.config["url"].rstrip("/")
        if not self.url.startswith("https://") and not self.url.startswith("http://localhost:"):
            raise ValueError("Use HTTPS, or localhost for isolated development")

    def request(self, path, value=None, key=None, authenticated=True):
        headers = {"Content-Type": "application/json", "User-Agent": "SchematicaReviewDesktop/1.0"}
        if authenticated:
            headers["Authorization"] = "Bearer " + self.config["token"]
        if value is not None:
            headers["Idempotency-Key"] = key or str(uuid.uuid4())
        request = urllib.request.Request(self.url + path, data=None if value is None else json.dumps(value, ensure_ascii=False).encode(), headers=headers)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read()
                    return json.loads(raw) if "json" in response.headers.get("Content-Type", "") else raw
            except urllib.error.HTTPError as error:
                detail = error.read().decode(errors="replace")
                if error.code in (429, 500, 502, 503, 504) or (error.code == 409 and "Another device saved first" in detail):
                    if attempt < 3:
                        time.sleep(1 + attempt)
                        continue
                raise RuntimeError(f"Review returned {error.code}: {detail[:1200]}") from error
            except (TimeoutError, urllib.error.URLError):
                if attempt == 3:
                    raise
                time.sleep(1 + attempt)

    def action(self, name, value, key=None):
        return self.request("/api/review/actions/" + name, value, key)

    def state(self):
        return self.request("/api/review/state")

    def revision(self, revision_id):
        return self.request("/api/review/revisions/" + revision_id)

    def upload(self, package, job=None):
        package = Path(package)
        revision = json.loads((package / "revision.json").read_text(encoding="utf-8"))
        existing = self.state()["symbols"].get(revision["symbol"]["id"])
        if existing and revision["id"] in existing["revisions"]:
            if self.revision(revision["id"])["fingerprint"] != revision["fingerprint"]:
                raise ValueError("A different immutable revision already uses this ID")
            return {"id": revision["id"], "recovered": True}
        for path in (package / "assets").glob("*.svg"):
            content = path.read_bytes().decode("utf-8")
            if digest(content) != path.stem:
                raise ValueError("Package asset changed: " + path.name)
            self.request("/api/review/assets", {"hash": path.stem, "body": content})
        payload = {"revision": revision}
        if job:
            payload.update(job=job["id"], lease=job["lease"])
        # Lease changes on recovery, so key must include its lease; immutable revision
        # identity and state checks still prevent duplicate uploads across claims.
        return self.action("upload", payload, "upload:" + revision["id"] + (":" + job["lease"] if job else ""))

    def backup(self, output):
        output = Path(output)
        output.mkdir(parents=True, exist_ok=False)
        version = self.state()["version"]
        manifest = {}
        for table in ("state", "events", "revisions", "assets", "requests", "publication"):
            rows, after = [], ""
            while True:
                page = self.request(f"/api/review/backup?table={table}&after={after}")
                rows.extend(page["rows"])
                if not page["rows"]:
                    break
                after = page["next"]
            path = output / (table + ".json")
            write_json(path, rows)
            manifest[table] = {"rows": len(rows), "sha256": digest(path.read_bytes())}
        consistent = self.state()["version"] == version
        write_json(output / "manifest.json", {"url": self.url, "at": time.time(), "collections": manifest, "version": version, "consistent": consistent})
        if not consistent:
            raise RuntimeError("Review changed during backup. This copy is retained but is not a restore point. Pause the desktop and review edits, then repeat into a new directory.")
        return manifest

    def source_export(self, revision_id, output):
        revision = self.revision(revision_id)
        output = Path(output)
        output.mkdir(parents=True, exist_ok=False)
        write_json(output / "revision.json", revision)
        write_json(output / "definition.json", revision["source"]["definition"])
        (output / "recipe.tex").write_text(revision["source"]["recipe"], encoding="utf-8")
        (output / "helpers").mkdir()
        for name, content in revision["source"].get("helpers", {}).items():
            if Path(name).name != name or not name.endswith((".tex", ".sty")):
                raise ValueError("Unsafe helper name in source archive")
            (output / "helpers" / name).write_text(content, encoding="utf-8")
        (output / "svg").mkdir()
        for c in revision["symbol"]["configurations"]:
            raw = self.request("/review/assets/" + c["sha256"])
            if digest(raw) != c["sha256"]:
                raise ValueError("Hosted artwork fingerprint changed")
            (output / "svg" / (c["key"] + ".svg")).write_bytes(raw)
        events, after = [], 0
        while True:
            page = self.request(f"/api/review/evidence?after={after}")
            if not page["events"]:
                break
            events.extend(page["events"]); after = page["next"]
        # The full private event chain retains shared-target context and proposal decisions.
        write_json(output / "review-events.json", events)
        write_json(output / "checksums.json", {str(p.relative_to(output)): digest(p.read_bytes()) for p in output.rglob("*") if p.is_file()})
        return {"revision": revision_id, "fingerprint": revision["fingerprint"], "directory": str(output)}


def recovery_sql(backup, output):
    """Create an import for a NEW database; never connects to or replaces a database."""
    backup, output = Path(backup), Path(output)
    if output.exists():
        raise ValueError("Choose a new recovery SQL file")
    manifest = json.loads((backup / "manifest.json").read_text())
    if not manifest.get("consistent"):
        raise ValueError("Backup was not a consistent restore point")
    tables = {"state", "events", "revisions", "assets", "requests", "publication"}
    if set(manifest["collections"]) != tables:
        raise ValueError("Backup is incomplete")
    statements = [(core.ROOT / "review/schema.sql").read_text()]
    def literal(value):
        if value is None: return "NULL"
        if isinstance(value, (int, float)): return str(value)
        # Hex preserves exact UTF-8 bytes and CRLF through Windows text-file IO.
        return "CAST(X'" + str(value).encode("utf-8").hex() + "' AS TEXT)"
    for table in ("assets", "revisions", "events", "requests", "publication", "state"):
        path = backup / (table + ".json")
        if digest(path.read_bytes()) != manifest["collections"][table]["sha256"]:
            raise ValueError("Backup checksum failed: " + table)
        for row in json.loads(path.read_text(encoding="utf-8")):
            first = {k: v[:4096] if isinstance(v, str) else v for k, v in row.items()}
            statements.append(f"INSERT {'OR REPLACE ' if table == 'state' else ''}INTO {table} ({','.join(row)}) VALUES ({','.join(literal(v) for v in first.values())});")
            key = {"assets": "hash", "events": "sequence"}.get(table, "id")
            for column, value in row.items():
                if isinstance(value, str):
                    for offset in range(4096, len(value), 4096):
                        statements.append(f"UPDATE {table} SET {column}={column}||{literal(value[offset:offset+4096])} WHERE {key}={literal(row[key])};")
    output.write_text("\n".join(statements), encoding="utf-8")
    return str(output)


def package_symbol(symbol, source, directory, artwork_root, visual, *, parent=None, batch="Individual", migration=False, change=None, revision_id=None):
    """Package an already-rendered symbol. No recompilation for metadata/decisions."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    asset_dir = directory / "assets"
    asset_dir.mkdir()
    symbol = copy.deepcopy(symbol)
    original_root = exports.LIBRARY
    exports.LIBRARY = Path(artwork_root).resolve()
    try:
        for c in symbol["configurations"]:
            source_path = (exports.LIBRARY / c["svg"]).resolve()
            if not source_path.is_relative_to(exports.LIBRARY):
                raise ValueError("Artwork path escaped its source directory")
            content = source_path.read_bytes()
            svg_root = ET.fromstring(content)
            core.validate_svg_references(svg_root)
            box = [float(v) for v in svg_root.get("viewBox").split()]
            c["visual_center_from_origin_mm"] = [(box[0] + box[2] / 2 - c["origin_svg"][0]) * core.BP_MM,
                                                  (box[1] + box[3] / 2 - c["origin_svg"][1]) * core.BP_MM]
            c["sha256"] = digest(content)
            (asset_dir / (c["sha256"] + ".svg")).write_bytes(content)
            fragment = ET.Element(f"{{{core.SVG}}}svg")
            exports.place(fragment, c, 0, 0, "review-" + c["key"], origin=True)
            fragment_bytes = exports.svg_bytes(fragment)
            c["fragment"] = digest(fragment_bytes)
            (asset_dir / (c["fragment"] + ".svg")).write_bytes(fragment_bytes)
            c.pop("asset", None)
    finally:
        exports.LIBRARY = original_root
    fingerprint = digest({"source": source, "configurations": [{k: c[k] for k in ("key", "sha256", "fragment")} for c in symbol["configurations"]]})
    references = core.ROOT.parent / "docs/SYMBOL_REFERENCE.md"
    revision = {"id": revision_id or str(uuid.uuid4()), "parent": parent, "symbol": symbol, "source": source,
                "fingerprint": fingerprint, "batch": batch, "migration": migration, "change": change,
                "readiness": {"configurations": len(symbol["configurations"]),
                    "renderer": {"core": digest((core.ROOT / "core.py").read_bytes()), "custom": digest((core.ROOT / "custom_renderer.py").read_bytes())},
                    "reference": {"path": "docs/SYMBOL_REFERENCE.md", "sha256": digest(references.read_bytes())}, "visual": visual}}
    provenance = subprocess.run(["git", "rev-parse", "HEAD"], cwd=core.ROOT, capture_output=True, text=True)
    revision["provenance"] = {"repository_commit": provenance.stdout.strip() if provenance.returncode == 0 else None,
                              "renderer_hashes_are_authoritative": True}
    if migration:
        revision["historical_approval"] = symbol.get("verification")
        revision["history_note"] = "Migrated accepted source and exact artwork. Earlier comments and decisions were not recorded; none are inferred."
    write_json(directory / "revision.json", revision)
    return revision


def render_package(definition, recipe, output, visual, *, parent=None, change=None, batch="Individual", revision_id=None):
    output = Path(output)
    validate_custom(definition, recipe)
    rendered = output / "rendered"
    symbol = render_all(definition, recipe, rendered)
    source = {"format": "custom", "definition": definition, "recipe": recipe,
              "helpers": {p.name: p.read_text(encoding="utf-8") for p in (core.ROOT / "tex").glob("*") if p.is_file()},
              "presets": core.read_yaml(core.ROOT / "presets.yaml")}
    revision = package_symbol(symbol, source, output / "package", rendered, visual, parent=parent, batch=batch, change=change, revision_id=revision_id)
    return revision


def migrate(client, output):
    from build_site import payload
    data = json.loads(payload()["library/catalog.json"])
    by_id = {s["id"]: s for s in core.definitions()}
    helpers = {p.name: p.read_text(encoding="utf-8") for p in (core.ROOT / "tex").glob("*") if p.is_file()}
    existing = client.state()["symbols"]
    for symbol in data["symbols"]:
        if symbol["id"] in existing:
            continue
        definition = by_id[symbol["id"]]
        source = {"format": "registered", "definition": definition,
                  "recipe": helpers.get(definition["recipe"] + ".tex", helpers["schematica.sty"]),
                  "helpers": helpers, "presets": data["presets"]}
        target = Path(output) / symbol["id"]
        if not target.exists():
            package_symbol(symbol, source, target, core.ROOT / "library",
                           {"by": "historical migration", "summary": "Existing accepted rendering and fingerprint retained; no new visual acceptance inferred."}, migration=True, batch=symbol.get("batch", "Accepted library"))
        client.upload(target)
        print("Preserved", symbol["id"], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Private desktop configuration outside the repository")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    upload = sub.add_parser("upload"); upload.add_argument("package")
    backup = sub.add_parser("backup"); backup.add_argument("output")
    migration = sub.add_parser("migrate"); migration.add_argument("output")
    source = sub.add_parser("source"); source.add_argument("revision"); source.add_argument("output")
    recovery = sub.add_parser("recovery-sql"); recovery.add_argument("backup"); recovery.add_argument("output")
    prepare = sub.add_parser("prepare")
    for name in ("definition", "recipe", "output", "visual-note"):
        prepare.add_argument("--" + name, required=True)
    prepare.add_argument("--parent"); prepare.add_argument("--batch", default="Individual")
    args = parser.parse_args(); client = Client(args.config)
    for name in ("dvisvgm", "tectonic", "inkscape"):
        if client.config.get(name):
            os.environ["SCHEMATICA_" + name.upper()] = client.config[name]
    if args.command == "status":
        state = client.state(); print(json.dumps({"symbols": len(state["symbols"]), "desktop": state["desktop"], "jobs": state["jobs"]}, indent=2))
    elif args.command == "upload": print(client.upload(args.package))
    elif args.command == "backup": print(client.backup(args.output))
    elif args.command == "migrate": migrate(client, args.output)
    elif args.command == "source": print(client.source_export(args.revision, args.output))
    elif args.command == "recovery-sql": print(recovery_sql(args.backup, args.output))
    elif args.command == "prepare":
        definition = core.read_yaml(Path(args.definition))
        revision = render_package(definition, Path(args.recipe).read_text(encoding="utf-8"), Path(args.output),
            {"by": "submitting agent", "summary": args.visual_note}, parent=args.parent, batch=args.batch)
        print(json.dumps({"revision": revision["id"], "configurations": len(revision["symbol"]["configurations"]), "package": str(Path(args.output) / "package")}))


if __name__ == "__main__":
    main()
