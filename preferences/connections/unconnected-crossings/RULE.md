# Unconnected wire crossings

ID: G-CONNECTION-03
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Where wires cross without an electrical connection, draw straight, uninterrupted
wires with no junction circle by default. Do not use a gap or break to indicate
that the crossing wires are unconnected.

The keyword **wire bridges**, used as an instruction for a drawing, selects
semicircular wire bridges at its unconnected crossings instead. Apply it to the
requested drawing, or only the explicitly named crossings if the request is
local. A descriptive mention of the keyword is not an instruction to change a
drawing. A bridge has no junction circle and does not change connectivity.

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

## Illustrations and reproduction

[README.md](README.md) compares the default straight crossing with the rejected
gap crossing at the same scale. Both examples intend two continuous wires with
no connection between them. A separate illustration shows the accepted bridge
variant and its trigger. Good/Bad evaluate the stated feature; the variant is
part of this rule, not a separate preference category.

These are focused generated examples based on the reviewed A/B/C geometry,
not historical screenshots. The conventions and save are user-approved; the
newly exported assets require their own visual review.

Compile [drawing.tex](drawing.tex) into an ignored build directory. Export pages
1, 2 and 3 with stems `good`, `bad` and `bridge`, respectively, including PNGs,
using [export_svg.py](../../../scripts/export_svg.py). Follow
[the presentation procedure](../../../scripts/PRESENTATION.md).
