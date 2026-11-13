# Rendering proof — ready for review, 13-11-2026

Historical checkpoint; superseded by [the current review](../CHECKPOINT.md).

The user authorized local implementation with a mandatory stop after the two-symbol
rendering proof. Visual acceptance is pending. The full library and viewer have not
started. No commit or publication is authorized.

Accepted settings: 1 mm connection grid; Small/Medium/Large 75/100/125%; stroke
Thin/Medium/Thick 0.15/0.20/0.30 mm, initially Medium/Medium. Independent size and
stroke supersede blanket wire-relative normalization for this implementation.
The preserved accepted palette's geometry and grid calculations are authoritative;
its old draft captions predate acceptance.

Before implementation, a complete local snapshot was copied and all 2,282 file
hashes verified. Git fsck passed (unreferenced historical blobs were retained).
The six pre-existing modified files and ignored/untracked build work were included.
Backup recovery details belong to the local workspace backup manifest.

**Technical checkpoint complete; user visual review pending. Stop here.**

The current user boundary is: “show me the completed rendering proof and stop
for my review before expanding the library or building the viewer.”

## Completed

Two revision-1 YAML definitions, shared presets, parameterized TeX recipes,
reusable find/inspect/render core, generated TeX bundles and 18 SVG configurations.
The pipeline uses Tectonic XDV → dvisvgm → packaging, retaining converter geometry
with shallow named parts. XDV is the XeTeX extension of DVI; there is no second
symbol-drawing backend.

Review the [sheet](proof.png), [editable SVG](proof.svg), and
[Symbols library](symbols.svg). [README.md](../README.md) documents setup,
commands, actual dependency versions, editing steps and the integration interface.

## Verified

- All 18 configurations retain expected physical dimensions, 1 mm grid pins and
  0.15/0.20/0.30 mm strokes. Changing stroke leaves paths, dimensions and pins
  unchanged. Each export has approximately 1 mm of unclipped page margin.
- Fourteen comparisons against the accepted PDF (12 unique configurations,
  including Small+Thick) found maximum coordinate deviation **0.001955 mm** and
  stroke deviation **0.000002124 mm**. The 0.005 mm comparison tolerance allows
  Inkscape/Cairo PDF coordinate quantization.
- Small+Thick op-amp signs retain approximately **0.359 mm** clear space from the
  triangle after accounting for stroke. The complete sheet was inspected.
- Named-body selection through Inkscape's command interface, an attribute edit,
  save/reopen, and preservation of all eight named parts passed.
- Inkscape GUI: both symbols appeared in the Symbols panel. The op-amp was copied
  into a fresh A4 document, saved, unlinked using the menu, and its `body` selected
  in Layers and Objects. All eight readable part names were visible. Saved artwork
  was reopened in Inkscape and retained geometry and semantic parts. Placement size
  was 18.200 × 13.533 mm including stroke. Resistor GUI placement was not repeated.
- Inkscape GUI: **Label A** was changed to **Label B**, saved, closed and reopened.
  Native editable SVG text and the separately preserved original string were checked.
- Repeated symbols retained unique IDs and valid references after serialization.
- The same TeX helpers compiled alongside native CircuitikZ content connected
  through named anchors. This is a compatibility fixture, not a complete schematic.
- Nine focused tests cover duplicate definitions/parts, unknown/missing references,
  presets, namespaces, physical settings, stroke independence and group structure.

Evidence: [measurements](measurements.json),
[palette and serialization](verification.json),
[placement, text and clearances](inkscape-checks.json),
[edited text](editable-label-reopened.svg),
[reopened symbol](symbols-reopened.svg), and
[native CircuitikZ PDF](tex/native-circuitikz.pdf).

## Measured rendering cost

The recorded 18-configuration run used **12.9544 s** for TeX compilation and
**0.5107 s** for dvisvgm conversion (13.4651 s combined, about 0.748 s/configuration).
Individual SVGs are **1,786–3,382 bytes**. The native CircuitikZ fixture compiled
in **0.8712 s**. These measurements exclude installation, initial bundle/font
downloads, PNG generation, GUI work and verification; they are not a cold-start
benchmark or a viewer performance claim.

## Review and limits

Review the actual sheet, especially Small+Thick, proportions, lead lengths, signs
and weight balance. Technical verification and appearance acceptance are separate.
No additional appearances or viewer should be built until the user approves.

Editable-text normalization is limited to one simple installed-Arial label;
arbitrary fonts and mathematical text are unproven. Placed Symbols instances must
be unlinked before part editing; Inkscape can change XML IDs but preserved
`data-part` identities and readable labels. SVG edits do not synchronize back to
TeX/YAML. README records the tested versions, commands and bounded limitations.
