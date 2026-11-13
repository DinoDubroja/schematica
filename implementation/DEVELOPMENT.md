# Development

**Start with [the current review](CHECKPOINT.md): what changed, exact checks,
expected results and verified limits.** Update that page after every implementation
run. A passing automated test is not a substitute for clear review instructions.

## Get the project on another Windows device

To browse/test the published app, open the web preview from the repository README.
No project download, Python installation or Cloudflare account is needed.

To work on the source, use a Git checkout outside OneDrive. These commands run in
PowerShell and require Git. If Git is not recognized, install it from
[Git for Windows](https://git-scm.com/downloads/win) first.

**If the project is already on the laptop:** open PowerShell inside its repository
folder (the one containing README.md and AGENTS.md), then run:

```powershell
git status --short
```

If this prints any files, preserve that work and resolve it before updating. If it
prints nothing, run:

```powershell
git pull --ff-only
```

If Git reports a conflict or divergent history, stop and ask for help; do not reset
or overwrite files. A successful update includes the `implementation` folder and
the README's web-preview and testing links.

**If this is the first copy:** create/open your local projects folder, then run:

```powershell
git clone https://github.com/DinoDubroja/schematica.git
cd schematica
```

Do not clone into or extract a ZIP over an existing checkout. Open the resulting
`schematica` folder in your development app. For local browsing, follow the setup
below from its `implementation` folder.

Before switching devices, commit and push the completed source changes. On the
receiving device, check for local edits and pull before starting. Work on one
device at a time until the previous changes are synchronized. GitHub carries the
source and docs; Cloudflare serves the last separately published website. Downloaded
SVGs and Inkscape drawings are local files unless you save them in a folder that
synchronizes on both devices.

## Open the viewer on Windows

From the repository's `implementation` folder:

```powershell
.\launch.ps1
```

Open the printed address, normally http://127.0.0.1:8765/. Leave the terminal running;
Ctrl+C stops it. If that port belongs to another application, use
`.\launch.ps1 -Port 8766`. Do not open the HTML file directly.

First-time setup requires Python 3.12 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\launch.ps1
```

The launcher uses this environment when present and rebuilds the static website.
TeX and Inkscape are not needed for browsing or packaging the existing artwork.

## Quick checks after a UI or export change

```powershell
.\.venv\Scripts\python.exe build_site.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: **25 tests, OK**; 54 individual SVGs and nine libraries in a 71-file
website. Tests cover preset geometry, named parts, duplicate references, six distinct
symbols per library, byte-identical individual artwork, repeatable builds and HTTP
file serving. The generated build ID identifies exactly which website was tested.
Git preserves the implementation files byte for byte, including line endings,
so a Windows checkout reproduces the published artwork and build ID.

Then follow the numbered browser/Inkscape checklist in [CHECKPOINT.md](CHECKPOINT.md).
Record the browser and Inkscape versions, build ID, pass/fail, and untested steps.
For a failure, record the selected symbol/size/stroke and what happened instead of
the expected result. Keep screenshots only where they explain an issue or review.

## Test on the second Windows device

Open [this fixed review version](https://650191bd-schematica-preview.dinodubroja.workers.dev/)
on both devices. [Build information](https://650191bd-schematica-preview.dinodubroja.workers.dev/build.json)
must show `971b3b876b93`. Each browser remembers its
own theme; no preferences synchronize between devices. Run the current review
checklist on each device. A browser is enough to test the UI; install Inkscape only
for the export checks. Do not mark device two as passed based on device one.

For offline/local testing, the same build can be checked by transferring
`review/web-preview.zip`, extracting it, and serving that extracted folder:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Run this command **inside the extracted website**, then open the printed localhost
address. It needs Python but no packages. This is a local fallback, not the shared
preview. Repository changes remain unsynchronized until a commit/push is approved.

## Build and hosting

```text
implementation/
├── definitions/        # Symbol descriptions, keywords, pins and parts
├── presets.yaml       # Independent size and stroke choices
├── tex/               # Authoritative symbol geometry
├── core.py            # Render, inspect and find symbols
├── exports.py         # Compose existing SVG artwork at physical scale
├── library/           # Generated catalog, 54 SVGs and matching TeX bundles
├── viewer/            # Browser interface
├── build_site.py      # Build website and nine six-symbol libraries
├── dist/              # Generated website only; ignored by Git
├── wrangler.jsonc     # Cloudflare configuration; no account or credentials
├── tests/             # Core, export and portable-site checks
└── review/            # Review evidence and portable website ZIP
```

`build_site.py` uses an explicit file list. It includes no source code, TeX bundles,
reference material, logs or review evidence in the hosted website. It recreates
`dist/` and `review/web-preview.zip`; edit sources instead. `build.json` records
content hashes, without machine paths or timestamps. `server.py` serves this same
output locally with only Python's standard library. There is no export API or
server-side renderer in the website.

Cloudflare Workers Static Assets hosts the preview, public to anyone with its URL
without login. Search-engine exclusion is requested; the URL is not private.

- [Main preview](https://schematica-preview.dinodubroja.workers.dev/)
- [Fixed version 650191bd](https://650191bd-schematica-preview.dinodubroja.workers.dev/)
- Build: `971b3b876b93`, published 13-11-2026 after explicit approval.

This deployment used **Workers & Pages → Create app → Upload your static files**
with `review/web-preview.zip` (71 files), Worker name `schematica-preview`, assets
directory `/`, HTML handling `auto-trailing-slash` and not-found handling `none`.
Production and Preview URLs are enabled. No Git integration or automatic publishing
was configured. Dashboard upload does not read `wrangler.jsonc`; it retains the
equivalent settings for later CLI use. Wrangler was not installed or run.

For an approved update, rebuild/test locally, then open the existing Worker and use
its static-file upload to deploy the new ZIP. Record the new version URL and build
ID, compare the hosted manifest and actual downloads, then repeat the browser
checklist. Do not create another Worker for each update. Keep GitHub as the source
repository; commits/pushes and future publication need their own authorization.

The first address briefly returned a TLS error while activating, then opened
normally. Python `urllib` requests received Cloudflare 403/error 1010; use the
browser checklist and actual downloads for this preview. The hosted all-file and
response-header sweep remains unverified; no security settings were weakened.

[Cloudflare static hosting](https://developers.cloudflare.com/workers/static-assets/get-started/)
· [Headers](https://developers.cloudflare.com/workers/static-assets/headers/)
· [Fixed version URLs](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/)

## When symbol geometry changes

Do not rebuild accepted geometry for a CSS-only change. Edit parameterized TeX,
not generated paths. Python packages converter output; it must not redraw symbols.
Editorial descriptions/keywords live in YAML. The static builder reads them directly;
rebuild the library when exported SVG descriptions also need refreshing.

Rendering needs `requirements-dev.txt`, Tectonic, dvisvgm and Inkscape. Set executable
paths with `SCHEMATICA_TECTONIC`, `SCHEMATICA_DVISVGM`, `SCHEMATICA_INKSCAPE` when they
are not found automatically. On Windows choose `inkscape.com` for command-line work.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe build_library.py
.\.venv\Scripts\python.exe verify_library.py
.\.venv\Scripts\python.exe build_site.py
.\.venv\Scripts\python.exe verify_site.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`verify_library.py` renders all 54 configurations, compares accepted palette geometry
and checks named parts through Inkscape save/reopen. Inspect
`review/library-proof.png` for clipping, signs, coil curves and pin alignment.
`verify_site.py` checks the website hashes and all nine six-symbol libraries through
Inkscape save/reopen, including physical page size and clipping. Add
`--downloads <folder>` to compare your nine library downloads and Small/Thick coil
against the build; keep their original filenames in that folder.
`verify_inkscape.py` and `verify_browser_exports.py` validate retained earlier GUI
fixtures; they do **not** perform a new browser/GUI journey.

Verified renderer baseline: Python 3.13.5, PyYAML 6.0.3, PyMuPDF 1.27.1,
Tectonic 0.17.0+20260731, dvisvgm 3.6 and Inkscape 1.3.2. First-time Tectonic use can
require a bundle download. Clean-machine/offline rebuilding is not yet verified.

## Agent integration

```powershell
python core.py find "coil"
python core.py inspect opamp --size small --stroke thick
python core.py render capacitor --size medium --stroke medium --output build/custom-export
```

Use `find_symbols`, `get_definition`, `resolve_settings`, `inspect_symbol` and
`render_symbol` from the Python core. Inspection recompiles; the viewer uses the
prebuilt catalog. IDs are `resistor-eu`, `resistor-us`, `inductor-coil`, `capacitor`,
`opamp`, `opamp-supply`; configuration keys append size and stroke.

`exports.export(format, configuration_keys, columns=3, spacing=6)` retains agent-side
`svg`, `zip`, `sheet` and `symbols` composition. Only single SVG and the six-symbol
library are exposed in the viewer. Use unique instance prefixes when composing SVG.

Each `library/tex/<configuration>/` contains `symbol.tex` and its helpers. For native
TikZ/CircuitikZ, load `schematica`, omit the SVG driver and `\SCsvgtrueexport`, and
call the matching macro, e.g. `\SCInductorCoil{L1}{1}{0.20}`. See
[the native example](review/tex/native-circuitikz.tex). SVG edits do not update TeX/YAML;
the three-pin op-amp defines no hidden-supply electrical behavior.
