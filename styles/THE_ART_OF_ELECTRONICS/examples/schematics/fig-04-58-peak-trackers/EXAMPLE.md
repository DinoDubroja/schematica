# Op-amp peak trackers

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.58. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** both source panels visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is optional and has not been requested. The original image is not saved in the repository.

## Original caption

> **Figure 4.58.** A. Op-amp peak detector (more accurately, a “peak tracker”). B. Improved peak tracker responds to short peaks, because the input op-amp does not have to slew from negative saturation.

Caption transcribed with line wrapping and print line-break hyphenation normalized. Its explanation is attributed to the source.

## What it demonstrates

Two vertically stacked panels compare related two-op-amp circuits. Both use $V_{\mathrm{in}}$, $V_{\mathrm{out}}$, a storage capacitor, and clearly separated feedback paths. Large A/B labels sit below-left of each circuit.

Panel A places the first op-amp above-left of the second. A downward diode connects its output to the storage node, with feedback returning to its negative input. Two nearby junction dots distinguish branches on the storage-node wire. The second op-amp is a follower. The capacitor is labeled C without a numeric value.

Panel B aligns U1 and U2 more horizontally. A diode lies between stages, and a second diode connects the upper feedback route to U1's output. The storage capacitor is C, 1nF. A 1k resistor precedes U2's positive input; a 20k resistor occupies the long upper path. Feedback loops remain visually separated from the signal route.

## Inferred lessons to review

- Keep panel labels and port names consistent while allowing layout to change with topology.
- Give feedback loops enough routing space to preserve diode direction and unambiguous junctions.
- Use the caption to explain the comparison without filling the circuit itself with prose.

These observations remain provisional. Select for multi-op-amp feedback routing and stacked circuit comparisons. Obtain the source image for recreation; the record is not a complete wiring specification. General symbol preferences remain unchanged.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
