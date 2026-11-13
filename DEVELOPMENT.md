# Develop Schematica

[Preview](https://schematica-preview.dinodubroja.workers.dev/)
· [Inkscape](docs/INKSCAPE.md)
· [Scope and gaps](docs/ROADMAP.md)
· [Current status](context/CURRENT.md)

## Latest changes

13-11-2026: repository cleanup reviewed and accepted. The accepted interface and
symbol artwork are unchanged. The rebuilt website is byte-identical to published
build **971b3b876b93**.

| Change | Where to check |
|---|---|
| Current app moved out of the old project layout | [app/](app/) |
| Current tests and essential regression inputs separated | [tests/](tests/), [fixture notes](tests/fixtures/README.md) |
| Standalone TeX bundles and ZIPs generated when requested | [Package exports](#package-exports) |
| Legacy instructions, galleries and historical reports archived outside the checkout | [Archive and deliberate reuse](docs/ROADMAP.md#archive-and-deliberate-reuse) |
| One human developer guide, concise project decisions | This page, [decisions](context/DECISIONS.md) |

Run the [review checklist](#test-and-review). Verification results and remaining
device checks are recorded in [current status](context/CURRENT.md).

Verified this run: 25 automated tests; 54 fresh TeX renders; 42 palette comparisons;
nine Inkscape library round trips; all 54 browser configurations; actual single and
six-symbol downloads; documentation links and desktop/narrow layouts. The 486
standalone TeX files and website ZIP match the archived exports. Earlier laptop
checks also reproduced the build and passed focused tests; the complete hosted
checklist, profile-wide Symbols installation and GUI snapping checks remain open.

## Run on Windows

From the repository root, with Python **3.12 or newer**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements.txt
.\app\launch.ps1
```

Open the printed address, normally **http://127.0.0.1:8765/**. Keep the terminal
open; Ctrl+C stops the server. To use another port, run
`.\app\launch.ps1 -Port 8766`. `-NoBrowser` leaves opening the browser to you.
If PowerShell blocks scripts, run the equivalent Python commands:

```powershell
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe app\server.py --open
```

Browsing and packaging existing artwork require only Python and PyYAML. No TeX,
Inkscape, Node.js or Cloudflare account is needed. Open the served address rather
than the HTML file itself. The launcher uses the root `.venv`, then an existing
workspace environment if available, then Python on PATH.

## Get the project on another Windows device

For web testing, open the preview from the GitHub README; no local project is
required. For source work, keep a separate Git checkout on each device, outside
OneDrive. Install [Git for Windows](https://git-scm.com/install/windows) if needed.

First copy, from a local projects folder:

```powershell
git clone https://github.com/DinoDubroja/schematica.git
cd schematica
```

Then follow [Run on Windows](#run-on-windows). The existing laptop checkout was
already set up during the first batch; update that copy instead of cloning again.

Before updating an existing copy, run `git status --short`. If it lists files,
preserve and resolve that work first. If empty, run `git pull --ff-only`. Stop on
divergence; do not overwrite the other device's work. Commit/push reviewed work
before switching devices, and pull before starting on the receiving device. After
this cleanup, use `app\launch.ps1`; the old `implementation\launch.ps1` path is gone.
If the existing preview server holds the old folder open, stop it with Ctrl+C
before pulling, then start it from the new path.
GitHub synchronizes source and docs; Cloudflare is a separate website deployment.
Downloaded SVGs and Inkscape drawings remain local unless separately synchronized.

## Find and edit

```text
schematica/
├── README.md               # Product overview and screenshot
├── DEVELOPMENT.md          # Setup, editing, checks and packaging
├── AGENTS.md               # Instructions for new Schematica
├── app/
│   ├── definitions/        # Names, descriptions, keywords, pins and parts
│   ├── presets.yaml        # Three sizes and three stroke weights
│   ├── tex/                # Authoritative parameterized geometry
│   ├── core.py             # Find, inspect and render; shared TeX export
│   ├── exports.py          # SVG, ZIP, sheet and Symbols composition
│   ├── library/            # Catalog and 54 SVGs for immediate browsing
│   ├── viewer/             # Accepted HTML/CSS/JavaScript interface
│   ├── build_site.py       # Portable website builder
│   ├── build_library.py    # Regenerate artwork after a geometry change
│   ├── package.py          # Generate distributable ZIPs
│   ├── launch.ps1          # Windows entry point
│   ├── server.py           # Local static server
│   └── wrangler.jsonc      # Cloudflare static-asset settings
├── tests/                  # Automated checks, render checks and fixtures
├── docs/                   # Inkscape, roadmap and documentation images
└── context/                # Current status and new-project decisions
```

| Edit | Source | Then |
|---|---|---|
| Layout, controls, dark/light colors | [viewer/](app/viewer/) | Build website, tests, browser checklist |
| Description and search keywords | [definitions/](app/definitions/) | Build website; rebuild artwork to update SVG descriptions too |
| Symbol paths, leads or signs | [tex/](app/tex/) | Full rendering and Inkscape checks |
| Supported sizes/strokes | [presets.yaml](app/presets.yaml) and definitions | Requires an agreed scope change; regenerate and review |
| SVG composition and physical placement | [exports.py](app/exports.py) | Tests and Inkscape checks |
| Packaging and hosting output | [build_site.py](app/build_site.py), [package.py](app/package.py) | Build, package, validate downloads |

![Definitions and TeX feed the renderer, prebuilt library and browser exports](docs/images/pipeline.svg)

The viewer reads pre-rendered SVGs and a catalog. It never compiles TeX. The static
builder copies the accepted artwork, reads current editorial metadata and creates
nine six-symbol libraries. The website contains 71 files, with no Python, source
TeX, references or test material. Its content hashes determine `build.json`.

## Test and review

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\check_docs.py
```

Expect **25 tests, OK**, a **71-file** website and no broken documentation links.
The tests cover accepted paths, dimensions, independent strokes, grid coordinates,
named parts, repeated IDs, export bytes, six distinct symbols per library and HTTP
boundaries. The cleanup should still produce build **971b3b876b93**.

| Action | Expected result |
|---|---|
| Open the app; select an op-amp | Six symbol cards; name, artwork and preview update |
| Switch dark/light; reload after each choice | Theme persists and controls, grid and pins stay readable |
| Search `elliptical`, then `zzzz`, then clear | Coil only; empty result; all six cards |
| Select Coil inductor → Small → Thick | Proportions and stroke update; changing only stroke leaves pins fixed |
| Toggle Grid & pins; expand Description | Both preview aids toggle together; description/keywords are read-only |
| Download the selected coil SVG | Black vector artwork, no grid/blue points; 14.30 × 1.80 mm visual bounds |
| Search `capacitor`, then Export library | All six symbols at Small/Thick, despite the filter |
| Open the library in Inkscape Symbols | Six thumbnails; paste, unlink, edit named parts, save/reopen successfully |
| Tab through controls; use Enter, Escape and `/`; narrow the window | Controls work, dialog returns focus, search focuses, no horizontal overflow |

Repeat on both Windows devices using the same
[fixed hosted version](https://650191bd-schematica-preview.dinodubroja.workers.dev/).
For export and grid details, use [the Inkscape guide](docs/INKSCAPE.md). Record
device/browser, build ID, selected preset, failed action and actual result. A test
on this computer does not establish the laptop's result.

## Render and verify geometry

Only geometry work needs the extra tools:

```powershell
.\.venv\Scripts\python.exe -m pip install -r app\requirements-dev.txt
.\.venv\Scripts\python.exe app\build_library.py
.\.venv\Scripts\python.exe tests\verify_library.py
.\.venv\Scripts\python.exe tests\verify_renderer.py
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\verify_site.py
```

Tectonic and dvisvgm compile the TeX; Inkscape and PyMuPDF independently check the
SVGs. Set `SCHEMATICA_TECTONIC`, `SCHEMATICA_DVISVGM` and `SCHEMATICA_INKSCAPE` to
executable paths when automatic discovery fails. On Windows use `inkscape.com`.

`verify_library.py` checks all 54 SVGs, 42 accepted-palette comparisons, bounds,
named parts and composite save/reopen. `verify_renderer.py` checks a fresh render,
native CircuitikZ and the bounded editable-label fixture. `verify_site.py` checks
all nine Inkscape libraries. Add `--downloads <folder>` to compare real browser
downloads (all nine libraries and `inductor-coil-small-thick.svg`). Results go into
ignored `app/build/` subfolders. Command-line checks do not imply a new GUI check.

The accepted palette is an independent regression reference, not an inherited
legacy style. Update it only after explicit geometry acceptance. Baseline tools:
Python 3.13.5, PyYAML 6.0.3, PyMuPDF 1.27.1, Tectonic 0.17.0+20260731,
dvisvgm 3.6, Inkscape 1.3.2. Tectonic may download its bundle on first use;
fresh-machine/offline rendering remains unverified.

## Package exports

```powershell
.\.venv\Scripts\python.exe app\package.py
```

Creates `app/build/exports/` with a hash manifest and three ZIPs:

| Package | Contents |
|---|---|
| `web-preview.zip` | 71 static website files, ready for Cloudflare upload |
| `all-symbols.zip` | 54 individual SVGs |
| `tex-bundles.zip` | 54 standalone configurations, each with `symbol.tex` and required helpers |

Only the shared TeX recipes/helpers and prebuilt browser SVGs are maintained.
Generated standalone bundles and ZIPs are not committed. To use the native TeX
example, copy [native-circuitikz.tex](tests/fixtures/native-circuitikz.tex) beside
the helpers from [app/tex/](app/tex/), then compile it without the SVG driver.

## Core interface

```powershell
.\.venv\Scripts\python.exe app\core.py find coil
.\.venv\Scripts\python.exe app\core.py inspect opamp --size small --stroke thick
.\.venv\Scripts\python.exe app\core.py render capacitor --output app\build\capacitor
```

Python integrations use `find_symbols`, `get_definition`, `resolve_settings`,
`inspect_symbol`, `render_symbol` and `write_tex_bundle`. Inspection recompiles;
browsing uses the catalog. Stable IDs: `resistor-eu`, `resistor-us`, `inductor-coil`,
`capacitor`, `opamp`, `opamp-supply`, all revision 1. Configuration keys append
size and stroke. `exports.export(kind, keys, columns=3, spacing=6)` supports `svg`,
`zip`, `sheet`, `symbols`; the viewer exposes the two agreed export actions.

## Hosting and documentation previews

The live Cloudflare preview is a separate static upload. No Git auto-deploy is
configured. For an authorized update, build/package/test, then upload
`web-preview.zip` to the existing `schematica-preview` Worker. Record its version
URL and build ID and repeat browser/download checks. The [Wrangler settings](app/wrangler.jsonc)
describe equivalent CLI settings; the dashboard upload does not read that file.

To render these Markdown guides locally, install the developer requirements and run:

```powershell
.\.venv\Scripts\python.exe tests\check_docs.py --render
python -m http.server 8790 --bind 127.0.0.1 --directory app\build\docs
```

Open **http://127.0.0.1:8790/README.html**. Check images, tables, commands and links
at desktop and narrow widths. HTML previews are generated output, not another
documentation source.
