# Active clamp

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.61. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session, together with Figure 4.62.
- **User feedback:** no comment specifically addressed this figure; recorded as liked overall under the collection convention. The accompanying praise of complexity explicitly concerned Figure 4.87.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.61.** Active clamp.

## What it demonstrates

A straight upper signal path runs from $V_{\mathrm{in}}$ through a 2k resistor to $V_{\mathrm{out}}$. The output node branches down to the op-amp's negative input and to a vertical diode connected to its output. A +15 reference branch contains a 10k/20k divider whose midpoint feeds the positive input. The divider and op-amp occupy the space below the main path, with ground at the bottom.

The triangle points right, with the negative input above the positive input. Filled dots identify the reference and output branches. Component values and port labels are sparse; there are no device part numbers. The nearby [Figure 4.62](../../plots/fig-04-62-clamp-output-glitches/EXAMPLE.md) explains a nonideal timing effect using a separate waveform illustration.

## Inferred lessons to review

- Keep the principal signal path visually direct and place a supporting control circuit beneath it.
- Link a compact circuit and a separate explanatory waveform through their shared signal names.

These observations remain provisional. Select for a simple circuit paired with a behavior diagram. Obtain the source image for recreation; source plain lead endings do not override accepted terminal or supply rules.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
