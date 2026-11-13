"""Check local Markdown links; optionally render portable documentation previews."""
import argparse
import html
import os
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

from support import REPOSITORY, APP


def source_files():
    files = list(REPOSITORY.glob("*.md"))
    generated = {"build", "dist", "__pycache__", ".venv", ".wrangler", "node_modules"}
    for folder in ("app", "tests", "docs", "context"):
        for directory, directories, names in os.walk(REPOSITORY / folder, followlinks=False):
            directories[:] = [name for name in directories if name not in generated]
            files.extend(Path(directory) / name for name in names if not name.endswith(".pyc"))
    return sorted(files)


def without_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def anchors(text):
    found = set(re.findall(r'\bid=["\']([^"\']+)', text))
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", without_code(text), re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug if not count else f"{slug}-{count}")
    return found


def check(files):
    count, errors = 0, []
    for path in files:
        if path.suffix != ".md":
            continue
        content = path.read_text(encoding="utf-8")
        targets = re.findall(r"\]\(([^)]+)\)", without_code(content))
        for target in targets:
            target = target.strip("<>").split(' "')[0]
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path
            count += 1
            if not destination.is_relative_to(REPOSITORY) or not destination.exists():
                errors.append(f"{path.relative_to(REPOSITORY)}: missing {target}")
            elif url.fragment and destination.suffix == ".md":
                if unquote(url.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                    errors.append(f"{path.relative_to(REPOSITORY)}: missing anchor {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Documentation: {count} local links/anchors checked, no failures.")


def render(files):
    try:
        import markdown
    except ImportError as exc:
        raise SystemExit("Install app/requirements-dev.txt to render Markdown previews.") from exc
    output = APP / "build/docs"
    if output.is_symlink() or output.is_junction() or output.resolve() != APP.resolve() / "build/docs":
        raise SystemExit("Refusing to replace a redirected documentation output directory.")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    css = """body{margin:0;background:#f4f6f8;color:#20272e;font:16px/1.65 'Segoe UI',Arial,sans-serif}
main{max-width:960px;margin:32px auto;padding:32px 44px;background:white;border:1px solid #dce2e6;border-radius:12px}
nav{font-size:14px;padding-bottom:18px;border-bottom:1px solid #dce2e6}h1{font-size:34px;line-height:1.2}h2{margin-top:36px;font-size:23px}
a{color:#0965a7;text-underline-offset:3px}img{display:block;max-width:100%;height:auto;border-radius:6px}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;border:1px solid #dce2e6;padding:9px 12px}th{background:#f2f5f7}
pre{padding:16px;background:#f2f5f7;border-radius:6px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.5}code{font-family:Consolas,monospace;font-size:.9em}p,li,td{overflow-wrap:anywhere}
@media(max-width:650px){main{margin:0;padding:20px;border:0;border-radius:0}h1{font-size:29px}table{font-size:12px}th,td{padding:7px}}
@media(prefers-color-scheme:dark){body{background:#10151b;color:#e2e7eb}main{background:#171e26;border-color:#384450}nav,th,td{border-color:#384450}pre,th{background:#222c36}a{color:#85caff}}
"""
    (output / "docs-preview.css").write_text(css, encoding="utf-8")
    for source in files:
        relative = source.relative_to(REPOSITORY)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix != ".md":
            shutil.copy2(source, destination)
            continue
        body = markdown.markdown(source.read_text(encoding="utf-8"),
                                 extensions=["tables", "fenced_code", "toc"])
        body = re.sub(r'href="([^":?#]+)\.md([#?][^"]*)?"',
                      lambda m: f'href="{m[1]}.html{m[2] or ""}"', body)
        prefix = "../" * (len(relative.parts) - 1)
        title = html.escape(source.stem)
        document = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Schematica · {title}</title><link rel="stylesheet" href="{prefix}docs-preview.css"><main><nav><a href="{prefix}README.html">Schematica</a> · <a href="{prefix}DEVELOPMENT.html">Development</a> · <a href="{prefix}docs/ROADMAP.html">Roadmap</a></nav>{body}</main></html>'
        destination.with_suffix(".html").write_text(document, encoding="utf-8")
    print(f"Rendered documentation: {output / 'README.html'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    options = parser.parse_args()
    files = source_files()
    check(files)
    if options.render:
        render(files)
