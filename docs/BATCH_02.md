# Dev-library batch 02

**Authorized 14-11-2026:** 80 new designs, expected 828 configurations. Family
checkpoints, branch push and publication are authorized; all new designs remain
Unverified for human review. Existing 26 approvals and 342 SVGs stay unchanged.

Use the existing family/batch filters, Unverified and Variations. Every new
family uses `overnight-<family>-02`; searching `overnight` finds this whole run.
No additional review UI is introduced.

## What to inspect

Open **Unverified**, choose a family and its overnight batch, then use **Variations**
and **Small / Thick**. Copy the symbol reference when reporting a correction.

| Family | Look for |
|---|---|
| Capacitors | Positive terminal, curved negative plate, feedthrough case pin; adjustment marks clear of the plates |
| Diodes | Cathode marking, outward LED versus inward photo arrows, separate varactor plates and opposed TVS junctions |
| Transistors | Base/gate and collector/drain/source identities; N/P arrows, broken/continuous channels and independent bulk terminals |
| Sources / grounds | Voltage polarity, current direction, long positive battery plates; earth, signal and chassis meanings |
| Magnetics | Core marks, winding isolation, corresponding polarity dots and secondary center tap; all adjustment directions |
| Analog | Input/output polarity, gain/reference/bias terminals and readable labels; generic blocks are not specific IC pinouts |
| Logic | Inversion bubbles, separate XOR curve, Schmitt mark and lower active-high tri-state enable |
| Switches / relays | Open/closed resting state, selected throw, mechanically linked poles and isolated relay coil |
| Connections / instruments | Contact numbers, separate coax center/shield, TP marking and A/V meter labels |
| Protection / resonators | Fusible link, crystal plates and the ceramic resonator's two load capacitors/common terminal |

Verify acceptable designs and copy approvals into chat. Technical completion below
does not mark a design Verified; see the [approval handoff](VERIFICATION.md).

## Finite inventory

Status below describes production, never human acceptance. Unidirectional TVS
is intentionally covered by the Zener drawing and aliases; adding identical
artwork under a second name would inflate the inventory. Sources/grounds has
11 designs so all requested electrical forms are represented.

### Capacitors

Status: complete — 5 designs / 99 configurations; Unverified.

`capacitor-polarized`, `capacitor-polarized-curved`, `capacitor-variable`, `capacitor-trimmer`, `capacitor-feedthrough`.

### Diodes

Status: complete — 7 designs / 63 configurations; Unverified.

`diode`, `diode-zener`, `diode-schottky`, `diode-led`, `diode-photo`, `diode-varactor`, `diode-tvs-bidirectional`.

### Transistors

Status: complete — 12 designs / 108 configurations; Unverified.

`transistor-npn`, `transistor-pnp`, `jfet-n`, `jfet-p`, `mosfet-n-enhancement`, `mosfet-p-enhancement`, `mosfet-n-depletion`, `mosfet-p-depletion`, `mosfet-n-enhancement-bulk`, `mosfet-p-enhancement-bulk`, `phototransistor-npn`, `igbt-n`.

### Sources And Grounds

Status: complete — 11 designs / 99 configurations; Unverified.

`source-voltage`, `source-current`, `source-voltage-ac`, `source-dependent-voltage`, `source-dependent-current`, `cell`, `battery`, `supply-port`, `ground-earth`, `ground-signal`, `ground-chassis`.

### Inductors And Transformers

Status: complete — 8 designs / 126 configurations; Unverified.

`inductor-eu`, `inductor-iron`, `inductor-ferrite`, `inductor-variable`, `inductor-variable-iron`, `transformer-air`, `transformer-core`, `transformer-center-tap`.

### Analog

Status: complete — 6 designs / 54 configurations; Unverified.

`comparator`, `comparator-supply`, `amplifier-fully-differential`, `amplifier-instrumentation`, `ota`, `regulator`.

### Logic

Status: complete — 12 designs / 108 configurations; Unverified.

`logic-and`, `logic-nand`, `logic-or`, `logic-nor`, `logic-xor`, `logic-xnor`, `logic-not`, `logic-buffer`, `logic-schmitt-buffer`, `logic-schmitt-inverter`, `logic-tristate-buffer`, `logic-tristate-inverter`.

### Switches And Relays

Status: complete — 8 designs / 72 configurations; Unverified.

`switch-spst`, `switch-spdt`, `switch-dpst`, `switch-dpdt`, `pushbutton-no`, `pushbutton-nc`, `relay-coil`, `relay-spdt`.

### Connections And Instruments

Status: planned.

`terminal-open`, `terminal-filled`, `test-point`, `connector-2pin`, `connector-3pin`, `connector-coaxial`, `ammeter`, `voltmeter`.

### Protection And Resonators

Status: planned.

`fuse`, `crystal`, `ceramic-resonator`.

## Construction and verification

[Construction reference](SYMBOL_REFERENCE.md) remains authoritative for styling
and source-access limits. Each YAML definition names its CircuitikZ reference
or explains its custom construction. Detailed IEC/ISO records remain inaccessible;
no standards compliance is claimed. Native TeX remains drawing authority.

Prioritize capacitors, diodes, transistors, sources/grounds and magnetics, then
analog, logic, switches/relays, connections/instruments and protection/resonators.
Render and visually refine representatives before all configurations of each
family. Inspect actual Medium/Medium, Small/Thick and adjustment orientations at
common scale and normal size. Check electrical meaning, named parts, grid,
clearances, Inkscape bounds/save/reopen and export references. Promote only passing
complete designs. Candidate failures remain outside the active catalog.

[Developer checks](../DEVELOPMENT.md#test-and-review) ·
[Human verification](VERIFICATION.md)
