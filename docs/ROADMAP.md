# Roadmap

Schematica should help people and agents make clear, consistent electronic drawings.
The website is a place to browse and compare symbols, styles and examples, and later
find personal presets and created schematics. Keep its everyday controls minimal.

Planning reconciled 14-11-2026 00:55 +01:00. Source timestamps, superseded ideas
and outstanding decisions are in [the decision history](../context/DECISIONS.md#product-direction-recovered-from-chats).
This page states desired capabilities; implementation status comes from
[current status](../context/CURRENT.md).

## Broad milestones

| Outcome | Status | What it means |
|---|---|---|
| Minimal symbol library in the web app | Implemented | Browse, search, compare variations, use dark/light mode and export one symbol or the whole Inkscape library |
| Grow the dev library with agent-run batches | First batch implemented | A finite resistor inventory, repeatable creation and validation, and human verification; more component families remain to be planned |
| Create symbols interactively with an agent | Near term · missing | Create one symbol from text, images, sketches or PDFs: interpret → confirm → create → preview/refine → offer download/save to the dev library; shares formats and checks with batches |
| Search and reuse symbols through agent apps | Near term · planning | Separate search skill; proposed shared interactive web/chat viewer with filtered results, configuration controls and an explicit selection handoff |
| Connect Schematica through MCP | Near term · missing | Required: ChatGPT Desktop across its environments and Claude Desktop; verify each complete journey, including previews, downloads and fresh-chat retrieval |
| Select the first default library | Planned · not released | Review material from the dev library for the first Schematica default library |
| Personal libraries alongside supplied originals | Deferred from the immediate prototype | Later sign-in, account-linked preferences/designs and separate personal variants; admin privileges for supplied originals |
| Schematic styles and examples in the library | Future · deferred | Browse styles and visible references with captions, including mixed circuits/plots/equations; compare symbols in circuits and test style generalization on realistic examples |
| Create and revisit complete schematics | Future · deferred | Turn text, paper-sketch photos, tablet exports and PDFs into circuits or system diagrams; reuse/create symbols, refine connections and layout, then revisit saved work; general CircuitikZ import/round-trip comes later |

Library expansion is underway; individual creation and search are separate
workstreams that may be developed alongside it after their own scope is authorized.
The remaining interview must settle retrieval behavior (including single matches),
save/version semantics, concrete host acceptance tests and the next delivery order.
The latest decision defers accounts until after the dev-library prototype.
The current authorization covers resistor corrections, declared options, Variations, batch checks and publication; it does not authorize the future milestones.

## Decisions that guide the work

- **Creation starts through agent integrations.** A creation skill and interactive
  workflow are explicit goals. In-app agentic creation can follow later.
- **Automate library growth in bounded batches.** Establish an inventory first,
  generate and check every configuration, correct failures, and ask for human
  verification. Automatic checks do not confer human approval.
- **Dev library first, personal libraries later.** The 14-11-2026 00:22 +01:00
  decision supersedes personal-library-first prototype wording. Future personal
  variants must preserve supplied originals; accounts/storage/admin design remains open.
- **Interpret before creating.** Confirm meaning and uncertain elements, use visual
  annotations where useful, request a short description when missing, then render
  and refine. Offer two meaningful alternatives and save only when requested.
- **Reuse the viewer where practical.** Shared prewritten search UI is proposed;
  host support and the exact selection/download contract still need testing.
- **The website has a broader future than exporting symbols.** Keep export small;
  support browsing, comparison and reuse without filling the interface with setup
  text or technical details. Descriptions and keywords remain read-only for now.
- **Batch creation and interactive creation are separate workflows** built on
  shared TeX drawing tools, semantic definitions and validation rules.
- **Beautiful drawings come first.** The current resistor run does not implement
  sketch/PDF interpretation, simulation, automatic routing or component sourcing.
  Sketch interpretation is an explicit future priority, not a rejected goal.
- **Test usefulness for newcomers.** Use realistic tasks, with/without-Schematica
  comparisons and clean setup tests; an established developer environment alone
  does not demonstrate the intended first-use experience.

The [MCP transition review](https://github.com/DinoDubroja/schematica/blob/docs/mcp-transition-review/context/MCP_TRANSITION_REVIEW.md)
records earlier integration discussion. Its proposed host-first sequence,
ground-symbol prototype, legacy-gallery migration and wire-relative defaults are
not current implementation instructions. The accepted geometry and later product
decisions take precedence.

## Current limits

| Area | What remains |
|---|---|
| Human verification | All 26 current designs are Verified; new or changed designs require explicit human acceptance |
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
