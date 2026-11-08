# Three-op-amp instrumentation amplifier

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 5.77. Printed page not supplied.
- **Received:** 08-11-2026, with an explicit request to add this and Figure 5.78 to the collection list.
- **User feedback:** no feature-specific comments on the figure; recorded as liked overall under the collection convention. The accompanying workflow questions concern image storage and preview formats.
- **Review and assets:** source screenshot visually inspected. Caption, equations, and observations are recorded; editable source and repository previews are unavailable. Recreation is optional and has not been requested. The original image is not saved in the repository. Original PNG import was authorized on 08-11-2026, but the download failed because this machine could not resolve the image host. Import and visual-page completion remain outstanding; no new style inference is authorized.

- **Import source:** user-supplied `image(20261108-150805).png` (49,916 bytes reported by the source service). This filename identifies the intended original; the file has not been downloaded or hash-verified here. Obtain it from the supplied attachment or the user's saved original, not a substitute found online.

## Original caption

> **Figure 5.77.** The classic three-op-amp instrumentation amplifier.

## Equations shown in the figure

$$G_{\mathrm{CM}}=1$$

$$G_{\mathrm{diff}}=1+\frac{2R_{\mathrm{f}}}{R_{\mathrm{g}}}$$

These source equations appear below a brace spanning the first two op-amps. They describe that input-stage grouping; do not present the unity common-mode gain as the gain of the complete three-op-amp circuit. Source symbols and scope are preserved, not independently rederived.

## What it demonstrates

U1 and U2 form a vertically paired input stage, feeding U3 at the right through equal resistors labeled R. Each input amplifier has a local feedback resistor $R_{\mathrm{f}}$; the single $R_{\mathrm{g}}$ links their inverting-input networks at the left. Filled dots mark branch connections, while hollow circles identify the input, gain-resistor, sense, output, and reference connection points.

The source labels the upper external input “−in” and the lower “+in”, even though both enter their respective input amplifiers at positive pins. Preserve these overall input labels separately from individual op-amp pin polarities. At the right, “sense” returns around the outside to the output node, and “ref” is connected to ground. The output connection is labeled “out”.

A lower brace groups the two input amplifiers and their gain equations. Clear vertical alignment and matching feedback geometry reveal the paired structure, while the right-hand stage remains visually distinct. Labels sit next to components or exposed connection points rather than inside the routing corridors.

## Inferred lessons to review

- Use aligned repeated stages and a grouping brace to connect a circuit region to its equations.
- Distinguish external signal polarity from the plus/minus pins of individual amplifiers.
- Make sense, output, reference, and gain-setting connections visible as separate labeled roles.

These observations remain provisional. Select for instrumentation-amplifier layout and equations scoped to a subcircuit; compare [Figure 5.78](../fig-05-78-signal-guarding/EXAMPLE.md) for a related circuit with guard circuitry. Obtain the original image for recreation. Source terminal and junction details do not introduce new general symbol rules.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
