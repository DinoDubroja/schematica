# Dev-library batch 02

**Review applied 14-11-2026:** 65 retained designs / 693 configurations from the
original 80-design batch. **52 Verified; 13 Unverified.** Exactly 15 designs removed.
The complete dev library has **91 designs / 1,035 configurations: 78 Verified,
13 Unverified**. The original 26 approvals and 342 SVGs are unchanged.

All 53 supplied approvals matched the reviewed revisions before editing. XOR's
approval applied to its old drawing and was superseded by the requested correction.
The N-channel bulk MOSFET was already dot-free: its unchanged revision 1 is Verified.
The P-channel bulk MOSFET is also unchanged but has no supplied approval.

## What to inspect

Open **Unverified → Variations**, then try **Small / Thick** in the main preview.
The 12 corrected designs are revision 2 and require fresh review. The remaining
Unverified design is the unchanged P-channel bulk MOSFET, revision 1.

| Review | Expected drawing |
|---|---|
| [N-JFET](https://schematica-preview.dinodubroja.workers.dev/#symbol=jfet-n), [P-JFET](https://schematica-preview.dinodubroja.workers.dev/#symbol=jfet-p) | Bent drain/source leads, gate at source-side branch; N arrow inward, P outward. P source is above drain, following CircuitikZ |
| [N enhancement](https://schematica-preview.dinodubroja.workers.dev/#symbol=mosfet-n-enhancement), [P enhancement](https://schematica-preview.dinodubroja.workers.dev/#symbol=mosfet-p-enhancement), [N depletion](https://schematica-preview.dinodubroja.workers.dev/#symbol=mosfet-n-depletion), [P depletion](https://schematica-preview.dinodubroja.workers.dev/#symbol=mosfet-p-depletion) | No filled junction dots; connecting lines and body arrows intact |
| [NPN](https://schematica-preview.dinodubroja.workers.dev/#symbol=transistor-npn), [PNP](https://schematica-preview.dinodubroja.workers.dev/#symbol=transistor-pnp), [phototransistor](https://schematica-preview.dinodubroja.workers.dev/#symbol=phototransistor-npn) | Collector/emitter junctions and pins 1 mm left; base unchanged. Arrow at outer emitter end, pointing outward for NPN and inward for PNP |
| [Chassis ground](https://schematica-preview.dinodubroja.workers.dev/#symbol=ground-chassis) | Bar stops at first/third hatch attachments, including Thick; no horizontal overhang |
| [XOR](https://schematica-preview.dinodubroja.workers.dev/#symbol=logic-xor), [XNOR](https://schematica-preview.dinodubroja.workers.dev/#symbol=logic-xnor) | Inputs end on the separate outer curve; no lead in the gap. XNOR bubble remains |
| [P-channel bulk MOSFET](https://schematica-preview.dinodubroja.workers.dev/#symbol=mosfet-p-enhancement-bulk) | Unchanged four-terminal drawing, still awaiting its first approval |

Copy the symbol reference when reporting a correction. Technical checks do not
approve designs; use the [verification handoff](VERIFICATION.md).

## Retained inventory

Existing family/batch filters remain. Each retained design keeps its
`overnight-<family>-02` batch; searching `overnight` finds all 65 retained designs.
Unidirectional TVS remains covered by the Zener drawing/aliases.

### Capacitors

5 designs / 99 configurations · 5 Verified / 0 Unverified.

`capacitor-feedthrough`, `capacitor-polarized`, `capacitor-polarized-curved`, `capacitor-trimmer`, `capacitor-variable`.

### Diodes

7 designs / 63 configurations · 7 Verified / 0 Unverified.

`diode`, `diode-led`, `diode-photo`, `diode-schottky`, `diode-tvs-bidirectional`, `diode-varactor`, `diode-zener`.

### Transistors

12 designs / 108 configurations · 2 Verified / 10 Unverified.

`igbt-n`, `jfet-n`, `jfet-p`, `mosfet-n-depletion`, `mosfet-n-enhancement`, `mosfet-n-enhancement-bulk`, `mosfet-p-depletion`, `mosfet-p-enhancement`, `mosfet-p-enhancement-bulk`, `phototransistor-npn`, `transistor-npn`, `transistor-pnp`.

### Sources and grounds

10 designs / 90 configurations · 9 Verified / 1 Unverified.

`battery`, `cell`, `ground-chassis`, `ground-earth`, `ground-signal`, `source-current`, `source-dependent-current`, `source-dependent-voltage`, `source-voltage`, `source-voltage-ac`.

### Inductors and transformers

8 designs / 126 configurations · 8 Verified / 0 Unverified.

`inductor-eu`, `inductor-ferrite`, `inductor-iron`, `inductor-variable`, `inductor-variable-iron`, `transformer-air`, `transformer-center-tap`, `transformer-core`.

### Logic

12 designs / 108 configurations · 10 Verified / 2 Unverified.

`logic-and`, `logic-buffer`, `logic-nand`, `logic-nor`, `logic-not`, `logic-or`, `logic-schmitt-buffer`, `logic-schmitt-inverter`, `logic-tristate-buffer`, `logic-tristate-inverter`, `logic-xnor`, `logic-xor`.

### Switches and relays

4 designs / 36 configurations · 4 Verified / 0 Unverified.

`switch-dpdt`, `switch-dpst`, `switch-spdt`, `switch-spst`.

### Connections and instruments

5 designs / 45 configurations · 5 Verified / 0 Unverified.

`ammeter`, `connector-coaxial`, `terminal-open`, `test-point`, `voltmeter`.

### Protection and resonators

2 designs / 18 configurations · 2 Verified / 0 Unverified.

`crystal`, `fuse`.

## Removed after review

The six new analog blocks were removed; the original op-amp designs remain.
These 15 IDs have no active definition, recipe registration, catalog entry or SVG:

`amplifier-fully-differential`, `amplifier-instrumentation`, `ceramic-resonator`, `comparator`, `comparator-supply`, `connector-2pin`, `connector-3pin`, `ota`, `pushbutton-nc`, `pushbutton-no`, `regulator`, `relay-coil`, `relay-spdt`, `supply-port`, `terminal-filled`.

Their earlier artwork remains in Git history and the verified external backup.

## Construction and checks

[Construction reference](SYMBOL_REFERENCE.md) and parameterized TeX remain the
authority. The JFET rebuild follows CircuitikZ `njfet`/`pjfet` with arrows at the
gate end, translated and sized for Schematica's 1 mm connection grid. P-JFET's
source/drain placement mirrors N-JFET. The BJT shift is a fixed 1 mm at every size;
the PNP arrow's back edge sits at the outer junction and its tip points inward.
Chassis uses a butt cap on the trimmed bar. XOR/XNOR leads use the outer curve at
each input height; no masking shapes are used.

All 108 changed configurations were rendered and visually inspected. Regression checks
cover the reported defects, 927 unchanged SVG bytes, exact supplied approvals,
stale approval rejection and the retained/removed inventory. Full SVG bounds,
editable-parts save/reopen and all 36 complete-library exports are checked separately.
See [the latest results and device checklist](../DEVELOPMENT.md#latest-changes).
