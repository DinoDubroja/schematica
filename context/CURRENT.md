# Current status

14-11-2026 · **A integration milestone implemented locally; combined checks passed; host checks pending.**

## Ownership and authorization

This is Agent A's `work/agent-a-integration`, isolated from B's symbol checkout.
A started at `477f679`, adopted B's ready documentation checkpoint `89dbd3e`,
and has integrated exact READY capacitor `51a101c` and diode `9c70fc6` checkpoints. Machine-specific
paths, ports, data and ready commits are in `Local/parallel-work/agent-a.md`.
B owns its own handoff and checkout. See [parallel work](../DEVELOPMENT.md#parallel-work).

A's integration milestone authorized local setup, implementation, tests, checkpoint
commits and integration of exact ready B work. Its unpublished product ancestry
has no push/deployment authorization; the guidance adoption below adds no such grant.
B's separate [batch-02 request](../docs/BATCH_02.md) authorizes its finite 80-design
batch, family commits, pushing B's branch and publishing its tested library.
B remains sole shared-preview publisher. Never treat its moving branch tip as ready.
The collection is the dev library; accounts and personal libraries remain deferred.

## Delivery workflow adoption

14-11-2026: the [delivery checklist](../DEVELOPMENT.md#delivery-checklist) is adopted
in A, B and main; every AGENTS.md reaches the same six-item checklist. Agent A
coordinates integration. Installer simplification and user-guide rewrites remain
separate work. This delivery merges no product features and deploys no app.

- **Main and documentation branch published:**
  [`131d705`](https://github.com/DinoDubroja/schematica/commit/131d705f0ea0fa19db7fb2e10dda43dacdf18367)
  on `main` and `docs/delivery-workflow`; five documentation files only. The main
  README links setup, testing, preview, progress and the checklist, and separates
  main's older source snapshot from B's published preview and A's unfinished work.
- **B adopted and published:**
  [`ddbd03f`](https://github.com/DinoDubroja/schematica/commit/ddbd03f0b5350019eb3ff3c8609268b7bc105780),
  after its final approvals completed at `2fedf44`. Four guidance files only;
  B's product work, approvals, own handoff and unrelated research were preserved.
  B can acknowledge this adoption in its own handoff at its next session.
- **A adopted locally:** original guidance-only commit `b722d22`, plus status
  receipts. A's product branch remains unpublished: pushing it would publish
  earlier product ancestry outside that task's local-only authorization. The
  guidance was published independently from main without including that ancestry.

GitHub remote heads, changed-file scope and published document targets were read
back successfully. Local link checks: A 109, B 96, main 86; identical checklist and
all AGENTS routes pass. The independent recovery audit passed for the shared
workflow. The preview link check returned HTTP 403 here; this delivery performed
no installation, actual first-use or embedded-host verification. Earlier local-only
publication holds and pending B-adoption notes are superseded by this receipt.

## Delivered locally

- Natural-language search and follow-ups; exact identity/revision/configuration/SVG
  selection. One prewritten shared website/MCP Apps viewer, including one/zero
  matches, active filters, Browse all and accepted Variations controls.
- Separate creation skill: short text plus accessible images, explain/confirm/wait,
  authoritative TeX, all combinations checked, preview/two alternatives, request-only
  save. Isolated drafts and recoverable dev-library revisions; saves stay Unverified.
- Combined checks: 61 Python + 11 JavaScript tests; real proofs covering 108 TeX
  configurations across creation, refinement, transport, added options and B recipe reuse.
  stdio/HTTP and focused browser behavior pass; embedded-host journeys are pending.
- [Setup/use](../docs/AGENT_INTEGRATION.md), [creation contract](../docs/INDIVIDUAL_CREATION.md),
  [platform evidence and exact user checks](../docs/HOST_VERIFICATION.md).

## Integrated symbols and review

B's integrated checkpoints have **38 designs / 504 configurations**, including the
original 26 Verified designs and 12 new Unverified designs. B reports all original
342 SVG bytes and 26 approval records preserved, with 47 Python/eight JS checks,
full-family Inkscape bounds/vector/save-reopen checks and visual inspection.
A independently confirmed the same preservation, regenerated build `2bb74f98e29b`
(551 files) and passed combined checks. Tests do not confer human artwork approval.
Nonlinear B revision 3 and removed tapped/varistor designs remain unchanged.

B's diode checkpoint build was `7342b5918472`; its shared preview was still on the prior
`fae9ed42be9d` release at that handoff. This is historical evidence, not an A live-site
verification. The remaining batch families continue independently in B.

Next: run host-specific checks
after MCP reload/approved cloud connectivity. The independent repository recovery
audit identified stale overview counts/links, now corrected.
The lighter recurring Inkscape policy and two-device interaction checks remain open.

[Decision history](DECISIONS.md) · [Broad roadmap](../docs/ROADMAP.md)
· [Symbol review](../DEVELOPMENT.md#test-on-both-windows-devices)
