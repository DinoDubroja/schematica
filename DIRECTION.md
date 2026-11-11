# Project direction

Schematica aims to enable AI agents to automatically create beautiful, useful electronics illustrations with CircuitikZ and TikZ from text prompts, sketches, or screenshots. Its scope includes schematics, conceptual diagrams, waveforms, plots, equations, and combinations of these. It is intended for engineering documentation, papers, teaching, and in-chat discussions with ChatGPT or other AI agents.

It should be available for anyone to use in their agent environment and work well from the first prompt.

It should come with consistent, predefined drawing preferences. Users should be able to modify and save their preferences without having to establish everything from scratch. The user's circuit connections, component names, and supplied values should be preserved.

## Agreed first-release direction

The first release will be an agent integration using MCP as its tool interface.
Support for Claude Desktop and OpenAI/ChatGPT is required from the start; exact
supported application surfaces and setup must be verified through real user tests.
The existing local Codex installation is not evidence of those integrations working.

The library and rendering capabilities should be shared with a later app or web app.
The first release still needs a minimal visual catalogue: a user must be able to
create/save a symbol, see it in their catalogue, and reuse it in a later session.
Establish the underlying library and user-data structure before growing it broadly.
Keep development separate from realistic first-time-user testing with an isolated
fictional user. A polished application interface can follow later.

Develop through small working prototypes and document consequential decisions one
at a time. Focus first on schematics; preserve existing rules, symbols, references,
and unfinished ideas with their actual approval and implementation status. Exact
storage, profiles versus styles, grid conventions, transport, and packaging remain
open. See the [repository review and proposed migration](context/MCP_TRANSITION_REVIEW.md).

## Development approach

- Preserve selected source images with their captions as visual references; recreate selected favorites in CircuitikZ when an editable drawing or theme-aware SVG is wanted.
- Compare examples from the same circuit category, infer recurring design patterns, and document the agreed lessons.
- Use realistic circuits and functional subsystems for demonstrations.
- Provide prompts and inputs users can run with and without Schematica to compare results themselves.
- Document useful examples and conclusions as development progresses.

Present illustrations and visual comparisons directly in chat by default, using native visual capabilities and transparent, theme-aware SVG for generated drawings; follow [chat behavior](agents/BEHAVIOR.md#presenting-illustrations). Explicit requests for another format or destination take precedence. Authorized saved examples retain PNG downloads alongside their source and SVGs. Original reference images may display directly in their original format and background; no recreation or theme conversion is required.

## Style collections

General conventions live in a [visual preference bank](preferences/README.md), separate from source-specific styles. The [agent index](preferences/GENERAL.md) selects relevant pages and defines precedence; each rule folder separates its authoritative `RULE.md` (scope and evidence) from a minimal visual `README.md` with a good example and an optional bad example. Category galleries assemble those presentations; [project rules](agents/PROJECT_RULES.md) define their maintenance. Ordinary corrections can develop this bank through agent suggestions and scoped user approval. Styles inherit general preferences unless they declare an explicit exception.

Each source/style has a collection under `styles/`. [INDEX.md](styles/INDEX.md) routes agents to its `STYLE.md`, which owns shared guidance, domain selection, collection status, and the example inventory. Domain guides such as `SCHEMATICS.md` and `PLOTS.md` hold the corresponding guidance and selection cues. A source can later support writing guidance when there is actual content; this organization does not create a writing style. Read only the domains needed for the task and inspect relevant examples rather than the entire library.

Examples live under each collection's `examples/<category>/<example>/`. Existing categories are `schematics`, `plots`, and `mixed`; create other guides or categories only when supported by content. Keep mixed figures intact in one folder and link them from all relevant domain guides. General preferences remain outside `styles/` and apply only within their stated scope; explicit style exceptions belong in the relevant domain guide, or `STYLE.md` when shared, with discovery links from `STYLE.md`.

Each collection has a short `README.md` showcase of selected highlights, linking to `examples/README.md` and category galleries for all references. The user chooses showcase favorites; existing SVGs can serve as temporary highlights. Each example with a saved image has its own `README.md` with the picture, a brief explanation, caption/source information, and file links. Detailed agent guidance stays in `STYLE.md`, domain guides, and `EXAMPLE.md`. Public installation or invocation instructions belong in the main README only once that workflow is established.

Each example has an `EXAMPLE.md` record with caption, source, feedback, and accurate asset/review status. An original image saved within the approved scope is a complete visual reference: retain its bytes in `reference.png` (or its original format) and show it on its human page. An optional recreation adds editable LaTeX, transparent light/dark SVGs, and a PNG export alongside the original. Records without saved images remain discoverable as notes, explicitly marked as unavailable for visual inspection. Saving images does not authorize generalizing their style, adopting rules, or recreating them.

Reference examples and generated examples use the same record format. Origin is distinct from evaluation: either origin may have useful, deficient, or still-unreviewed aspects. Recreating a book figure does not change its reference origin.

The [collection workflow](skills/schematica-preferences/SKILL.md) supports starting, resuming, adding examples, and reviewing a style. It preserves enough state for a fresh chat to continue without the original conversation.

## Learn through use

Generate new illustrations using a developing style, review them with the user, and iterate. When a result or correction has reusable value, offer to document the specific example and lesson. Save after approval, including the relevant prompt, feedback, and useful intermediate versions. A positive reaction alone is not permission to save or publish.

The agent should notice useful preservation opportunities so the user need not manage documentation manually. The user controls what becomes lasting guidance. Agreed collection scope can cover routine incoming examples without repeated permission requests.

## Current limits and later work

The first collection is The Art of Electronics. Five reference recreations have editable LaTeX, SVG previews, PNG downloads, captions, and browsing pages; the [style guide](styles/THE_ART_OF_ELECTRONICS/STYLE.md) tracks all collected references and their asset availability. The shared style remains provisional. A separate practical output-stage trial has been drawn and refined after initial feedback, but it has not been approved for the permanent collection; see [the current checkpoint](context/CURRENT.md).

The first local installation route bundles the preferences-and-examples skill with
the complete library; see [installation and use](INSTALL.md). A user explores options
in chat and saves approved changes in their selected copy. Automated preservation of
personal changes across package upgrades, plugin distribution and generalization to
other artifact domains remain to be designed. Difference-only storage for intermediate
versions is also undecided. Start with complete files for selected useful revisions.
