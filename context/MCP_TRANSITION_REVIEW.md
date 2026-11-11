# MCP transition: repository review and development proposal

Reviewed: 11-11-2026. Published `main`: `8af543344773017cd7b2294dbb4fba501ce98eee`.

Scope: repository review, recording the agreed product direction, and proposing a gradual migration. No MCP server, new symbol format, or migration has been implemented. Existing assets and accepted drawing rules are unchanged.

## Agreed direction

The product direction is recorded in [DIRECTION.md](../DIRECTION.md#agreed-first-release-direction). The first release is an agent integration, with MCP as its tool interface and support for Claude Desktop and OpenAI/ChatGPT required from the start. A minimal visual catalogue and a realistic first-time-user workflow are part of that release. A fuller app or web app comes later, using the same underlying library and capabilities.

This is a product requirement, not a claim of current host compatibility. The exact supported OpenAI application surface, installation path, account prerequisites, local/remote transport, and authentication must be checked against current host capabilities and demonstrated before being advertised. The existing Windows Codex installer does not establish ChatGPT Desktop or Claude Desktop support.

The user's desire for standardized grids and compatible symbol connections remains a design goal. No numeric grid, lead pitch, database, server framework, or new profile schema has been selected.

## What was actually reviewed

A clean clone of the published repository contains 148 tracked files. The remote exposed only `main` and no tags at review time. Source, documentation, existing tests, asset inventories, and representative drawings were inspected. This review cannot establish the state of other devices, their unpushed commits, or their untracked/ignored files.

The repository's own [maintenance rules](../agents/PROJECT_RULES.md#context-and-synchronization) were available. The linked external project-workflow repository could not be fetched without authentication; its contents were not assumed.

## Reuse inventory

| Existing material | Verified state | Recommended use |
| --- | --- | --- |
| [Accepted rules](../preferences/GENERAL.md) | Seven accepted rules, each with editable TeX and rendered examples: four connection rules and three symbol rules. | Preserve stable IDs, scope, approval status, evidence, and precedence. Load these through the future library interface. |
| [Ground symbols](../preferences/symbols/ground-symbols/drawing.tex) | A parameterized TikZ macro draws the single bar, open triangle, and PE forms at the accepted wire-relative width. Neither circuit-ground variant is designated default. | Strong first candidate for a reusable symbol definition; extract the macro and add connection anchors, units, bounds, and validation. Preserve both variants without inventing a default. |
| [Supply arrows](../preferences/symbols/power-supply-arrows/drawing.tex) and [signal terminals](../preferences/symbols/signal-terminal-circles/drawing.tex) | Drawing styles and geometry exist inside demonstration sheets. Current SVGs are whole illustrations rather than individual drop-in symbols. | Reuse geometry and examples; produce separate symbol assets and explicit connection metadata when migration is authorized. |
| [Connection examples](../preferences/connections/README.md) | Junction dots, explicit connections, unconnected crossings, and wire thickness have accepted rules and visual evidence. | Reuse as rule demonstrations and targeted regression cases; do not model every rule as a symbol. |
| [AOE collection](../styles/THE_ART_OF_ELECTRONICS/STYLE.md) | 31 reference records: 15 schematics, 15 mixed figures, one plot. Five contain TeX, light/dark SVGs, PNGs, and browsing pages; 26 lack saved images. | Keep all records, captions, feedback, and status. Use available images as style references and visual comparison material. |
| Five AOE recreations | Parallel connection, voltage divider, adjustable divider, Thevenin equivalent, and leading-edge detector. Shapes are traced TikZ paths inside CircuitikZ. | Reuse reference geometry, composition, and visual evidence. They are not a finished semantic component library or proof of reliable AOE generation. |
| [SVG exporter](../scripts/export_svg.py) | PyMuPDF converts a compiled monochrome PDF page to transparent light/dark SVG and optional PNG. It rejects unsupported colors and embedded raster content. | Retain the export stage. Add a reproducible TeX compilation service, dependency setup, errors, timeouts, and bounded execution before exposing rendering through tools. |
| [Preference gallery builder](../scripts/build_preference_galleries.py) | Deterministic, standard-library-only generation with link checks, approval filtering, and tests. AOE galleries are separately authored. | Keep current galleries usable during migration. Extend or adapt the builder for new symbols; it does not currently provide a private user catalogue. |
| [Installed workflow](../skills/schematica-preferences/SKILL.md) and [installer](../INSTALL.md) | A complete local Windows Codex workflow exists, including discovery, approved saves, and checks that uninstalling preserves the library. | Reuse interaction guidance and isolation principles. Keep the existing route working while adding MCP and host-specific setup. |
| [Decision history](LOG.md) | Accepted choices, proposals, rejected variants, and unfinished experiments are recorded. Resistor decisions exist, but no permanent resistor component rule or illustration is tracked. | Preserve history and status; do not silently promote preview choices or infer that missing local preview files are backed up. |

## Repository and preservation recommendation

Keep one Schematica project and one repository. Retain `main` as the current working baseline; it is not yet a release-ready product. Develop new architecture on a branch and merge small, reviewed milestones. A second Git worktree can provide a separate development folder while sharing the same repository and history. It is not a new product or a backup by itself.

Before reorganizing the original checkout:

1. Inspect its status, branches, remotes, unpushed commits, untracked files, and useful ignored files. Do not reset, clean, or move the existing checkout wholesale.
2. Preserve valuable unfinished sources and experiments in appropriate commits or a separate dated archive. The recorded output-stage trial and resistor previews may be in ignored `build/` folders; their presence and recoverability need local verification. Original screenshots may exist outside the repository. Avoid blindly committing all generated files or private inputs.
3. Verify the preserved commits reached the remote, then create a named baseline tag, such as `pre-mcp-baseline`. Verify any non-Git archive separately. A tag protects only committed content, not working files.
4. Create an implementation branch, such as `feature/mcp-foundation`, optionally checked out in a sibling worktree. Give each worktree its own temporary build directory and test-user data. Avoid registering competing global installations.
5. Merge only after the milestone works and its data/compatibility checks pass. Prefer additional short-lived milestone branches to one long-running rewrite. Keep the legacy library readable until replacement and migration are demonstrated.

The baseline tag, PC archive, implementation worktree, and implementation branch are recommendations, not completed actions. This review's documentation branch does not back up work on other devices.

## Proposed first development sequence

### 1. Verify the two host connections

Use a minimal read-only capability to list the existing library and return an accessible preview. Exercise it in both the selected Claude and OpenAI user applications, using documented installation only. Record the supported versions/surfaces and any account or hosting requirements. MCP transport success alone does not prove that preview display and later saves will work in both clients.

### 2. Define one symbol through a working prototype

Use an existing ground-symbol variant, retaining its accepted geometry. Introduce only the fields needed to save, connect, render, and find it: stable identity and revision, source, units, connection anchors, bounds, preview locations, and linked examples/rules. Make grid and lead spacing explicit in this prototype and visually check snapping before adopting a convention for other symbols. Treat these fields as a proposed starting point, not a settled schema.

Keep machine-checkable geometry constraints distinct from textual drawing guidance. A rule may retain interpretive scope; port alignment and output validity need deterministic checks.

### 3. Complete one realistic user journey

In an isolated fictional user's workspace: browse the supplied symbol, create a variant, render it, save it, see it in the catalogue, and reuse it in a new session. Run the same journey through both clients. The catalogue can initially be generated HTML or a simple served page; choose its delivery after the host connection experiment. It must reflect that user's saved data without requiring a GitHub publication.

Keep shipped defaults, user additions/overrides, and generated output distinguishable. The same core library/save/render operations should serve MCP now and a later app. MCP should expose these capabilities, with host-specific instructions kept small. Persistent user data must survive restarting the integration and updating the product.

### 4. Expand only after that journey works

Migrate the remaining existing symbol candidates incrementally. Keep IDs, source attribution, rule approval status, and existing links intact or provide explicit compatibility mappings. Then return to the reusable AOE preset and new-circuit trials already proposed. A fuller visual editor, plot/sketch workflows, and intelligent mixed-output composition can follow.

At each milestone, record the decision and its reason, show the working result, preserve the relevant example, and update [CURRENT.md](CURRENT.md). Carry unfinished ideas forward with their actual status. This avoids both losing ideas and requiring every future product decision upfront.

## Questions intentionally left open

- Local versus hosted service and the precise supported host/transport combination.
- Whether styles fully cover saved visual preference profiles; user identity/workspace ownership still needs separate handling.
- File formats and storage backend; no database is required merely to begin the prototype.
- Numeric grid, anchor conventions, lead pitch, and complete symbol schema.
- Minimal catalogue technology and how each client opens its previews.
- Upgrade/migration packaging and the eventual public distribution model.

## Verification and limits

- `python scripts/build_preference_galleries.py --check`: passed; galleries current and checked local references valid.
- `python -m unittest discover -s tests -v`: seven passed, four Windows-only installer tests skipped on Linux. Eleven tests were discovered, not eleven executed successfully here.
- Exporter smoke test: a temporary monochrome vector PDF produced both SVG themes and PNG with the expected ink colors. This checks export, not schematic correctness or TeX compilation.
- TeX binaries are present in this review environment, but `kpsewhich circuitikz.sty` found no installed CircuitikZ package. No fresh circuit compilation or renderer installation was attempted.
- No live Claude Desktop or ChatGPT integration was tested. No MCP implementation exists in the reviewed repository.
- No PC backup or local worktree verification was performed. Original image gaps and ignored trials remain explicitly unresolved.

The earlier [release-readiness audit](RELEASE_READINESS.md) describes an older commit. Its claims of three rules, no installer, and no tests are superseded by this inventory; its outstanding AOE quality and new-user validation goals remain relevant.
