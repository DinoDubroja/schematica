# Resistor batch 01

Preparation was fixed before production: **24 resistor designs**, including two
existing fixed resistors and **22 additional designs**. Four adjustable designs
have 36 configurations each; the other 24 designs have nine. Including the four
non-resistor originals, the library has **28 designs / 360 configurations**.
Arrays and networks are excluded. Varistors were replaced by nonlinear resistors
in the user-authorized correction run.

## Inventory and references

Use the established [symbol construction reference](SYMBOL_REFERENCE.md):
CircuitikZ geometry, IEC meanings, ISO construction and accepted Schematica appearance.
The guide separates accessible sources, unavailable standard records and our styling.

| Designs (stable identifiers) | Reference and selected approach |
|---|---|
| `resistor-eu`, `resistor-us` | Reuse the accepted fixed bodies and exports unchanged; CircuitikZ `R` forms |
| `resistor-variable-eu`, `resistor-variable-us` | Adapt `vR`: two electrical terminals and a diagonal adjustment arrow |
| `potentiometer-eu`, `potentiometer-us` | Adapt `pR`: two ends and a separately connectable central wiper |
| `resistor-trimmer-eu`, `resistor-trimmer-us` | Custom preset-resistor marking on the accepted body: diagonal bar with perpendicular end; two terminals |
| `potentiometer-trimmer-eu`, `potentiometer-trimmer-us` | Adapt `pR` with a preset adjustment bar; retain the third wiper terminal |
| `thermistor-eu`, `thermistor-us` | Adapt `thR`: bent dependency stroke; temperature coefficient deliberately unspecified |
| `thermistor-ntc-eu`, `thermistor-ntc-us` | Adapt `thRn`: dependency stroke with uppercase NTC label |
| `thermistor-ptc-eu`, `thermistor-ptc-us` | Adapt `thRp`: dependency stroke with uppercase PTC label |
| `resistor-nonlinear-eu`, `resistor-nonlinear-us` | User-confirmed diagonal S-shaped marking; custom curve, no arrowhead; two terminals |
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
- Center the potentiometer wiper vertically; its tip is 1 mm above the upper body
  edge. This applies to both body forms and trimmers. Fixed taps remain unchanged.
- Share symmetric arrowhead construction across variable resistors, potentiometers
  and photoresistors. Photo shafts also share angle, length and perpendicular spacing.
- NTC/PTC use the same font, cap height and placement; outlines are kept in one named part.
- Four orientations reflect only the variable/trimmer marking. Body, A/B leads,
  grid coordinates and pin identities remain unchanged.
- Variations uses a common scale and changes one setting per row; combinations are
  checked separately by the renderer and tests.

## Repeatable creation workflow

1. **Prepare:** fix a finite inventory, meanings, pins and reference mapping.
   Reuse [the reference guide](SYMBOL_REFERENCE.md); document deliberate adaptations.
2. **Refine representatives first:** render both body forms and the most crowded
   Small/Thick cases. Compare shared arrows, wipers, labels and nonlinear marks
   before spreading them across a family.
3. **Produce every combination:** render candidates separately. Derive combinations
   from each definition's sizes, strokes and declared options/defaults: 36 for
   four-orientation designs, nine for the rest. A failed configuration excludes its design.
4. **Technical checks:** test semantic pins, body/stroke independence, orientation
   reflections, clearances, clipping, editable parts, references, exports and Inkscape
   save/reopen. Preserve all accepted-original SVG bytes.
5. **Mandatory visual review:** compare related designs together at a common scale
   and normal schematic size. Inspect symmetry, proportions, label readability,
   intended crossings and visible gaps. Open each design's Variations and inspect
   Small/Thick with every applicable orientation. Both themes must remain usable.
6. **Correct and repeat:** rerun affected checks after fixes. Never promote an
   incomplete design, silently substitute a missing configuration or manually edit generated paths.
7. **Promote:** only passing candidates enter the browsable catalog as **Unverified**.
   Remove obsolete catalog assets/exports and retain unaffected official approvals.
   Update the developer guide with action → expected-result checks and actual limits.

Option names/defaults belong in YAML; drawing behavior belongs in parameterized TeX.
The viewer, configuration IDs, standalone TeX bundles and exports use those declarations.
Complete libraries apply a selected orientation to compatible designs; when the
selected design has no such option, they use Up-right. All 36 library profiles
(three sizes × three strokes × four orientations) are generated deterministically.

The batch and a future interactive creation skill share the same renderer and
checks, but remain separate workflows. Review changes stay in chat; no review
sheets or comment fields are maintained.

## Results — 14-11-2026

The representative review passed before full production: centered US/EU wipers,
trimmer wiper, NTC/PTC, enclosed/unenclosed photoresistors, nonlinear US/EU and
variable/trimmer marks. Medium/Medium and Small/Thick were compared together.
The font-conversion issue found in this step was corrected before production.
The full-family Small/Thick review also exposed arrowhead/body contact on variable
resistors; extending the tip to 2.4s restored at least 0.38 mm visible clearance.
The final candidates were regenerated and checked after that correction.

All 360 configurations passed Inkscape bounds/parts/save-reopen checks; all 36
complete-library profiles passed, including actual browser download comparison.
Detailed validation and publication results are recorded in
[the developer review](../DEVELOPMENT.md#latest-changes) and
[current status](../context/CURRENT.md). Technical validation does not substitute
for the user's visual approval or establish standards compliance.
