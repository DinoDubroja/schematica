# Voltage regulator

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.29. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.29.** Voltage regulator.

Caption transcribed from the supplied screenshot.

## What it demonstrates

The principal power path runs across the top. The input annotation stacks “input”, “+12V to +30V”, and “(unregulated)”; the output stacks “output”, “+10V”, “0 to 1A”, and “(regulated)”. These describe ports rather than individual components.

A large dashed circle groups two transistor symbols and a 120 resistor beneath the annotation “2N6044 (Darlington) + heat sink”. The upper transistor is oriented along the horizontal power path. A heat-sink graphic sits beside the group. The LT1637 op-amp and its reference branch are below-left, with a 10k resistor, 5.6V 1N752B zener, and explicit supply/ground connections.

The right-side divider is labeled 4.42k and 5.62k. The lower feedback route returns around the op-amp. Capacitor $C_{\mathrm{C}}$ is accompanied by the parenthetical text `("compensation")`, identifying its role in addition to its symbol.

## Inferred lessons to review

- Use a local boundary and shared part label to explain the internal elements of a composite device.
- Orient symbols to follow the dominant circuit path when doing so preserves recognizable pin roles.
- Separate port specifications, device identification, and explanatory notes through placement and short text groups.

These observations remain provisional. The source's port ranges are recorded specifications, not independently verified performance. Select for composite-device grouping, horizontal power paths, and feedback composition; compare [Figure 4.13](../fig-04-13-fet-bipolar-current-source/EXAMPLE.md). Original imagery is needed for recreation. Plain port endings do not override general terminal or supply rules.

[Collection guide](../STYLE.md) · [Available visual examples](../README.md)
