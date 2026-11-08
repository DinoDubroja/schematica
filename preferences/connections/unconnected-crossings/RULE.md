# Unconnected wire crossings

ID: G-CONNECTION-03
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Where wires cross without an electrical connection, draw straight, uninterrupted
wires with no junction circle by default. Do not use a gap or break to indicate
that the crossing wires are unconnected.

Use these names as drawing-instruction keywords:

- **straight wire crossing** selects the default uninterrupted crossing.
- **bridged wire crossing** selects a semicircular bridge instead.
  **wire bridges** remains an equivalent alias for the bridge variant.

Apply the chosen style to the requested drawing, or only the explicitly named
crossings if the request is local. A descriptive mention of a keyword is not an
instruction to change a drawing. Neither style has a junction circle, and the
choice never changes electrical connectivity.

Apply [shared precedence](../../GENERAL.md#apply-preferences) across schematic
styles. Connected crossings and T-junctions must follow
[G-CONNECTION-02: Explicit wire junctions](../explicit-wire-junctions/RULE.md);
the bridge keyword never overrides their required connection markers.

## Exceptions and exclusions

The gap prohibition applies to depicting unconnected crossings. It does not
prohibit a real open circuit, switch contact separation or another intentional
electrical break. Preserve each wire's continuity and the supplied circuit's
intended connectivity.

## Evidence and history

In the reviewed chat comparison the user selected the plain crossing (A) as the
default, accepted a semicircular bridge (C) as a keyword-selected alternative,
and rejected the gap crossing (B). They requested separating this rule from
connected-junction marking and explicitly authorized saving both rules and
Good/Bad examples, choosing the exact keyword "wire bridges". See
[the decision](../../../context/LOG.md#separate-junction-and-crossing-rules).

The user subsequently requested showing the straight and bridged styles together
in one table, giving each its name/keyword and marking the straight style
"(default)". The gap remains a Bad example below the accepted variants. The
earlier "wire bridges" keyword remains supported. See
[the presentation correction](../../../context/LOG.md#wire-width-and-crossing-variants).

## Illustrations and reproduction

[README.md](README.md) shows straight and bridged crossings side by side as two
accepted variants, using their names/keywords as column headings and marking the
default. The rejected gap crossing appears below them. All use the same scale
and intend two continuous wires with no connection between them. The variants
belong to this rule, not separate preference categories.

These are focused generated examples based on the reviewed A/B/C geometry,
not historical screenshots. The conventions and save are user-approved; the
newly exported assets require their own visual review.

Compile [drawing.tex](drawing.tex) into an ignored build directory. Export pages
1, 2 and 3 with stems `good`, `bad` and `bridge`, respectively, including PNGs,
using [export_svg.py](../../../scripts/export_svg.py). Follow
[the presentation procedure](../../../scripts/PRESENTATION.md).
