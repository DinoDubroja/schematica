# Inherently differential signals

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 5.64. Printed page not supplied.
- **Received:** 08-11-2026, following the earlier collection wrap-up; the user explicitly requested adding these two examples.
- **User feedback:** supplied without feature-specific comments; recorded as liked overall under the collection convention. No individual drawing convention is inferred to be approved.
- **Review and assets:** both source panels visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 5.64.** Inherently differential signals, for which good common-mode rejection is required. (a) Strain gauge. (b) Audio balanced line pair.

Caption transcribed with line wrapping normalized. The drawing uses uppercase A/B panel labels while the caption uses lowercase (a)/(b).

## What it demonstrates

Two side-by-side panels explain the same signal property using different visual representations. Panel A shows a diamond resistor bridge supplied from +5V, grounded at the bottom, with its two midpoint signals entering a differential amplifier. All four resistors are labeled R; a shared note reads R = 350Ω, typ. A leader and narrow elliptical annotation identify the small differential signal, ΔV = ±10 mV, between the input leads. The lower signal wire crosses the bridge's ground lead without a junction dot.

Panel B combines circuit symbols and physical illustrations. Three source alternatives, labeled “xfmr”, “mic”, and “diff drvr”, are grouped by a brace beside a shielded twisted-pair cable drawing. They represent alternatives, not three simultaneously wired sources. A cutaway cable and 3-pin XLR connector show the conductors and shield, with leaders for “shield”, “twisted pair”, and “3-pin XLR connector”. No numbered pin assignment is supplied.

At the right, the differential receiver has labeled negative and positive inputs, with “difference amp, instrumentation amp” above and “high CMRR”, “high $Z_{\mathrm{in}}$ (CM)” below. A separate ground connection is drawn at the connector/shield region. Both panels use a triangle with a rectangular input section to depict the receiving amplifier. Dashed enclosure/shield details, hollow contacts, and leaders have different roles from electrical wires and junction dots.

## Inferred lessons to review

- Use different levels of abstraction within a figure when they explain one shared concept: a bridge schematic beside a physical cable/connector illustration.
- Group alternative source types with a brace instead of implying simultaneous electrical connections.
- Label cable construction, signal polarity, and receiver requirements close to the relevant features.
- Distinguish wire crossings, junctions, connector contacts, shield outlines, and explanatory leaders.

These observations remain provisional. Select for differential signals, balanced-line connections, and combined physical/circuit illustrations; compare [Figure 1.139](../fig-01-139-oscilloscope-probe/EXAMPLE.md). Preserve the source's common-mode qualification on input impedance; do not invent XLR pin numbers or wiring rules from the unnumbered drawing. Obtain the original image for recreation. No ground, terminal, supply, or amplifier-symbol preference is adopted by this record.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
