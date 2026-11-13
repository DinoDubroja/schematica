"""Create website, individual-SVG and standalone-TeX ZIPs on demand. No upload."""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

from build_site import payload
from core import ROOT, write_tex_bundle
from exports import LIBRARY, catalog


def write_archive(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, body in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, body)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(files)
        for name, body in files.items():
            assert archive.read(name) == body, name
    return {"files": len(files), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def package():
    output = ROOT / "build/exports"
    output.mkdir(parents=True, exist_ok=True)
    items = [c for s in catalog()["symbols"] for c in s["configurations"]]
    report = {"web-preview.zip": write_archive(output / "web-preview.zip", payload())}
    svgs = {f"{c['key']}.svg": (LIBRARY / c["svg"]).read_bytes() for c in items}
    report["all-symbols.zip"] = write_archive(output / "all-symbols.zip", svgs)
    with tempfile.TemporaryDirectory(prefix="tex-export-", dir=ROOT / "build") as temporary:
        source = Path(temporary)
        for config in items:
            write_tex_bundle(config["symbol_id"], config["size"], config["stroke"],
                             source / config["key"])
        files = {p.relative_to(source).as_posix(): p.read_bytes()
                 for p in source.rglob("*") if p.is_file()}
        report["tex-bundles.zip"] = write_archive(output / "tex-bundles.zip", files)
    (output / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"directory": str(output), "archives": report}, indent=2))
    return report


if __name__ == "__main__":
    package()
