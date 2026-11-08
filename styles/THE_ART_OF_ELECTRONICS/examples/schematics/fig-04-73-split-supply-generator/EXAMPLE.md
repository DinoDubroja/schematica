# Op-amp split-supply generator

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.73. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is optional and has not been requested. The original image is not saved in the repository.

## Original caption

> **Figure 4.73.** Op-amp split-supply generator. A follower generates a low-impedance mid-battery output voltage, which becomes circuit ground.

Caption transcribed with line wrapping and print line-break hyphenation normalized.

## What it demonstrates

A 9V battery forms the left boundary of a compact circuit between horizontal upper and lower rails, labeled $V_+$ and $V_-$. Two 100k resistors create a midpoint at the op-amp's positive input. A 0.1µF capacitor connects this midpoint to the lower rail.

The follower is labeled LT 1097 across two lines. Its explicit supply leads reach both rails; the feedback wire loops above the triangle to the negative input. Junction dots distinguish connected branches from a crossing between the upper supply lead and feedback wire.

The op-amp output is marked with a ground symbol on the right. Two 1µF capacitors connect this output to the upper and lower rails, with separate polarity plus signs. The lower capacitor's positive side is at the output/ground node; the upper capacitor's positive side is at the upper rail. These capacitor symbols use straight parallel plates with polarity annotations in this source.

## Inferred lessons to review

- Make the chosen reference node explicit: here the op-amp output is circuit ground, while the battery's negative terminal belongs to the lower rail.
- Preserve polarity annotations relative to actual nodes, even when the grounded node lies between supply rails.
- Use clear junctions and crossings when feedback and supply wires share limited space.

These observations remain provisional. The ground placement is part of this circuit's meaning, not a newly adopted ground-symbol preference. Straight capacitor plates and labeled rail endings are source observations, not global style requirements. Select for split-supply composition and explicit op-amp supplies. The caption's performance description remains a source claim; obtain the image for recreation.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
