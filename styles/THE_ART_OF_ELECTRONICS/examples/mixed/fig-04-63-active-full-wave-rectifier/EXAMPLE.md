# Active full-wave rectifier

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.63. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** source screenshot visually inspected. Caption, displayed relationships, and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 4.63.** Active full-wave rectifier.

Caption transcribed from the supplied screenshot.

## Relationships shown in the figure

The output is labeled:

$$V_{\mathrm{out}}(t)=|V_{\mathrm{in}}(t)|$$

A curved leader points from a braced two-condition annotation toward the node feeding the R/2 branch:

$$\begin{cases}
-V_{\mathrm{in}} & \text{(if }V_{\mathrm{in}}>0\text{)}\\
R\text{ to GND} & \text{(if }V_{\mathrm{in}}<0\text{)}
\end{cases}$$

These transcribe the source notation. The second line describes an equivalent resistance to ground, not a voltage equal to R; the brace must not be recast as two numerical voltage values. No behavior at exactly zero is added.

## What it demonstrates

Two right-facing op-amps are staggered: the first below-left and the second above-right. Both positive inputs are grounded. The input divides into a long upper path and a lower path containing the first stage and two diodes. Resistors use symbolic ratios R and R/2 rather than numeric values. Filled dots make branch connections visible around the diode network and second-stage summing node.

The output relationship sits immediately below the output. The curved annotation leader occupies whitespace between stages; its arrow is explanatory and does not form an electrical connection. The source mixes “input”/“output” text with mathematical signal labels.

## Inferred lessons to review

- Place a conditional explanation next to the relevant node, using a leader and brace to connect the text visually.
- Keep different kinds of conditions explicit: voltage behavior and an equivalent resistance are not interchangeable quantities.
- Stagger stages to reserve space for local explanations while keeping major signal paths readable.

These observations remain provisional. Select for symbolic component ratios, conditional annotations, and multi-stage composition. Preserve source notation during transcription; this is not a new notation rule or independent circuit validation. Obtain the image for recreation. General terminal preferences remain unchanged.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
