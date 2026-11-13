# Resistor batch 01

Preparation was fixed before production: **24 resistor designs**, including two
existing fixed resistors and **22 new designs**. Each design has nine size/stroke
configurations. With the four other existing symbols, the library has 28 designs
and 252 configurations. Arrays and networks are excluded.

## Inventory and references

The first reference is [CircuitikZ, resistive bipoles](https://rmano.github.io/circuitikz/node-The-components-list.html).
The component list and visual examples were checked on 13-11-2026 against version
1.8.7 and the project's installed renderer. These are reference-informed drawings,
not a claim of certification to an electrical drawing standard.

| Designs (stable identifiers) | Reference and selected approach |
|---|---|
| `resistor-eu`, `resistor-us` | Reuse the accepted fixed bodies and exports unchanged; CircuitikZ `R` forms |
| `resistor-variable-eu`, `resistor-variable-us` | Adapt `vR`: two electrical terminals and a diagonal adjustment arrow |
| `potentiometer-eu`, `potentiometer-us` | Adapt `pR`: two ends and a separately connectable central wiper |
| `resistor-trimmer-eu`, `resistor-trimmer-us` | Custom preset-resistor marking on the accepted body: diagonal bar with perpendicular end; two terminals |
| `potentiometer-trimmer-eu`, `potentiometer-trimmer-us` | Adapt `pR` with a preset adjustment bar; retain the third wiper terminal |
| `thermistor-eu`, `thermistor-us` | Adapt `thR`: bent dependency stroke; temperature coefficient deliberately unspecified |
| `thermistor-ntc-eu`, `thermistor-ntc-us` | Adapt `thRn`: dependency stroke with negative temperature indication |
| `thermistor-ptc-eu`, `thermistor-ptc-us` | Adapt `thRp`: dependency stroke with positive temperature indication |
| `varistor-eu`, `varistor-us` | Adapt `varistor`: dependency stroke with voltage indication; two non-polarized terminals |
| `photoresistor-eu`, `photoresistor-us` | Adapt `phR`: two incoming light arrows; no extra electrical pins |
| `photoresistor-enclosed-eu`, `photoresistor-enclosed-us` | Adapt `ldR`: circular enclosure and incoming light arrows |
| `resistor-tapped-eu`, `resistor-tapped-us` | Custom fixed central tap derived from the `pR` connection arrangement, with no movable-wiper arrow |

EU and US indicate rectangular and zigzag body appearances. For miscellaneous
components where CircuitikZ offers a rectangular form, the zigzag companion is an
explicit Schematica adaptation. Preset/trimmer and tapped forms are custom TeX
designs, not invented names for built-in CircuitikZ symbols.

### Deliberate adaptations

- Reuse Schematica's accepted body proportions, independent strokes and 1 mm pins.
- Express the reference forms through the existing TeX helpers so bodies, leads,
  indicators and wipers remain named editable parts. A monolithic stock glyph
  would lose that structure; it is a starting reference, not the final SVG asset.
- Keep diagonal adjustment/dependency marks distinct from electrical connections.
  Only three-terminal potentiometers and tapped resistors receive a third pin.
- A zigzag wiper or tap meets a clear upper peak. Its external third terminal
  remains centered on the connection grid; the short angled lead keeps the contact legible.
- Use explicit `−t°`, `+t°` and `U` indications for NTC, PTC and voltage dependence.
  Their geometry scales with size, independently of stroke.
- Use the same physical scale in the nine-configuration viewer. Do not enlarge
  small symbols to fill their cells.

## Repeatable creation workflow

Preparation establishes the finite inventory, meaning, pins, reference and approach
above. Creation then uses that specification:

1. Create the definition and TeX recipe with stable pins and named parts.
2. Render all nine configurations into temporary build output.
3. Check semantics/pin mapping, geometry, grid, clearances, clipping, editable
   parts, repeated instances and exports; visually inspect the actual results.
4. Correct failures and repeat the affected checks.
5. Add passing designs to the catalog as **Unverified**. Technical success never
   grants human verification. Keep unresolved failures out of the released catalog.

The batch and a future interactive creation skill share the same renderer and
checks, but remain separate workflows. Review changes stay in chat; no review
sheets or comment fields are maintained.

## Results — 13-11-2026

**Completed: all 22 new designs. Excluded: none.** The catalog contains 28 designs
and 252 configurations. Six earlier designs retain official acceptance; all new
designs remain Unverified. No test approvals were applied to the real record.

| Check | Result |
|---|---|
| Complete batch rendering | 252 configurations compiled; no unresolved failures |
| Automated checks | 34 Python tests and 4 JavaScript state tests pass |
| Accepted originals | All 54 original SVG files are byte-identical; 42 independent palette comparisons pass |
| Electrical structure | Two terminals except potentiometers/preset potentiometers and tapped resistors; all external pins on the 1 mm grid |
| Independent size/stroke | All designs preserve geometry and pins across stroke changes; bodies reuse the accepted rectangle/zigzag |
| Visual inspection | All 28 designs inspected in the labelled 3 × 3 viewer; US wiper/tap contacts corrected to a clear zigzag peak |
| Inkscape rendering | All 252 checked; minimum margin 0.999986 mm; original-palette maximum deviation 0.001234 mm (limit 0.005 mm) |
| Exports | Nine downloaded libraries contain all 28 designs and match the build byte for byte; original and new individual downloads also match |
| Editing/reuse | Composite save/reopen preserves named parts; GUI Symbols shows 28 thumbnails; a US potentiometer was pasted, unlinked, saved and reopened with all five editable parts |
| Native TeX | Existing CircuitikZ fixture and a new US trimmer potentiometer compile to PDF |
| Approval handoff | Separate temporary browser → clipboard/fallback → apply → rebuild → official status loop passed; repeated apply is harmless; unknown/stale entries rejected |
| Browser | Search, family/batch filters, review navigation, reload, reference links, themes, keyboard and 360 px layout pass; no console warnings/errors observed |

The initial source references were reviewed before creation. The visual correction
above changed only new designs. Technical validation is not electrical simulation
or standards certification, and does not substitute for the user's visual review.

Build **c7b750381988**. Publication status is recorded in
[current status](../context/CURRENT.md). Repeat the [developer checklist](../DEVELOPMENT.md#test-and-review)
on the second Windows device. Profile-wide Inkscape installation, fresh GUI grid
snapping and clean-machine/offline rendering remain unverified.

Published: [shared preview](https://schematica-preview.dinodubroja.workers.dev/) ·
[fixed version](https://6b23fd83-schematica-preview.dinodubroja.workers.dev/).
Hosted manifest and all 268 served assets match build **c7b750381988**. Actual hosted
single/library downloads match; live search, comparison, theme persistence, pending
reload/Undo and symbol references pass. Browser warnings/errors: none.
