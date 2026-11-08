# Differential amplifier performance

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 2.64. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** the source screenshot was visually inspected. This record preserves its caption, equations, and observations. Editable source and repository previews are not available. Recreation is optional and has not been requested. The original image is not saved in the repository.

## Original caption

> **Figure 2.64.** Calculating differential amplifier performance.

Caption transcribed from the supplied screenshot.

## Equations shown in the figure

The following equations are transcribed from the source, retaining its symbols and signs. They are part of the reference illustration, not a new derivation or independently validated model.

$$G_{\mathrm{diff}}=\frac{v_{\mathrm{out}}}{v_1-v_2}=\frac{R_{\mathrm{C}}}{2(R_{\mathrm{E}}+r_e)}$$

$$G_{\mathrm{CM}}=-\frac{R_{\mathrm{C}}}{2R_1+R_{\mathrm{E}}+r_e}$$

$$\mathrm{CMRR}\approx\frac{R_1}{R_{\mathrm{E}}+r_e}$$

## What it demonstrates

The differential pair occupies the left side, while three equations form a separate vertical group on the right. The transistors face inward toward two horizontal emitter resistors and a central tail resistor. Input 1 (+) and input 2 (−) are labeled outside the bases, and output is labeled at the right collector branch.

The top rail is +5V; the tail resistor terminates at −5V. The two emitter resistors are each labeled $R_{\mathrm{E}}$, 1.0k. The tail resistor is $R_1$, 22k, beside a downward 200μA arrow. The right collector resistor is $R_{\mathrm{C}}$, 25k; the left collector resistor has no visible identifier or value. Filled dots mark branch connections, and component identifiers and values are stacked near their symbols.

## Inferred lessons to review

- Circuit topology and its associated equations can share one figure without placing formulas over the wiring.
- A central tail branch and inward-facing transistors make the paired arrangement visually clear.
- External input polarity labels and nearby current arrows add functional information while preserving component-label clearance.

These observations remain provisional. Preserve the source's equation notation when recording or faithfully recreating it; it is not a new general notation rule. Supply labels and plain wire endings are reference observations, not implicit exceptions to accepted general preferences. Select for circuit-and-equation composition, differential-pair layout, and current annotations. Obtain the source image before recreating geometry. Compare [Figure 2.66](../../schematics/fig-02-66-single-ended-dc-amplifier/EXAMPLE.md) for a related layout with different connections.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
