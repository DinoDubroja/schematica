# Sziklai-pair power stage

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 2.78. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** the source screenshot was visually inspected. This record preserves its caption and observations. Editable source and repository previews are not available; recreation remains pending. The screenshot is a working input outside the repository.

## Original caption

> **Figure 2.78.** Push–pull power stage with Sziklai-pair output transistors, capable of output swings to ±70 V and output currents of ±2 A peak.

Caption transcribed from the supplied screenshot; line-break hyphenation is removed and spacing around units is normalized.

## What it demonstrates

A tall six-transistor circuit is organized between horizontal +75V and −75V rails. Bias and adjustment components occupy the left; driver/output transistor pairs occupy the upper and lower right. Two vertically aligned 0.5Ω resistors meet in the output region, which connects to a rectangular load with a vertically rotated label and local ground.

Identifiers and transistor part numbers are stacked beside the symbols: $Q_1$ and $Q_3$, 2SC4793; $Q_2$, 2N3904; $Q_4$, 2SA1943; $Q_5$, 2SA1837; and $Q_6$, 2SC5200. Heat-sink graphics sit beside the two outer output transistors. Other labels include $R_1$ and $R_2$ at 3.6k, two 100 resistors, a 1.0k resistor, and a 2.5k adjustment marked set bias with a small diagonally marked circle nearby.

Polarized $C_1$ is horizontal and labeled 47μF, 50V, with its positive side on the left. Polarized $C_2$ is vertical and labeled 10μF, with its positive side above. A downward 10mA annotation sits beside the bias branch; another downward arrow at the output stage is labeled $I_{\mathrm{Q}}=100\,\mathrm{mA}$. Solid junction dots identify connected branches, while unmarked crossings stay visually distinct. Dashed leads at the lower-left transistor show circuit continuation beyond the drawn region; they are not the dashed external load convention seen in Figure 1.67.

## Inferred lessons to review

- Functional grouping and a tall layout can keep a dense practical circuit legible.
- Stacked identifiers, part numbers, values, and voltage ratings can provide detail while staying close to the relevant symbol.
- Heat-sink, bias-adjustment, current, and continuation annotations have different roles despite sharing the monochrome drawing style.
- Filled dots and deliberate label placement are particularly important where long wires cross or pass close to other branches.

These observations are provisional; they do not impose new typography, routing, ground, or supply-symbol defaults. Preserve transistor types, capacitor polarities, marked junctions, unconnected crossings, and partial-circuit boundaries in a future recreation. The caption's operating limits remain attributed to the source and have not been independently validated. Select for dense power-stage layout, practical part labels, adjustment controls, and heat-sink symbols. Obtain the source image before recreating geometry; no repository preview exists.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
