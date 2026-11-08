# Explicit wire junctions

ID: G-CONNECTION-02
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Make every electrical branch connection explicit with a solid junction circle
centered on the meeting point. This includes every T-junction and four-way
junction: wherever three or more wire branches connect, the circle is required.
Do not rely on touching or intersecting lines alone to indicate that connection.

Both a single four-way junction and two staggered T-junctions are acceptable.
Mark each actual junction in either layout; neither layout is preferred by this
rule. Preserve the circuit's intended connectivity.

Use [G-CONNECTION-01: Junction dots](../junction-dots/RULE.md) for the marker's
appearance and size. This rule specifies where markers are required and does not
define a second size setting. Apply [shared precedence](../../GENERAL.md#apply-preferences)
across schematic styles.

## Exceptions and exclusions

Ordinary wire bends and uninterrupted two-branch continuations do not need dots.
This rule concerns wire branch connections, not the marking of every component
terminal. Never place a junction circle at a crossing that is electrically
unconnected; use [G-CONNECTION-03](../unconnected-crossings/RULE.md) there.

## Evidence and history

The user accepted both four-way and staggered T-junction layouts in the chat
comparison (D and E), requiring an explicit junction circle for connected lines.
They corrected a combined proposal and requested separate rules for connected
junctions and unconnected crossings. They then explicitly authorized saving both
rules and their Good/Bad examples. See [the decision](../../../context/LOG.md#separate-junction-and-crossing-rules).

## Illustrations and reproduction

[README.md](README.md) compares the same intended four-branch connected net in
two layouts. Good marks the four-way junction and both staggered T-junctions;
Bad omits all three required markers. The Bad drawings are deficient depictions
of an intended connected net, not alternative unconnected circuits. Layout,
wire width, scale and canvas are identical across the comparison.

These are focused generated examples based on the reviewed D/E layouts, not
historical screenshots. The rule and save are user-approved; the newly exported
Good/Bad assets require their own visual review.

Compile [drawing.tex](drawing.tex) into an ignored build directory. Export page 1
with stem `good` and page 2 with stem `bad`, including PNGs, using
[export_svg.py](../../../scripts/export_svg.py). Follow
[the presentation procedure](../../../scripts/PRESENTATION.md).
