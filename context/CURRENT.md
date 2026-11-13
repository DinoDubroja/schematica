# Current status

14-11-2026 · **Resistor corrections and Variations ready for human review.**

The user authorized implementation, testing, documentation, commit/push and the
existing-preview deployment. Creation skills and accounts/profiles remain outside
this run. See [decisions](DECISIONS.md) for confirmed versus deferred scope.

## Current checkpoint

- **28 designs / 360 configurations**, promoted after technical and family visual
  checks. Four variable/trimmer designs have 36 combinations; the other 24 have nine.
- Centered vertical potentiometer wipers, NTC/PTC lettering, symmetric light arrows,
  nonlinear S instead of varistors, and four adjustment orientations are implemented.
- Compact **Variations** compares Stroke, Size and applicable options at common scale.
  Exact single exports and all 36 deterministic library profiles are implemented.
- Six original designs retain approval and byte-identical SVGs. The other 22 remain
  **Unverified**. Browser test approvals were undone; the official record is unchanged.
- Build **`601a9624a06d`**: 42 Python + 8 JavaScript tests, all 360 Inkscape checks,
  36 library exports, 57 actual local downloads and native TeX checks pass.
  See [actual results and review steps](../DEVELOPMENT.md#latest-changes).
- The [reference guide](../docs/SYMBOL_REFERENCE.md) was established before redrawing.
  Detailed IEC/ISO records were inaccessible; no unreviewed compliance is claimed.

## Published preview

Cloudflare deployment **`e6505edb`** serves build **`601a9624a06d`**. The hosted
manifest and all 404 served assets match local hashes. Actual selected-orientation
single and library downloads, plus a default-orientation library download, match
byte for byte. Live search, Variations, themes and pending/reload/Undo passed.
An independent read-only session recovered the scope, boundaries and next step
from the repository alone without contradictions or edits.

A fresh Git-index checkout reproduces build `601a9624a06d`. SVG output uses
consistent line endings; the six originals retain their historical bytes.

## Next step

Human visual review on both Windows devices: follow the short checks in
[DEVELOPMENT.md](../DEVELOPMENT.md#test-and-review). Fix requests remain in chat;
design approval uses the existing [verification handoff](../docs/VERIFICATION.md).
This run's publication authorization covers the completed update only. Further
features and publishing new human approvals require their own user instruction.

[Develop and test](../DEVELOPMENT.md) · [Batch workflow](../docs/RESISTOR_BATCH.md)
· [Preview](https://schematica-preview.dinodubroja.workers.dev/)

The laptop, profile-wide Inkscape installation, fresh GUI grid snapping and
clean-machine/offline TeX setup remain unverified. Inkscape roundtrip results in
this run are command-line checks. The broader milestone interview is unfinished;
see [roadmap](../docs/ROADMAP.md). Future wishes do not authorize new implementation.
