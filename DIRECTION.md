# Project direction

Schematica aims to enable AI agents to automatically create beautiful, useful electronics illustrations with CircuitikZ and TikZ from text prompts, sketches, or screenshots. Its scope includes schematics, conceptual diagrams, waveforms, plots, equations, and combinations of these. It is intended for engineering documentation, papers, teaching, and in-chat discussions with ChatGPT or other AI agents.

It should be available for anyone to use in their agent environment and work well from the first prompt.

It should come with consistent, predefined drawing preferences. Users should be able to modify and save their preferences without having to establish everything from scratch. The user's circuit connections, component names, and supplied values should be preserved.

## Development approach

- Recreate selected good schematics in CircuitikZ so the examples themselves provide guidance.
- Compare examples from the same circuit category, infer recurring design patterns, and document the agreed lessons.
- Use realistic circuits and functional subsystems for demonstrations.
- Provide prompts and inputs users can run with and without Schematica to compare results themselves.
- Document useful examples and conclusions as development progresses.

Present schematics inline using transparent, theme-aware SVG by default in chat. GitHub galleries also display SVG, selecting light or dark ink for the active site theme. Keep PNGs as convenient downloads. Explicit requests for another format or save location take precedence.

## Example collections

General conventions live in a [visual preference bank](preferences/README.md), separate from source-specific styles. The [agent index](preferences/GENERAL.md) selects relevant pages and defines precedence; each rule folder separates its authoritative `RULE.md` (scope and evidence) from a minimal visual `README.md` with a good example and an optional bad example. Category galleries assemble those presentations; [project rules](agents/PROJECT_RULES.md) define their maintenance. Ordinary corrections can develop this bank through agent suggestions and scoped user approval. Styles inherit general preferences unless they declare an explicit exception.

Each style has a collection under `examples/`. `INDEX.md` routes agents to relevant `STYLE.md` documents; each style document explains shared patterns and helps select particular examples. Agents inspect relevant rendered examples and their context rather than reading the entire library on every task.

Each collection also has a short `README.md` visual gallery for people. The main README links to that gallery, and each developed example has its own `README.md` with the picture, a brief explanation, caption/source information, and links to its files. Detailed agent guidance stays in `STYLE.md` and `EXAMPLE.md`. The main README presents available work; public installation or invocation instructions belong there only once the user-facing workflow is established.

Each example has an `EXAMPLE.md` record with its caption, source, feedback, distinctive lessons, and review status. A developed visual example includes editable LaTeX source, transparent light/dark SVG previews, and a PNG rendered from the same source. A caption/feedback-only record may preserve an incoming reference while recreation awaits authorization, but must be identified as pending rather than presented as a completed gallery example. Original screenshots are working inputs, not repository deliverables. Captions belong with examples in the repository.

Reference examples and generated examples use the same record format. Origin is distinct from evaluation: either origin may have useful, deficient, or still-unreviewed aspects. Recreating a book figure does not change its reference origin.

The [collection workflow](skills/schematica-examples/SKILL.md) supports starting, resuming, adding examples, and reviewing a style. It preserves enough state for a fresh chat to continue without the original conversation.

## Learn through use

Generate new illustrations using a developing style, review them with the user, and iterate. When a result or correction has reusable value, offer to document the specific example and lesson. Save after approval, including the relevant prompt, feedback, and useful intermediate versions. A positive reaction alone is not permission to save or publish.

The agent should notice useful preservation opportunities so the user need not manage documentation manually. The user controls what becomes lasting guidance. Agreed collection scope can cover routine incoming examples without repeated permission requests.

## Current limits and later work

The first collection is The Art of Electronics. All five references have editable LaTeX, SVG previews, PNG downloads, captions, and browsing pages. The shared style remains provisional. A separate practical output-stage trial has been drawn and refined after initial feedback, but it has not been approved for the permanent collection; see [the current checkpoint](context/CURRENT.md).

Personal customization and storage, plugin distribution, and generalization to other artifact domains remain to be designed. Difference-only storage for intermediate versions is also undecided. Start with complete files for selected useful revisions.
