# Laboratory dc amplifier

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.87. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** “Figure 4.87 nice example of more complex project schematic”. This explicitly endorses its usefulness as a reference for a more complex project schematic; it does not approve every individual convention as a general rule.
- **Review and assets:** source screenshot visually inspected. Caption, feedback, and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.87.** Laboratory dc amplifier with output offset. Op-amp power supply connections and bypass capacitors are not shown explicitly, a common practice in circuit schematics.

Caption transcribed with line wrapping normalized. Omission of these connections is stated by the source, not inferred from the illustration.

## What it demonstrates

A broad project schematic places the input, amplifier stages, unity-gain buffer, and output across the upper region. A separate lower reference/offset circuit connects upward through an offset-polarity selector. Functional arrangement and short control labels organize the drawing without enclosing every subsystem in a box.

The left input has a “floating BNC” connector drawing, an “input common” triangle, ground bars, and specifications $Z_{\mathrm{in}}=10\mathrm{M}\Omega$ and $|V_{\mathrm{in}}|<150\mathrm{V}$. These reference/common symbols have distinct roles and must not be merged merely for visual consistency. Protection diodes and precision resistor labels sit close to the first OPA627 stage.

Boxed control names identify “var. gain”, “gain”, “rolloff”, “offset polarity”, and “output offset”. S3 offers five gain positions labeled 0dB, 10, 20, 30, and 40dB; S1 shows 1kHz, 10kHz, and 100kHz settings. S2 has minus, zero, and plus selections. Hollow switch contacts are part of their switch symbols, not exposed signal-terminal defaults.

IC identifiers are paired with part numbers: OPA627 stages, OP-177 offset amplifiers, an LT1010CT buffer marked +1, and an LT1027D reference block. The lower controls include a 5.00V reference and a ten-turn adjustment. At the right are an output connector with $Z_{\mathrm{out}}=50\Omega$ and a zero-center meter labeled ±15V and (500-0-500µA). Component values, tolerances, and occasional power ratings use compact stacked labels.

## Inferred lessons to review

- Use this explicitly liked example when composing a complete project schematic with several interacting subsystems.
- Keep the main signal chain readable and position auxiliary circuits nearby according to their connections.
- Make user controls easy to locate with concise boxed names and adjacent setting labels.
- Distinguish connector/common roles, switch contacts, IC blocks, instrument readouts, and ordinary component labels.

The selection preference for complex project schematics is explicit; these individual layout lessons remain provisional. The caption does not authorize omitting supply connections or bypass components from a new design or netlist. No general supply, terminal, ground, or annotation rule changes are adopted. Obtain the original image before recreating this dense circuit; the record is not a complete connectivity specification.

[Collection guide](../STYLE.md) · [Available visual examples](../README.md)
