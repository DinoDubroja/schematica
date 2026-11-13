Historical checkpoint before the browsing UI revision. See [the current review](../CHECKPOINT.md).

# First batch — ready for review, 13-11-2026

**Completed and locally verified. Stop for user review before commit or publication.**

The user accepted the two-symbol rendering proof and authorized: “Continue with the
remaining four appearances, all 54 configurations, and the local viewer and exports.
Stop for my review before committing or publishing.” During implementation the user
also requested working dark mode and a polished interface from the start. Those
changes are included. The original proof checkpoint is retained separately in
[the historical record](../review/rendering-proof-checkpoint.md) and its original ZIP.

## Completed

Six revision-1 YAML definitions and authoritative parameterized TeX recipes produce
all 54 configurations. Size remains independent of stroke: 75/100/125% and
0.15/0.20/0.30 mm, with the accepted 1 mm grid and Medium/Medium initial selection.
The three-pin op-amp has no hidden supply semantics. Source geometry is preserved.

The local viewer groups configurations under six searchable cards, with metric-grid
inspection, named pins/parts/dimensions, preset selection and collected exports.
Dark mode is the initial theme; a visible switch persists the chosen theme. Both
light and dark layouts were reviewed. Four export formats work: individual SVG,
selected SVG ZIP, automatically arranged sheet (columns/spacing), and Inkscape
Symbols library. All exports use original physical scale and omit inspection aids.

[README.md](../README.md) provides local setup, launch, build and integration commands.
The loopback viewer is available at `http://127.0.0.1:8765/` while running; the
Windows launch helper can restart it or open an existing instance. No hosting or
application connections are involved.

## Verification evidence

- All 54 configurations compiled and rendered in Inkscape. Source checks verified
  preset geometry, stroke independence, named parts and on-grid pins. Minimum
  exported page margin: **0.999986 mm**.
- Forty-two comparisons against the accepted palette (36 unique configurations,
  all six Small/Thick cases) measured a maximum coordinate deviation of
  **0.001234 mm** and stroke deviation of **0.000002124 mm**. The full sheet was
  visually inspected for clipping, crowding and broken curves/marks.
- All 54 configurations in both arranged and Symbols sheets retained named parts,
  readable labels and valid unique references through Inkscape save/reopen.
- The browser journey searched appearance attributes, inspected pins, changed size
  and stroke, collected three configurations and downloaded all four export types.
  The sheet used two columns and 8 mm spacing. Actual downloads match the core's
  expected output, including an SVG downloaded while dark mode was active.
- Inkscape GUI opened the downloaded Symbols library. Its Small/Thick coil was
  pasted into a fresh document at **14.300 × 1.800 mm** including stroke, saved as
  a clone, unlinked, and its named `body` selected in Layers and Objects. All three
  named parts survived a separate save, close and reopen. The placed artwork's
  maximum coordinate deviation was **0.000882 mm** after PDF quantization.
- Theme switching and reload persistence worked in both directions. Search, type
  filters, empty results, grid toggle, selection and downloads worked. Layouts were
  checked at 1280, 1000 and 390 px widths, with no horizontal overflow observed.
  Browser console errors: none observed.
- **22 focused automated tests passed**, covering core validation, all presets,
  preserved accepted paths, duplicate references, export composition, spacing,
  HTTP request errors, local-origin checks and restricted file serving.
- The accepted proof's editable Arial text fixture and native CircuitikZ compatibility
  fixture remain available. The native fixture was regenerated with the complete
  helper set; all 54 standalone TeX configurations compiled through the same core.

Evidence: [library measurements](../review/library-measurements.json),
[palette/save/reopen checks](../review/library-verification.json),
[browser and placement checks](../review/browser-checks.json),
[named-part screenshot](../review/inkscape-coil-parts.jpg),
[reopened coil](../review/browser-exports/placed-coil-editable.svg), and
[earlier text/clearance checks](../review/inkscape-checks.json).

## Review outputs and measured cost

Review [the complete 54-cell proof](../review/library-proof.png),
[the dark viewer](../review/viewer-dark.jpg), [the light viewer](../review/viewer-light.jpg),
and use the local catalogue to inspect presets and exports. Download
[all individual SVGs](../review/all-symbols.zip), [the arranged sheet](../review/library-sheet.svg),
[the complete Symbols library](../review/library-symbols.svg), or
[the full local package](../review/first-batch.zip).

The recorded full run took **39.4221 s** compiling and **1.5657 s** converting:
**40.9878 s** combined, about **0.759 s/configuration**. Individual SVGs occupy
**1,863–3,462 bytes**. This excludes installation, initial bundle downloads, PNG
creation, browser/GUI testing and verification; it is not a cold-start benchmark.

## Remaining limits and approval boundary

Awaiting the user's final appearance and usability review. No further library
expansion, commit, push or publication is authorized by this checkpoint.
Connections, personal variants, full schematics and simulation remain deferred.

Editable text is demonstrated only for one installed Arial label; arbitrary fonts,
editable math and other operating systems remain untested. Inkscape instances must
be unlinked before internal part editing. Inkscape can change XML IDs, but semantic
part values and labels are preserved. SVG edits do not synchronize back to TeX/YAML.
Selections are not persisted across reloads. A disabled browser storage policy
prevents remembering the theme but does not prevent switching during the session.
The converter's supported transform/reference forms are deliberately bounded.

Before implementation, the full old checkout was backed up and all 2,282 file hashes
verified, including Git history and uncommitted work. The accepted rendering-proof
ZIP was separately backed up before expansion. Existing unrelated/concurrent work
was preserved. This implementation and its context notes are saved locally only.
