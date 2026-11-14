# Develop Schematica

[Preview](https://schematica-preview.dinodubroja.workers.dev/)
· [Inkscape](docs/INKSCAPE.md)
· [Scope and gaps](docs/ROADMAP.md)
· [Current status](context/CURRENT.md)

## Latest changes

14-11-2026: **batch 02 is in progress**. 12 of 80 new designs are complete;
the current source library has **38 designs / 504 configurations**.
The original 26 designs remain Verified; new designs are Unverified.
Completed families: capacitors, diodes. See the [finite inventory](docs/BATCH_02.md).

Local build: `7342b5918472`. The shared preview remains on the previous
release until the tested batch is published. Family checkpoint commits are pushed
on `work/agent-b-symbols`; main and A's work are not merged by this task.

Checks so far: 47 Python tests, eight JavaScript tests, all declared family
configurations, Inkscape vector bounds and composite save/reopen. Actual renders
were visually inspected at common scale and normal size, including Small/Thick
and every adjustment orientation. All 342 approved SVG bytes and 26 approval
records match the pre-batch baseline. No new design has human approval.

### Test on both Windows devices

Use the shared preview after publication; during development use your local build.

| Action | Expected result |
|---|---|
| Choose a family and its `overnight-…-02` batch | Only that family's new designs appear |
| Open Unverified; search `overnight` | New designs awaiting your review; existing approved designs stay Verified |
| Open Variations, then Small / Thick | All supported settings render; pin identities stay fixed |
| Inspect polarity, arrows and terminal names | Electrical meaning matches the description; report a fix by copied symbol reference |
| Switch dark/light; download one SVG and the library | Usable theme; clean vectors; complete library contains every current design |
| Verify acceptable designs; copy approvals into chat | Browser selections are Pending until the exact approval handoff is applied and published |

No new review sheet or comment UI is added. Review through Unverified and Variations;
send corrections in chat. See [verification](docs/VERIFICATION.md).

## Run on Windows

From the repository root, with Python **3.12 or newer**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements.txt
.\app\launch.ps1
```

Open the printed address, normally **http://127.0.0.1:8765/**. Keep the terminal
open; Ctrl+C stops the server. To use another port, run
`.\app\launch.ps1 -Port 8792`. `-NoBrowser` leaves opening the browser to you.
If Windows blocks the chosen port, try another; 8792 passed on this desktop.
The launcher now reports server-start failures as errors. If PowerShell blocks
scripts, run the equivalent Python commands:

```powershell
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe app\server.py --open
```

Browsing and packaging existing artwork require only Python and PyYAML. No TeX,
Inkscape, Node.js or Cloudflare account is needed. Open the served address rather
than the HTML file itself. The launcher uses the root `.venv`, then an existing
workspace environment if available, then Python on PATH.

## Parallel work

Agent B owns symbol definitions, artwork, metadata, existing-format options and
symbol tests on `work/agent-b-symbols`. Agent A owns MCP, search, creation skills
and shared viewer adaptation on `work/agent-a-integration` in its separate checkout.
The collection is the **dev library**; accounts and personal libraries remain deferred.

The local coordination records live outside Git in the workspace's
`Local/parallel-work/agent-b.md` and `agent-a.md`; each agent edits only its own.
They record actual checkout paths, ports, backups, exact tested commits and open
questions. An absent record means that agent's setup is not yet verified.

- Before work → confirm your checkout and branch, read both available records,
  and preserve local changes. Do not let synchronization switch an owned checkout.
- Before format, rendering, export or viewer changes → describe the proposed
  interface change in your handoff and coordinate with the other owner first.
- Before creation/save tests → use A's separate test library; never the accepted
  library in B's checkout. Builds, environments and preview ports stay separate.
- Before integration → use the exact **READY FOR INTEGRATION** commits and their
  checks. A combines them on its integration branch; B adopts agreed shared
  changes through B's branch. A checkpoint or passing test is not human approval.
- Before publication → B remains the sole shared-preview publisher, within the
  current task's explicit authorization. Keep A's experiments off that preview.

To check this setup: `git branch --show-current` must match your ownership record;
the preview's `build.json` must match your checkout's `app/dist/build.json`.
Run the [existing checks](#test-and-review) after adopting a shared checkpoint.
No new symbol batch or unresolved design is authorized by branch setup.

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
before switching devices, and pull before starting on the receiving device. Use `app\launch.ps1`; the old `implementation\launch.ps1` path is gone.
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
│   ├── library/            # Catalog and 342 SVGs for immediate browsing
│   ├── verification.py     # Validate and apply chat approval handoffs
│   ├── verification.json   # Official acceptance, tied to actual geometry
│   ├── viewer/             # Accepted HTML/CSS/JavaScript interface
│   ├── build_site.py       # Portable website builder
│   ├── build_library.py    # Render candidates before promotion
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
36 complete-library exports. The website contains 388 files, with no Python, source
TeX, references or test material. Its content hashes determine `build.json`.

## Test and review

Run from the repository root. Node.js **20 or newer** is needed only for the
browser-state tests; the app itself has no Node dependency.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests\review.test.cjs tests\configurations.test.cjs
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\check_docs.py
```

Expect **47 Python tests and 8 JavaScript tests**, a **550-file** website, and no
broken documentation links. Tests cover all designs/configurations, accepted SVG
bytes, pins, independent strokes, editable parts, exports, HTTP boundaries and
approval validity. Compare `app/dist/build.json` with the hosted `build.json` when
checking that both devices have the same version.

| Action | Expected result |
|---|---|
| Open the app; switch All symbols / Unverified | 31 designs / 5 unverified designs; the original 26 remain Verified |
| Choose Resistors / Batch 01; search `NTC`, then `zzzz`, then clear | Two NTCs; empty state; the filtered batch returns |
| Select Variable resistor · US; open Variations | Stroke, Size and Arrow orientation rows; one setting varies per row, all others at defaults; no large preview |
| Choose Small / Thick / Down-left; open Variations | Comparison rows still use defaults, independently of the main preview selection |
| Try all orientations on variable/trimmer US/EU | Only the diagonal marking reflects; body, leads and blue pin identities stay fixed |
| Inspect potentiometers, NTC/PTC, photos and nonlinear resistors | Wiper tip centered 1 mm above body; labels readable; arrows symmetric; diagonal S has no arrowhead; no varistors |
| Check a design; reload | Pending in this browser; selection and exact design identity persist |
| Verify & next, then Undo | Selects the next unreviewed design; Undo reverses the pending selection |
| Copy approvals or Copy symbol reference | Approval JSON includes exact revision/fingerprint; reference includes name/ID/revision/link |
| Open the reference link in another browser | Same design selected; local approvals are not transferred |
| Switch dark/light; reload; use Small/Thick and Grid & pins | Theme persists; stroke changes keep pins fixed; preview aids toggle together |
| Export Small/Thick/Down-left variable resistor, then the library while filtered | Single matches the selected marking; library has all 38 designs and Down-left on its four adjustable designs |
| Select a coil; export the library | Orientation controls disappear; adjustable designs in the library use Up-right |
| Inspect exported artwork | Black vectors, no blue points/grid; NTC/PTC glyph outlines stay grouped as temperature-mark |
| Open the library in Inkscape Symbols | 38 thumbnails; placed artwork can be unlinked, edited, saved and reopened |
| Use Tab, Enter, Escape, arrow keys on the tabs, and `/`; narrow the window | Controls remain reachable; dialogs return focus; search focuses; page does not overflow |

Repeat on both Windows devices using the [shared preview](https://schematica-preview.dinodubroja.workers.dev/).
Record device/browser, build ID, design reference, selected preset, failed action
and actual result. See [Inkscape](docs/INKSCAPE.md) for export/grid details and
[verification](docs/VERIFICATION.md) for approval handoff and clipboard fallback.

## Render and verify geometry

Only geometry work needs Tectonic, dvisvgm, Inkscape and the developer requirements.
Build candidates separately from the browsable library:

```powershell
.\.venv\Scripts\python.exe -m pip install -r app\requirements-dev.txt
.\.venv\Scripts\python.exe app\build_library.py --output app\build\candidates\current
$env:SCHEMATICA_LIBRARY = (Resolve-Path app\build\candidates\current).Path
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\verify_library.py
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\verify_site.py
.\.venv\Scripts\python.exe tests\verify_renderer.py
.\.venv\Scripts\python.exe app\server.py --port 8792
```

Inspect the candidate viewer at **http://127.0.0.1:8792/** and follow the
[creation workflow](docs/RESISTOR_BATCH.md#repeatable-creation-workflow). The renderer
excludes a design if any configuration fails and reports it in
`app/build/library-measurements.json`. Fix and repeat before promotion. Do not edit
generated SVGs as the drawing authority.

After technical and visual checks pass, stop that test server and promote only the
checked candidate output. Preserve concurrent edits before copying. Compare the
catalog file list with `app/library/svg/`; remove only backed-up obsolete SVGs
inside that folder (for example, removed designs or superseded optionless keys):

```powershell
# Back up the existing library first. Check the candidate and current status.
Copy-Item "$env:SCHEMATICA_LIBRARY\svg\*.svg" app\library\svg\
Copy-Item "$env:SCHEMATICA_LIBRARY\catalog.json" app\library\catalog.json
Remove-Item Env:SCHEMATICA_LIBRARY
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

NTC/PTC rendering retrieves Latin Modern Sans from the same cached Tectonic bundle
and gives dvisvgm a local font file; exported SVGs contain glyph outlines. Native
TeX uses the explicit font file with Tectonic/XeTeX. First use can require network
access to the TeX bundle; no font installation is required for browsing.

Set `SCHEMATICA_TECTONIC`, `SCHEMATICA_DVISVGM` and `SCHEMATICA_INKSCAPE` to executable
paths if discovery fails. On Windows use `inkscape.com`. The optional
`--symbols <ids...>` builds selected candidates for diagnosis; it does not merge
partial catalogs into the supplied library.

`verify_library.py` checks every SVG in Inkscape, 42 comparisons against the six
accepted palette designs, margins, named parts and composite save/reopen.
`verify_renderer.py` checks fresh compilation, native CircuitikZ and a bounded
editable-label fixture. `verify_site.py` checks all 36 complete-library exports;
add `--downloads <folder>` to compare actual browser downloads (36 libraries,
`inductor-coil-small-thick.svg`, and any other supplied single-symbol SVGs). Results go into ignored `app/build/` folders.
Command-line checks do not imply a GUI check.

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
| `web-preview.zip` | 550 static website files, ready for Cloudflare upload |
| `all-symbols.zip` | 504 individual SVGs |
| `tex-bundles.zip` | 504 standalone configurations, each with `symbol.tex` and required helpers |

Only the shared TeX recipes/helpers and prebuilt browser SVGs are maintained.
Generated standalone bundles and ZIPs are not committed. To use the native TeX
example, copy [native-circuitikz.tex](tests/fixtures/native-circuitikz.tex) beside
the helpers from [app/tex/](app/tex/), then compile it without the SVG driver.

## Core interface

```powershell
.\.venv\Scripts\python.exe app\core.py find coil
.\.venv\Scripts\python.exe app\core.py inspect opamp --size small --stroke thick
.\.venv\Scripts\python.exe app\core.py render capacitor --output app\build\capacitor
.\.venv\Scripts\python.exe app\core.py render resistor-variable-us --size small --stroke thick --option orientation=down-left
```

Python integrations use `find_symbols`, `get_definition`, `resolve_settings`,
`inspect_symbol`, `render_symbol` and `write_tex_bundle`. Inspection recompiles;
browsing uses the catalog. Stable IDs and revisions live in YAML; the [batch inventory](docs/RESISTOR_BATCH.md)
lists the resistor IDs. Configuration keys append size/stroke and declared options
(for example `resistor-variable-us-small-thick-orientation-down-left`). Unsupported
option values are rejected. `exports.export(kind, keys, columns=3, spacing=6)` supports `svg`,
`zip`, `sheet`, `symbols`; the viewer exposes the two agreed export actions.

## Hosting and documentation previews

The shared preview is a separate static deployment; Git pushes do not deploy it.
Prefer [Wrangler](https://developers.cloudflare.com/workers/wrangler/commands/general/)
for authorized publications. Build once, deploy, then compare the hosted `build.json`,
catalog and downloads against the local build. Routine publishing needs no automated
browser session or repeated Inkscape export checks.

This workstation has a portable Wrangler 4.162.0 installation outside the repository:

```powershell
.\.venv\Scripts\python.exe app\build_site.py
node ..\Local\tools\cloudflare\wrangler\node_modules\wrangler\bin\wrangler.js deploy --config app\wrangler.jsonc
```

On another publishing workstation, install Node.js 22.12 or newer with npm, then:

```powershell
npx wrangler@4.162.0 login --use-keyring --scopes account:read user:read workers:write workers_scripts:write
npx wrangler@4.162.0 deploy --config app\wrangler.jsonc
```

Login opens Cloudflare for the user to authorize. Credentials stay in Wrangler's
encrypted store with its key in Windows Credential Manager; do not put tokens in
chat or Git. The laptop needs no Cloudflare login merely to browse or run locally.
The [configuration](app/wrangler.jsonc) targets the existing `schematica-preview`
Worker; keep its name and preview URL. Record the deployed version and build ID.

To render these Markdown guides locally, install the developer requirements and run:

```powershell
.\.venv\Scripts\python.exe tests\check_docs.py --render
python -m http.server 8790 --bind 127.0.0.1 --directory app\build\docs
```

Open **http://127.0.0.1:8790/README.html**. Check images, tables, commands and links
at desktop and narrow widths. HTML previews are generated output, not another
documentation source.
