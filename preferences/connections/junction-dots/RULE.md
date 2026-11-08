# Junction dots

ID: G-CONNECTION-01
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Draw a wire-junction marker as a solid, round disk in the same ink color as the
wires, centered exactly on their meeting point. Use no contrasting outline or
hollow interior. Set its diameter to **ten times the wire stroke width** and
keep that proportion consistent throughout a drawing, including after scaling.

For example, a 0.65 pt wire uses a 6.5 pt diameter dot (3.25 pt radius).
The ten-to-one ratio is the accepted default; the example's absolute wire width
is not a universal line-weight rule. In TikZ, a filled circle with `radius=5\pgflinewidth`
implements this proportion when the current line width is the wire width.
With CircuitikZ, set the junction-node dimensions to the same visible diameter;
verify the rendered size rather than relying on a package default.

Apply to junction markers across schematic styles using
[the common precedence](../../GENERAL.md#apply-preferences).
This belongs under Connections because it describes wire connectivity.

## Exceptions and exclusions

Preserve the supplied circuit connectivity. This appearance rule does not require
adding dots at every bend or ordinary two-wire continuation, and never permits
marking an unconnected crossing as connected. It does not change the role or
dimensions of [hollow signal terminals](../../symbols/signal-terminal-circles/RULE.md)
or [supply arrows](../../symbols/power-supply-arrows/RULE.md).
The current request or an explicit style exception can override the proportion
for its stated scope.

## Evidence and history

The user identified the junction dots in both supply-symbol examples as too small
and explicitly requested correcting them and adding a general preference for
junction-circle style and size. The user also asked for a category beyond Symbols
to be considered. See [the decision](../../../context/LOG.md#junction-dots-and-labels).

The assistant initially chose a five-to-one ratio and the Connections category.
The user then explicitly requested trying seven times the wire width and viewing
Good/Bad examples side by side; see [the trial](../../../context/LOG.md#side-by-side-seven-width-junctions).
After reviewing an equal-scale 7x/10x comparison in chat, the user said "10x looks
better" and explicitly requested adopting it and updating the preference and
examples. The ten-to-one ratio is now accepted, replacing the earlier trials.
See [the approval](../../../context/LOG.md#ten-width-junction-adoption).

## Illustrations and reproduction

[README.md](README.md) contains focused generated illustrations of the same
three-way and four-way connected junctions. Only dot size differs: Good uses the
ten-to-one ratio; Bad uses the former supply-example radius of 1.2 pt at the
same 0.65 pt wire width. The rejected feature is the undersized dot.
These are new demonstrations, not historical screenshots.

Compile [drawing.tex](drawing.tex) into an ignored build directory. Page 1 is Good;
page 2 is Bad. Export using [export_svg.py](../../../scripts/export_svg.py) with
`--page 1 --stem good --png` and `--page 2 --stem bad --png`.
See [the presentation procedure](../../../scripts/PRESENTATION.md).
