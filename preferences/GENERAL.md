# General schematic preferences

Shared defaults for Schematica, independent of the selected visual style. Read this file before a style guide when creating, editing, or reviewing an illustration. Apply each preference only to its stated scope. The [example workflow](../skills/schematica-examples/SKILL.md#agent-suggestions) describes how suggestions become accepted guidance.

## Apply preferences

Resolve a drawing choice in this order:

1. The user's current explicit requirement for that drawing.
2. An explicit exception in the selected style guide, for the stated rule and condition.
3. An accepted general preference below.

A style inherits every applicable general preference it does not explicitly override. A different-looking reference, silence in a style guide, or an inferred pattern is not an override. State an exception in the style guide with the general rule ID, replacement behavior, scope, and decision/evidence. An exception replaces only the specified part of a rule.

Preferences govern presentation, not the circuit itself. Preserve the supplied connectivity, device roles, values, polarities, identifiers, and technical meaning unless the user explicitly requests a technical change. Resolve material ambiguity before changing it; a visual style cannot authorize a circuit redesign.

When no accepted preference applies, use the task and relevant examples to make a reasonable local choice. Do not turn that choice into a permanent requirement. In particular, one drawing's font size or component spacing is not a universal numeric default.

## Accepted preferences

### G-SYMBOL-01 — Supply and signal terminals

- **Rule:** Use arrows for supply-rail connections and hollow circles for exposed signal input/output terminals. Keep these symbol roles distinct. A request to change signal-terminal appearance does not change supply symbols.
- **Scope:** Supply and signal-terminal symbols in schematics. This does not prescribe the appearance of ground, junctions, current-direction arrows, connector pin drawings, or unrelated annotations.
- **Reason:** A similar geometric position or the broad word "terminal" does not make different electrical roles interchangeable.
- **Evidence and decision:** The user corrected the supply circles introduced during the output-stage trial and approved this shared preference on 08-11-2026; see the [correction and implementation decision](../context/LOG.md#general-preferences-implementation). The trial remains outside the saved example collection; its source/preview must not be claimed as available from this file.
- **Exceptions:** Apply an explicit current-task requirement or a documented style exception under the precedence above. The Art of Electronics collection currently declares no exception.

## Suggestions awaiting a decision

None currently. This section is inactive: entries here must not be applied as accepted general preferences.

Keep a concise entry when a meaningful suggestion has actually been presented during an authorized Schematica session. Record its stable ID, proposed scope (general, named style, or current example), exact proposed rule, reason, supporting example/correction, and status (`proposed`, `deferred`, or `rejected`). Mark an assistant inference as an inference. Link to existing evidence rather than copying entire discussions or duplicating drawings.

After approval, move the rule to its authoritative destination: accepted shared rules here, style-specific rules/exceptions in the selected `STYLE.md`, or local feedback in the example record. Retain a short decision reference so the same rejected suggestion is not repeatedly offered. A repeated pattern, positive reaction, or unanswered proposal is not approval. Explicit instructions to save a clearly scoped rule are sufficient; do not ask again.

Saving guidance does not require revising historical examples. Offer any broader redraw separately. Keep future sections such as layout, typography, routing, and annotations evidence-driven; do not fill them with unreviewed defaults merely to complete a checklist.
