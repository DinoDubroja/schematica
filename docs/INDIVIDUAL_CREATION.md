# Create one symbol

The agent interprets text and accessible reference images, waits for confirmation,
renders parameterized TeX, shows the shared viewer, offers two alternatives and
saves only on request. Search and production batches remain separate workflows.
Use [the creation skill](../.agents/skills/schematica-create/SKILL.md).

## Tools and state

`prepare_creation` → optional `attach_reference_image` / `read_reference_image`
→ user confirmation → `confirm_creation` → `render_creation` → user review and
save request → `save_creation` → `search_symbols` / `get_symbol`.

The interpretation includes `meaning`, `elements`, `terminals`, `labels` and
`options`; say `none` explicitly where appropriate. Necessary uncertainties block
confirmation. The server binds confirmation to the current interpretation digest;
the agent remains responsible for recording a real user response. A token cannot
prove that the user actually said the quoted text.

Pictures, screenshots and sketches use the same image path. The host must expose
their pixels to the agent for interpretation/OCR. Optional persisted references
accept PNG, JPEG and WebP up to 8 MiB; unsupported or inaccessible files need a
supported attachment. No external OCR service or image account is introduced.

## Drawing contract

The existing YAML semantics, part IDs, connection IDs, preset names and catalog
configuration format are retained. Individual creation uses `recipe: custom` and
a separate authoritative `custom.tex` file. Python packages converter output; it
does not draw symbol paths. All three sizes and three strokes are independent.

Use `get_drawing_source` for an existing symbol's definition and a parameterized
TeX wrapper. For a new design, use the same schema as
[the isolated test definition](../tests/fixtures/individual-ground.json) and
[its TeX recipe](../tests/fixtures/individual-ground.tex). These fixtures are
technical tests, not accepted production designs or default ground styling.

The recipe defines exactly `\newcommand{\SCCustom}[3]{...}`. Arguments are the
instance identifier, size factor and stroke width in millimetres. Reuse
`\SCresolve`, `SCpart`, `\SCpin` and `\SCdimension`, with drawing coordinates
resolved in TeX. Pins must lie on the 1 mm grid. Name every graphical part.
The accepted built-in drawing macros may be called from this wrapper.

Named options have `name`, `default`, `values` (`id`, `name`) and
`affected_parts`. `\SCoption{option-id}` expands to the zero-based index in
`values`; use `\ifcase ... \or ... \fi` inside the affected part. Define
2–8 values per option, up to 288 total configurations. These explicit prototype
bounds keep exhaustive rendering practical; larger option products need a scoped
implementation change, not silent partial validation.

Supported drawing commands are a bounded TikZ/TeX subset, checked by
[the custom renderer](../app/custom_renderer.py). Arbitrary packages, file IO,
shell commands and dynamically constructed commands are not supported. Compilation
also uses Tectonic's untrusted mode. This is a local tool for one symbol, not a
general TeX execution service or unrestricted symbol editor.

## Validation, refinement and storage

Every configuration must compile, produce valid packaged SVG, emit the exact
declared parts/pins and keep terminals on-grid. Options and stroke changes preserve
terminal positions. Option changes are checked against declared affected parts.
Refining a saved symbol advances its revision and preserves unaffected geometry
and connection identities. A draft refinement uses `source_draft_id`; prior
rendered artifacts remain recoverable. Alternatives are proposals only.

The active integration store is explicitly initialized under this checkout's
`app/build/`; startup rejects redirected or foreign locations. It holds immutable
render directories and SQLite metadata for drafts, search sessions and saved dev
revisions. Ordinary search includes saved revisions, never unsaved drafts. The
repository library and official verification ledger are read only to MCP tools.
Saved material remains Unverified; real approval uses the existing
[verification workflow](VERIFICATION.md).

Keep this local data across server restarts. It is ignored by Git and is **not**
backed up or synchronized by a checkpoint commit. Production storage, cloud
publication and moving reviewed material into the default library remain separate
handoffs. Do not point tests at another agent's library.
