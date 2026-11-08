# Wire thickness

ID: G-CONNECTION-04
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Use **0.65 pt** as the default wire stroke width at the drawing's native scale.
Keep the wire weight consistent within a schematic. Apply
[shared precedence](../../GENERAL.md#apply-preferences) across schematic styles.

The point value is a drawing-source dimension, not a fixed screen-pixel width.
Uniformly resizing the whole illustration scales its wires and markers together.
When changing the wire width, preserve the proportions owned by
[G-CONNECTION-01: Junction dots](../junction-dots/RULE.md),
[G-SYMBOL-02: Input/output terminal circles](../../symbols/signal-terminal-circles/RULE.md)
and [G-SYMBOL-03: Circuit ground and protective earth](../../symbols/ground-symbols/RULE.md).
Do not leave these marker or ground-symbol sizes fixed while changing the wire weight.

## Exceptions and exclusions

A current explicit request or a documented style exception can choose another
wire width for its stated scope. This rule does not set component-body outlines,
annotation-line weights, fonts, spacing, or circuit connectivity. Terminal-circle
outlines follow their own linked rule and therefore match the wire width.

## Evidence and history

The user reviewed three equal-scale chat options: A at 0.40 pt, B at 0.65 pt,
and C at 0.90 pt. Junction and terminal diameters retained their previously
accepted proportions in all three. The user chose B with "Lets use B."
This adopts the width already used in the current focused examples as a default.
See [the decision](../../../context/LOG.md#wire-width-and-crossing-variants).

## Illustrations and reproduction

[README.md](README.md) shows the accepted B geometry: a wire branch with a marked
junction, an ordinary unmarked bend, and hollow input/output terminals. This is
a focused generated example from the reviewed trial, not a historical screenshot.
Only the wire width and previously accepted marker proportions are defaults;
the remaining geometry is illustrative. The unselected widths are not labelled Bad.

Compile [drawing.tex](drawing.tex) into an ignored build directory and export with
[export_svg.py](../../../scripts/export_svg.py), `--page 1 --stem good --png`.
Follow [the presentation procedure](../../../scripts/PRESENTATION.md).
