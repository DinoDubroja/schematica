# Clamp output glitches

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.62. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session, together with Figure 4.61.
- **User feedback:** no comment specifically addressed this figure; recorded as liked overall under the collection convention. The accompanying praise of complexity explicitly concerned Figure 4.87.
- **Review and assets:** source waveform screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.62.** Finite slew-rate causes clamp output “glitches”.

## What it demonstrates

The waveform accompanies the [active-clamp circuit](../../schematics/fig-04-61-active-clamp/EXAMPLE.md). Three behaviors share one set of axes: the smooth input, clamped output, and op-amp output. Direct labels identify $V_{\mathrm{in}}$, $V_{\mathrm{out}}$, and “op-amp output”; “$V_{\mathrm{in}}$ & $V_{\mathrm{out}}$” marks a coincident portion. The horizontal axis ends in an arrow labeled t. The vertical reference labels include +15 and +10, with $V_{\mathrm{clamp}}$ beside +10.

Different line weights separate portions of overlapping curves. Short dashed vertical lines mark transition times; sloping op-amp-output transitions make the finite response visible. Two curved leaders connect the word “glitches” to small deviations near the transitions. Labels occupy whitespace, with a short leader where needed. There is no grid or separate legend.

## Inferred lessons to review

- Use direct labels and differentiated strokes to explain overlapping signals without requiring color.
- Identify a small timing defect with local leaders and transition markers rather than a long paragraph on the plot.
- Keep the schematic and behavior diagram as separate, linked figures when each needs a different composition.

These observations remain provisional. The supplied plot is explanatory; no time scale, frequency, sampled data, or numerical slew rate is supplied. Do not infer those from image geometry or present a recreation as a measured or simulated trace. Preserve the source labels when transcribing it. Select for qualitative nonideal behavior and annotated overlapping waveforms; obtain the image for recreation.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
