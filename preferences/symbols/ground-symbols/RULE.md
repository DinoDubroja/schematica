# Circuit ground and protective earth

ID: G-SYMBOL-03
Status: accepted
Decision date: 08-11-2026

## Rule and scope

For electronic **circuit ground**, use either a single horizontal bar or an open,
downward-pointing triangle. Both are accepted; neither has been selected as the
default. Reserve the **three decreasing horizontal bars for protective earth (PE)**.
Preserve the intended electrical role; circuit ground and PE are not interchangeable.
Apply [shared precedence](../../GENERAL.md#apply-preferences).

Let **w** be the wire stroke width and **W = 25w** the common symbol width.
Use these proportions:

| Symbol | Geometry |
| --- | --- |
| Single-bar circuit ground | Horizontal bar of length W |
| Open-triangle circuit ground | Downward triangle of width W and height W/2; width-to-height ratio 2:1 |
| Protective earth | Three centered horizontal bars of lengths W, 2W/3 and W/3, from top to bottom; equal vertical centre-line spacing W/6 |

Measure lengths, widths and heights along stroke centre lines. They are not the
outer ink bounds: round caps and outlines extend by half a stroke beyond the
underlying geometry. This measurement convention is specific to these symbols;
the terminal-circle and junction-dot rules retain their visible-diameter definitions.

Use the same stroke thickness and ink as the wires, with round line caps and joins.
Keep the triangle hollow. Center the symbol on its vertical connection stem, meeting
the midpoint of the top horizontal line. For isolated symbol samples, use a stem
length W; in a circuit, the connecting wire length follows the required layout.

Scale all these dimensions with wire thickness, including when the complete drawing
is resized. The native wire width comes from
[G-CONNECTION-04](../../connections/wire-thickness/RULE.md).
At its 0.65 pt default, W is 16.25 pt, the triangle height is 8.125 pt, and PE bar
spacing is 16.25/6 pt. Use the exact ratios rather than rounded decimal dimensions.

## Exceptions and exclusions

This is a schematic presentation preference, not a specification for physical
equipment markings or protective-earth installation. It does not establish whether
a circuit-ground net is bonded to PE, add a connection, merge different ground nets,
or change supplied ground labels. If the role is materially ambiguous, resolve it
before assigning a symbol. Chassis-ground symbols and distinctions between multiple
circuit-ground domains are outside this rule.

No filled-triangle variant or additional aspect ratio was adopted. Historical
examples are not automatically redrawn. Example font size and inter-symbol spacing
remain illustrative, not general defaults.

## Evidence and history

The user requested symbol-only comparisons, removing surrounding circuitry for this
topic. They selected A2 (single bar), B1 (open triangle with 2:1 width-to-height ratio)
and D1 (compact three-line PE with bar lengths in a 3:2:1 ratio and width-to-stack-height
ratio 3:1). These aspect ratios refer to centre-line geometry.

After discussing wire-relative sizing, the user explicitly authorized the final
size and save: "Yes, let's use 25× wire width and save the preference and examples
in the repo. Keep A2 and B1 for circuit ground and D1 for PE earth."
This supersedes the assistant's unsaved 26w size proposal. See
[the decision and validation](../../../context/LOG.md#ground-symbols-25-widths).

## Illustrations and reproduction

[README.md](README.md) shows the three accepted standalone symbols at the same scale,
with labels identifying their roles. These are focused generated examples based on
the reviewed A2/B1/D1 shapes, normalized to the user-approved 25w width. They are not
historical screenshots. The unselected comparison variants are not presented as Bad.

Compile [drawing.tex](drawing.tex) into an ignored build directory and export with
[export_svg.py](../../../scripts/export_svg.py), `--stem good --png`.
Follow [the presentation procedure](../../../scripts/PRESENTATION.md).
