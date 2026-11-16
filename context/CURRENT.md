# Current status

16-11-2026 · **Review workflow delivered on GitHub main and the shared preview.**

[Library](https://schematica-preview.dinodubroja.workers.dev/)
· [Private Review](https://schematica-preview.dinodubroja.workers.dev/review)
· [Using Review and five checks](../docs/REVIEW.md)
· [Setup, API and recovery](../docs/REVIEW_SETUP.md)

## Latest delivery

Review has two adjustable panes, latest-revision thumbnails, forgiving name/alias
search and selection that survives filters. One editor names exact targets and
retains text/images/scopes across navigation, resizing, reload and failed saves.
Verified symbols remain searchable. Filtered Verify & next does not skip a row when
the saved row disappears. History labels real events and compares at one scale.

**Process Review → read-only summary → Confirm & process.** Corrections and verified
publication choices are separate, with run-local exclusions. A changed snapshot
requires refreshed confirmation. Each comment target has an independent result;
extending a completed comment or retrying failure does not repeat successful work.
New drawings stay Unverified. Existing publication/approval history is unchanged.
[Decision and original source](DECISIONS.md#review-layout-shared-feedback-and-exact-processing-summary).

Validation: **92 Python / 49 JavaScript tests**, **42 hosted browser journeys**,
**7 hosted simulator checks**, plus five focused final screenshot/scope/image checks.
The shared grid passed **324 configuration/layout cases, 24 browser zoom checks and
four resizes**, with no endpoint defects (maximum screen error under 0.002 pixels).
Phone editor and image previews were inspected visually; a duplicated public/private
security policy that blocked local image thumbnails was corrected and regression-tested.
No real feedback was executed and no test symbols were published.

Product [`4106535`](https://github.com/DinoDubroja/schematica/commit/4106535b1e9b07c58319ab3bf8bff2934a013ff7)
is on GitHub `main` and `feat/review-workflow`; A independently integrated and checked
all 92 Python / 49 JavaScript tests and 150 documentation links. B deployed the exact
source: live build **a50ad9162e3a**, Worker **36e2b117-a35c-4369-a2fa-05492ed4a893**.
Six hosted UI/coordinate hashes match. Live desktop/phone, alias highlighting and
read-only processing-summary checks passed with zero production writes/jobs.
The connector restarted from the owner checkout and reports **Ready**, protocol 2,
with no queued or working jobs. No real feedback was processed during delivery.
Git history, ignored evidence and a complete D1 snapshot were backed up and verified
under `Archive/review-workflow-20261116-1533`; private receipts remain outside Git.
The earlier subscription/image-processing evidence remains in Git history; this
interface update uses isolated simulated returns without running the real agent.

## Library and preservation

The live baseline is **175 symbol entries, three comments, three completed jobs**,
with **98 published designs / 1,098 configurations / 36 exports**. The bundled
catalog remains **91 designs / 1,035 configurations**. No symbol geometry, source,
approval or public Library addition is part of this update. Fresh hosted readback
preserves all 175 entries, three comments, three completed jobs and cursor exactly;
all 1,134 public SVG/export hashes match the starting snapshot. Post-deploy SQL
comparison preserves 178 revisions, 3,701 artwork rows, all 1,797 earlier events and
requests, and the publication catalog byte for byte; SQLite integrity passes.
No schema migration occurred. The 21 owned validation fixtures are discarded with
their history retained; unrelated validation symbols remain unchanged.

**84 Batch 03 candidates / 792 configurations** remain available for human review.
[Batch checklist](../docs/BATCH_03.md) · [source inventory](../app/batches/batch-03/manifest.json)
· [validation receipt](../app/batches/batch-03/validation.json).
The [shared 1 mm grid](../docs/REVIEW_GRID.md) is preserved. Earlier delivery receipts
remain in Git history. Synthetic decisions are never human acceptance of production artwork.

## Desktop and remaining checks

Processing runs from the isolated `Local/review-implementation` checkout. This desktop's
`Local/review-desktop` folder has **Start Review**, **Stop Review** and **Status Review**
shortcuts. Start again after Windows restarts. Other devices need the Review link
and password, never the desktop token. Unsaved drafts remain in their original browser.

Physical phone keyboard/camera and second Windows-device testing remain user checks.
Use the [five-step checklist](../docs/REVIEW.md#quick-check-on-both-devices). A 390-pixel
phone viewport has no horizontal overflow. An extreme 195-CSS-pixel window at 200%
zoom can still overflow; grid alignment stays correct. HEIC/GIF require conversion.

The canonical checkout and A's runtime/store, saved band-pass symbol, unsaved ADC
draft, port 8793 and unrelated research remain untouched. A's separate host limits
remain in [host evidence](../docs/HOST_VERIFICATION.md); no A test symbols were promoted.
