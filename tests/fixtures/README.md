# Regression fixtures

These inputs belong to the accepted new symbol batch. They are test evidence,
not legacy drawing instructions. Do not regenerate the accepted baseline merely
to make a failing test pass.

| Fixture | Purpose |
|---|---|
| [accepted-geometry.json](accepted-geometry.json) | Frozen paths and SVG byte hashes for all 54 configurations at published baseline e97aa17 |
| [Accepted palette PDF](accepted-palette/preset-comparison-10mm-shorter-opamp.pdf) and [TeX](accepted-palette/preset-comparison-10mm-shorter-opamp.tex) | User-accepted geometry reference; historical “draft” captions predate acceptance |
| [opamp-supply.scmeta](opamp-supply.scmeta) | Missing/duplicate/unknown semantic-part validation |
| [repeated.svg](repeated.svg), [symbols.svg](symbols.svg) | Namespaced repeated symbols and Symbols references from the accepted rendering proof |
| [editable-label.svg](editable-label.svg), [source](editable-label.tex), [literal text](editable-label.strings.json) | Bounded editable-text conversion fixture; no general text guarantee |
| [native-circuitikz.tex](native-circuitikz.tex) | Schematica helpers beside native CircuitikZ, with named coordinates |

Palette files were preserved from the accepted 12-11-2026 comparison. The remaining
inputs came from the accepted first-batch rendering proof. Old screenshots,
historical reports, save/reopen copies and full duplicated bundles are archived
outside this checkout. Fresh verification output goes to ignored `app/build/`.
