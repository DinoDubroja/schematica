# Roadmap

Schematica should help people and agents make clear, consistent electronic drawings.
The website is a place to browse and compare symbols, styles and examples, and later
find personal presets and created schematics. Keep its everyday controls minimal.

## Broad milestones

| Outcome | Status | What it means |
|---|---|---|
| Minimal symbol library in the web app | Implemented | Browse, search, compare sizes/strokes, use dark/light mode and export one symbol or the whole Inkscape library |
| Grow a consistent supplied library with agent-run batches | First batch implemented | A finite resistor inventory, repeatable creation and validation, and human verification; more component families remain to be planned |
| Create symbols interactively with an agent | Near term · missing | A symbol-creation skill that discusses intent, shows alternatives, renders, checks and refines designs; shares tools and formats with batch production |
| Connect Schematica to agent apps through MCP | Near term · missing | Let supported Claude/Codex and cloud-hosted agent workflows find, inspect, create and reuse symbols; demonstrate a complete working journey |
| Personal libraries alongside supplied originals | Near term · missing | Sign-in, account-linked preferences, custom symbols/designs and separate personal variants; admin privileges for maintaining the supplied library |
| Schematic styles and examples in the library | Future · deferred | Browse coherent drawing styles, show symbols in circuits, compare alternatives in context, and let an agent use a selected style |
| Create and revisit complete schematics | Future · deferred | Find recent creations, search organized libraries and personal presets, and continue working on schematics through agent integrations and later the app |

These are product outcomes, not a step-by-step implementation plan. The detailed
priority interview is unfinished; the order among the near-term milestones has
not been agreed. Only the resistor batch and temporary verification workflow are
authorized in the current implementation.

## Decisions that guide the work

- **Creation starts through agent integrations.** A creation skill and interactive
  workflow are explicit goals. In-app agentic creation can follow later.
- **Automate library growth in bounded batches.** Establish an inventory first,
  generate and check every configuration, correct failures, and ask for human
  verification. Automatic checks do not confer human approval.
- **Supplied and personal designs stay distinct.** Personal variants must not
  overwrite supplied originals. Accounts, storage, grouping and admin boundaries
  still need design.
- **The website has a broader future than exporting symbols.** Keep export small;
  support browsing, comparison and reuse without filling the interface with setup
  text or technical details. Descriptions and keywords remain read-only for now.
- **Batch creation and interactive creation are separate workflows** built on
  shared TeX drawing tools, semantic definitions and validation rules.
- **Beautiful drawings come first.** Simulation, automatic routing, sketch/PDF
  interpretation and component sourcing remain outside the present scope.

The [MCP transition review](https://github.com/DinoDubroja/schematica/blob/docs/mcp-transition-review/context/MCP_TRANSITION_REVIEW.md)
records earlier integration discussion. Its proposed host-first sequence,
ground-symbol prototype, legacy-gallery migration and wire-relative defaults are
not current implementation instructions. The accepted geometry and later product
decisions take precedence.

## Current limits

| Area | What remains |
|---|---|
| Human verification | The 22 new resistor designs await the user's review; six earlier designs retain acceptance |
| Temporary approvals | Browser-local pending selections and a chat-mediated publish step; no accounts or cross-device selection sync |
| Text editing | Bounded editable-label proof only; no general mathematical-text round trip |
| Device readiness | Repeat the current hosted and local checklist on the laptop; desktop results do not establish laptop behavior |
| Rendering setup | Clean-machine/offline TeX setup is not demonstrated |
| Inkscape setup | Profile-wide Symbols installation and a fresh grid-snapping GUI walkthrough remain unverified |

[Batch inventory and results](RESISTOR_BATCH.md) · [Verification handoff](VERIFICATION.md)
· [Development and tests](../DEVELOPMENT.md)

## Archive and deliberate reuse

Old Schematica and obsolete implementation reports are preserved in a verified,
dated archive under the workspace's sibling `Archive/` folder, outside this Git
checkout. It includes Git history, original working files, ignored experiments,
both worktree snapshots and a recovery guide. Git history also remains intact.
The archive is consulted only for a specific reuse task; it is not a reading route
or source of defaults for this app. The local archive is not synchronized by Git.

| Material retained | Reason |
|---|---|
| Accepted palette PDF and its TeX source | Independent geometry/stroke regression reference for this batch |
| Frozen accepted paths for 54 configurations | Detect unintended artwork changes during refactors |
| Named-part, repeated-ID and editable-label fixtures | Exercise real converter and serialization failure modes |
| Native CircuitikZ example | Verify generated helpers and named connection coordinates |

No legacy gallery builder, installer, preference skill, AOE collection or legacy
test is required by the new implementation. The retained fixture provenance is
documented [with the fixtures](../tests/fixtures/README.md).
