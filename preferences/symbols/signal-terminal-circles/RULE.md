# Input/output terminal circles

ID: G-SYMBOL-02
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Use hollow circles for exposed signal input/output terminals. Apply across schematic
styles to signal ports; use [the common precedence](../../GENERAL.md#apply-preferences).
Keep the interior open against the drawing background.

## Exceptions and exclusions

The current request or an explicit style exception can replace this convention for
its stated scope. This rule does not choose supply symbols, ground symbols, junction
dots, connector-pin symbols, line weight, font size, or terminal dimensions. Supply
connections are covered independently by [G-SYMBOL-01](../power-supply-arrows/RULE.md).

## Evidence and history

The user's output-stage correction explicitly requested hollow signal terminals.
They stayed hollow when supply arrows were restored; see the
[original decision](../../../context/LOG.md#visual-preference-bank).
This was originally the signal clause of combined G-SYMBOL-01. The authorized
[migration](../../../context/LOG.md#preference-bank-migration) assigns it G-SYMBOL-02,
preserving that approval and separating it from supply-symbol changes.

## Illustrations and reproduction

[README.md](README.md) shows a focused reconstruction of input and output terminals,
not historical screenshots or a complete circuit. No bad example is needed to
communicate this rule. The image illustrates the accepted convention; incidental
dimensions and typography are not separately approved defaults.

Compile [drawing.tex](drawing.tex) into an ignored build directory and export with
[export_svg.py](../../../scripts/export_svg.py), `--page 1 --stem good --png`;
see [the presentation procedure](../../../scripts/PRESENTATION.md).
