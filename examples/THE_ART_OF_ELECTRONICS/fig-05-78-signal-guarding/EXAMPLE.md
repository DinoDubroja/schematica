# Signal guarding

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 5.78. Printed page not supplied.
- **Received:** 08-11-2026, with an explicit request to add this and Figure 5.77 to the collection list.
- **User feedback:** no feature-specific comments on the figure; recorded as liked overall under the collection convention. The accompanying workflow questions concern image storage and preview formats.
- **Review and assets:** all five source panels visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending under the current workflow; the proposed image-only alternative is not yet implemented. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 5.78.** Signal guarding for greatly reduced cable capacitance. (A)–(C) are common-mode guards; (D) and (E) are individual signal guards.

Caption transcribed with line wrapping normalized. The functional classification is supplied by the source.

## What it demonstrates

Five panels share a wide composition: a large detailed circuit A at the left, compact B/C panels across the upper right, and D/E below them. Panel size follows the detail required rather than forcing identical frames. Cable/shield outlines are combined with ordinary circuit symbols and functional amplifier blocks.

Panel A extends the three-op-amp instrumentation layout with U4, a left-facing follower. Two 10k resistors form a midpoint between the input-stage outputs; that midpoint drives the guard buffer, whose output reaches the guard through 100Ω. A separate outer shield connection is grounded. The sense, out, and ref connections are labeled at the right, with a load between out and ref. Hollow contacts, solid junctions, shield connections, and ground remain distinguishable.

Panel B uses an AD522 triangle with $R_{\mathrm{g}-}$ and $R_{\mathrm{g}+}$ terminals, an external gain resistor, and a “data guard” connection. Panel C splits the gain resistance into two $R_{\mathrm{g}}/2$ elements and buffers their midpoint toward the cable shield through 100Ω.

Panel D opens an INA116 block to show selected internal circuitry: two +1 buffers, two amplifier stages, 25k resistors, external $R_{\mathrm{g}}$, and separate guard paths. Dashed continuation leads and “etc” indicate omitted internal detail. Panel E uses separate left-facing guard buffers associated with the two inputs and 100 resistors in their shield-drive paths.

## Inferred lessons to review

- Combine detailed, functional-block, and partial-internal views when comparing implementations of one concept.
- Use unequal panel sizes to accommodate complexity while keeping panel labels and the shared caption clear.
- Preserve the distinct meanings of signal conductors, driven guards, grounded shields, and continuation marks.
- Use compact left-facing buffers when they make a returning guard path easier to follow.

These observations remain provisional. Select for multi-panel comparisons, mixed abstraction levels, and shield/guard illustrations. Compare [Figure 5.77](../fig-05-77-instrumentation-amplifier/EXAMPLE.md) for the simpler instrumentation-amplifier layout and [Figure 5.64](../fig-05-64-differential-signals/EXAMPLE.md) for balanced cable illustrations. Do not treat all shields as ground or infer unseen circuitry from the partial block. Source performance claims remain attributed to the caption; obtain the image for recreation.

[Collection guide](../STYLE.md) · [Available visual examples](../README.md)
