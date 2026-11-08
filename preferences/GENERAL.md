# General schematic preferences

Agent index and precedence for shared Schematica preferences. Read this file before a style guide, then read the applicable preference pages listed below, including their visuals. Each preference page is authoritative for its rule; this index does not duplicate its text. Apply each rule only to its stated scope. Humans can [browse the visual gallery](README.md). The [example workflow](../skills/schematica-examples/SKILL.md#agent-suggestions) describes how suggestions become accepted guidance.

## Apply preferences

Resolve a drawing choice in this order:

1. The user's current explicit requirement for that drawing.
2. An explicit exception in the selected style guide, for the stated rule and condition.
3. An accepted general preference linked below.

A style inherits every applicable general preference it does not explicitly override. A different-looking reference, silence in a style guide, or an inferred pattern is not an override. State an exception in the style guide with the general rule ID, replacement behavior, scope, and decision/evidence. An exception replaces only the specified part of a rule.

Preferences govern presentation, not the circuit itself. Preserve the supplied connectivity, device roles, values, polarities, identifiers, and technical meaning unless the user explicitly requests a technical change. Resolve material ambiguity before changing it; a visual style cannot authorize a circuit redesign.

When no accepted preference applies, use the task and relevant examples to make a reasonable local choice. Do not turn that choice into a permanent requirement. In particular, one drawing's font size or component spacing is not a universal numeric default.

## Accepted preferences

| ID and preference | Read when | Evidence available |
| --- | --- | --- |
| [G-SYMBOL-01: Supply and signal terminals](supply-and-signal-terminals/README.md) | Drawing or changing supply connections or exposed signal ports | Accepted rule, before/after illustrations, editable source, and user correction |

Select by the feature being drawn or reviewed, not by the style name. A style may point directly to a rule ID, but must not copy a competing version of the rule. Only entries explicitly marked accepted are active defaults.

## Suggestions awaiting a decision

None currently. This section is inactive: entries here must not be applied as accepted general preferences.

Keep a concise entry when a meaningful suggestion has actually been presented during an authorized Schematica session. Record its stable ID, proposed scope (general, named style, or current example), exact proposed rule, reason, supporting example/correction, and status (`proposed`, `deferred`, or `rejected`). Mark an assistant inference as an inference. Link to existing evidence rather than copying entire discussions or duplicating drawings.

After approval, move the rule to its authoritative destination: one visual preference page for an accepted general rule, the selected `STYLE.md` for a style-specific rule/exception, or the example record for local feedback. Maintain the index and gallery links after that save. Retain a short decision reference so the same rejected suggestion is not repeatedly offered. A repeated pattern, positive reaction, or unanswered proposal is not approval. Explicit instructions to save a clearly scoped rule are sufficient; do not ask again.

Saving guidance does not require revising historical examples. Offer any broader redraw separately. Keep future sections such as layout, typography, routing, and annotations evidence-driven; do not fill them with unreviewed defaults merely to complete a checklist.
