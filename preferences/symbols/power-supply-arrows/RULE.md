# Power supply arrow symbols

ID: G-SYMBOL-01
Status: accepted
Decision date: 08-11-2026

## Rule and scope

Use arrows for supply-rail connections. A correction to signal-terminal appearance
does not change supply symbols. Apply across schematic styles to exposed supply
connections; use [the common precedence](../../GENERAL.md#apply-preferences).

## Exceptions and exclusions

The current request or an explicit style exception can replace this convention for
its stated scope. This rule does not choose ground symbols, junction dots,
current-direction arrows, connector-pin symbols, or signal-terminal appearance.
See [G-SYMBOL-02](../signal-terminal-circles/RULE.md) for signal terminals.
Arrow orientation follows the rail layout; a negative supply need not always point
down. No universal font size, line weight, or terminal dimensions are implied.

## Evidence and history

In the output-stage trial the user requested hollow signal terminals. The agent also
changed supply arrows to circles; the user corrected that broader interpretation.
The supply-arrow convention and focused visual documentation were approved in the
[original decision](../../../context/LOG.md#visual-preference-bank).

The [migration decision](../../../context/LOG.md#preference-bank-migration) retains
G-SYMBOL-01 for supply arrows and extracts the signal part into G-SYMBOL-02. Earlier
mentions of G-SYMBOL-01 may refer to the combined rule; use these independent records
for future work. The earlier page/assets remain in Git history, not as active rules.

## Illustrations and reproduction

[README.md](README.md) shows a focused reconstruction, not historical screenshots
or the full trial. Only supply endpoints differ between Good and Bad; the rejected
feature is the supply-circle substitution. The images illustrate the accepted rule;
their detailed dimensions and typography are not separately approved defaults,
except for junction-dot proportions now governed by
[G-CONNECTION-01](../../connections/junction-dots/RULE.md). Both illustrations were
updated together after the user's [size correction](../../../context/LOG.md#junction-dots-and-labels).

Compile [drawing.tex](drawing.tex) into an ignored build directory. Page 1 is Good,
page 2 Bad, on equal canvases. Export each with [export_svg.py](../../../scripts/export_svg.py)
using `--page 1 --stem good --png` and `--page 2 --stem bad --png`; see
[the presentation procedure](../../../scripts/PRESENTATION.md).
