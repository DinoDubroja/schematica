"""Build the portable viewer and one complete Inkscape library per preset pair."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from core import ROOT, ValidationError, definitions
from exports import LIBRARY, catalog, sheet
from verification import publication_catalog, read_ledger

DIST = ROOT / "dist"
VIEWER_FILES = ("index.html", "style.css", "app.js", "review.js", "theme.js", "_headers", "robots.txt")


def payload():
    data = publication_catalog(catalog(), definitions(), LIBRARY, read_ledger())
    definitions_by_id = {symbol["id"]: symbol for symbol in definitions()}
    files = {name: (ROOT / "viewer" / name).read_bytes() for name in VIEWER_FILES}
    data["exports"] = {}
    for symbol in data["symbols"]:
        # Editorial metadata can be updated without recompiling accepted geometry.
        source = definitions_by_id[symbol["id"]]
        for field in ("name", "description", "keywords", "types"):
            symbol[field] = source[field]
        for config in symbol["configurations"]:
            path = (LIBRARY / config["svg"]).resolve()
            if not path.is_relative_to(LIBRARY.resolve()) or not path.is_file():
                raise ValidationError("Missing or invalid library artwork. Rebuild the library.")
            files[f"library/{config['svg']}"] = path.read_bytes()
    for size in data["presets"]["sizes"]:
        for stroke in data["presets"]["strokes"]:
            items = []
            for symbol in data["symbols"]:
                matches = [c for c in symbol["configurations"] if c["size"] == size and c["stroke"] == stroke]
                if len(matches) != 1:
                    raise ValidationError(f"Expected one {size}/{stroke} configuration per symbol.")
                items.extend(matches)
            filename = f"exports/schematica-{size}-{stroke}.svg"
            files[filename] = sheet(items, symbols=True, compact_titles=True,
                                   title=f"Schematica · {size.title()} / {stroke.title()}")
            data["exports"][f"{size}-{stroke}"] = filename
    files["library/catalog.json"] = (json.dumps(data, indent=2) + "\n").encode()
    hashes = {name: hashlib.sha256(body).hexdigest() for name, body in sorted(files.items())}
    build_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()[:12]
    files["build.json"] = (json.dumps({"build_id": build_id, "files": hashes}, indent=2) + "\n").encode()
    return files


def build():
    files = payload()
    # Prepare everything before replacing the generated output. Never clean sources.
    work = ROOT / "build"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="site-", dir=work) as temporary:
        staging = Path(temporary) / "dist"
        for name, body in files.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        if DIST.is_symlink() or DIST.is_junction() or DIST.resolve() != ROOT.resolve() / "dist":
            raise ValidationError("Refusing to replace a redirected dist directory.")
        if DIST.exists():
            shutil.rmtree(DIST)
        shutil.move(str(staging), str(DIST))
    print(json.dumps({"build_id": json.loads(files["build.json"])["build_id"],
                      "files": len(files), "individual_svgs": sum(name.startswith("library/svg/") for name in files),
                      "symbol_libraries": sum(name.startswith("exports/") for name in files),
                      "bytes": sum(map(len, files.values())), "directory": str(DIST)}, indent=2))


if __name__ == "__main__":
    build()
