# Output amplifier for a 60 Hz power source

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.105. Printed page not supplied.
- **Received:** 08-11-2026, following the earlier collection wrap-up; the user explicitly requested adding these two examples.
- **User feedback:** supplied without feature-specific comments; recorded as liked overall under the collection convention. No individual drawing convention is inferred to be approved.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.105.** Output amplifier for 60 Hz power source. The push–pull output transistors Q₁ and Q₂ are power Darlingtons in a plastic power package.

Caption transcribed with line wrapping normalized; subscripted transistor identifiers are retained.

## What it demonstrates

The signal path proceeds from a 60Hz, 1Vrms input through a coupling capacitor and LT1097 op-amp to a complementary power stage, transformer, and output receptacle drawing. The caption identifies Q1, 2N6044, and Q2, 2N6041, as power Darlingtons even though each uses a compact transistor symbol. Each has a fin-like heat-sink graphic and “+ heatsink” annotation. Upper and lower supply branches are arranged around the pair, labeled +16V and −16V, with 10,000µF, 20V capacitors and 0.5Ω, 5W resistors.

T1 is labeled 6.3Vrms, 3A xfmr; T2 below it is labeled 6.3Vrms, 0.1A xfmr. Dots beside the windings indicate winding polarity and must be distinguished from junction dots on wires. The output receptacle is labeled 115vac, 0–15W, with a separate chassis-style ground connection. The two transformer symbols, long lower feedback route, and clear branch connections expose the larger circuit structure.

C1, 1000pF, occupies a diagonal branch between the central output and lower feedback wiring. A separate capacitor/connection annotation below the op-amp uses dashed strokes and reads $C_{\mathrm{C}}$, “overcomp”. The source does not explain those dashes further in this crop. C2, 10µF, and its polarity mark sit beneath T2. Component identifiers, values, power ratings, and transformer ratings are placed in compact local groups.

## Inferred lessons to review

- Combine standard circuit symbols and a recognizable output receptacle to show how a complete power-source circuit connects to its load.
- Position power and feedback transformers so both signal flow and the long feedback path remain traceable.
- Preserve winding polarity, capacitor polarity, heat-sink annotations, and ratings as distinct information rather than decorative details.
- Use an occasional diagonal branch when it reveals a connection more clearly than additional orthogonal bends.

These observations remain provisional. Select for transformer-coupled power circuitry and mixed circuit/physical illustrations; compare [Figure 4.87](../fig-04-87-laboratory-dc-amplifier/EXAMPLE.md) for another complex project schematic. The record is not a complete netlist or independently validated design. Do not infer omitted component values, a transformer turns ratio, or optional status from the dashed annotation. Obtain the source image for recreation; general supply and ground preferences are unchanged.

[Collection guide](../STYLE.md) · [Available visual examples](../README.md)
