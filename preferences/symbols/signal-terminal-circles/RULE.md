# Input/output terminal circles

ID: G-SYMBOL-02
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Use hollow circles for exposed signal input/output terminals. Apply across schematic
styles to signal ports; use [the common precedence](../../GENERAL.md#apply-preferences).
Keep the interior open against the drawing background, with no wire through it.
Use the wire's ink color and stroke width for the circle outline. Set the visible
**outer diameter to twelve times the wire stroke width**, including the outline.
Keep this proportion consistent throughout the drawing, including after scaling.

For example, a 0.65 pt wire uses a 7.8 pt outer diameter and a 0.65 pt outline.
The absolute wire width is illustrative, not a universal line-weight default.
For a TikZ stroked circle, `radius=5.5\pgflinewidth` gives the required outer
diameter when its outline uses the wire width. The visible outer radius is
`6\pgflinewidth`; terminate the attached wire at that edge without entering the
hollow interior. For package-provided terminals, verify the rendered outer
diameter rather than assuming that a node-size parameter includes its stroke.

## Exceptions and exclusions

The current request or an explicit style exception can replace this convention for
its stated scope. This rule does not choose supply symbols, ground symbols, junction
dots, connector-pin symbols, absolute wire width, or font size. Supply
connections are covered independently by [G-SYMBOL-01](../power-supply-arrows/RULE.md).

## Evidence and history

The user's output-stage correction explicitly requested hollow signal terminals.
They stayed hollow when supply arrows were restored; see the
[original decision](../../../context/LOG.md#visual-preference-bank).
This was originally the signal clause of combined G-SYMBOL-01. The authorized
[migration](../../../context/LOG.md#preference-bank-migration) assigns it G-SYMBOL-02,
preserving that approval and separating it from supply-symbol changes.

The user later compared hollow terminal circles with outer diameters of 8, 10
and 12 times the wire width, with the outline held equal to the wire width and
a fixed 10-times solid junction dot as a reference. They selected C and explicitly
requested adopting 12 times the wire width and updating the preference and
examples. This establishes the terminal size previously left unspecified; it
does not change the separate junction-dot size. See
[the size decision](../../../context/LOG.md#twelve-width-terminal-circles).

## Illustrations and reproduction

[README.md](README.md) shows a focused reconstruction of input and output terminals,
not historical screenshots or a complete circuit. No bad example is needed to
communicate this rule. The example now uses the approved outer-diameter and
outline proportions for both input and output terminals. Remaining spacing,
absolute wire width and typography are illustrative, not additional defaults.

Compile [drawing.tex](drawing.tex) into an ignored build directory and export with
[export_svg.py](../../../scripts/export_svg.py), `--page 1 --stem good --png`;
see [the presentation procedure](../../../scripts/PRESENTATION.md).
