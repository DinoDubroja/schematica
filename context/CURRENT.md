# Current status

16-11-2026 · **Review usability implemented and validated; delivery in progress.**

[Library](https://schematica-preview.dinodubroja.workers.dev/)
· [Private Review](https://schematica-preview.dinodubroja.workers.dev/review)
· [Using Review and five checks](../docs/REVIEW.md)
· [Setup, API and recovery](../docs/REVIEW_SETUP.md)

## Current work

Verify & next and separate comment/save-and-next actions keep the drawing in view.
Phone actions stay at the bottom and clear the keyboard. Saved/Verified feedback
is inline; Description remembers its state. Private image comments support photo/
file selection, paste/drop, retained drafts, earlier edits and cross-device viewing.

Process Review directly authorizes new per-symbol corrections. The connector reads
actual attached images, returns a new Unverified revision and asks only essential
questions; independent jobs continue. Updates groups returned drawings, queued work
and questions/failures. Seen status is persistent and separate from verification.
Old unapproved proposals remain inert. Individual creation in chat is unchanged.

Validation: all 91 Python tests, 39 JavaScript tests, 143 documentation links,
32 browser interaction
checks and 14 Updates/history checks. The grid passed 324 configuration/layout cases,
24 real browser zoom checks and four continuous resizes, with no alignment defects.
Two actual subscription-backed corrections returned 18 configurations each,
Unverified; one independent ambiguous fixture asked a focused question. The agent
identified the number visible only in the attached image. Its private receipt retains
the observation. Synthetic tests made no production writes or test publications.
The additive image schema preserves existing rows and supports old backup formats.

Delivery remains in progress on `feat/review-usability`; A integrates exact READY
commits and B alone deploys. Production remains on the earlier grid build until the
final deployment receipt replaces this paragraph. Its desktop connector is stopped
for the upgrade. No real pending feedback is used for validation.

## Library and batch status

**84 Batch 03 candidates / 792 configurations** remain available for human review.
[Batch checklist](../docs/BATCH_03.md) · [source inventory](../app/batches/batch-03/manifest.json)
· [validation receipt](../app/batches/batch-03/validation.json).
The hosted Library already had **98 designs / 1,098 configurations** at this task's
start: seven Batch 03 designs had been explicitly published through Review. All
1,098 hosted SVGs and 36 exports match that snapshot. The repository's bundled
catalog remains 91 designs / 1,035 configurations. No symbol geometry, approval
or public Library addition is part of this usability delivery.

The previous [grid alignment fix](../docs/REVIEW_GRID.md) uses shared Library/Review
coordinates for the 1 mm grid, artwork and blue terminals; its behavior is preserved.
Batch 03 source checkpoint `2bff9bf` and grid product `e55e7d4` are already on main.
The saved PNP correction predates Batch 03 and remains its enclosed PNP's parent.

## Original Review service delivery receipt

| Receipt | Result |
|---|---|
| Product source | `72d128797d765e64dbfe999e3de200646e22cc4d` |
| Build | `826fc3ddf903` |
| Production Worker version | `a05fe7ce-32ca-427e-9ce1-6f9dbe433bf8` |
| GitHub delivery | `feat/review` and `main`; this receipt accompanies the final documentation commit |
| Production migration | 91 exact historical fingerprints; 2,070 private artwork/fragment assets; migration switch closed |
| Source checks | 81 Python and 26 JavaScript tests passed; documentation links checked |
| Hosted file checks | 1,079 public file hashes matched, including every accepted drawing and library export |
| Desktop | ChatGPT subscription authenticated; Check, Start, repeat Start, Stop and restart passed |

## Workflow evidence

- Nine hosted validation groups passed with independent authenticated sessions:
  comments/edits/shared targets, exact revision selection, discard/restore, stale
  proposals, duplicate requests/uploads, access protection, exports and evidence.
- A real subscription-backed correction changed one synthetic ground bar, rendered
  all 18 supported configurations, passed visual readiness and returned unverified.
  The separately approved test revision then published exactly; every returned
  public SVG matched. Original feedback, drawings, source diff and decisions remain.
- Thirteen browser interaction checks passed, including failed-save/reload draft
  retention, History comparison, Undo and independent phone-size sessions.
  A live arrival preserved the selected drawing and unfinished comment.
- An abandoned hosted job lease expired and was reclaimed once, with a new lease
  and incremented attempt count. Local connector stop/restart also passed.
- Production login and Library search, Small/Thick, light mode, Variations and both
  real browser downloads passed. Downloads matched the accepted files byte for byte.
- Validation backup restored into fresh local SQLite: all rows and 2,179 asset
  hashes matched. Production backup is consistent and checksummed: 91 revisions,
  2,070 assets. This is not a live Cloudflare disaster-recovery exercise.

All synthetic decisions belong to the separate validation database. They are not
human acceptance of production artwork. Review does not turn comments into rules.

## Desktop operation

The implementation runs from the isolated `Local/review-implementation` checkout.
This desktop's `Local/review-desktop` folder has **Start Review**, **Stop Review**
and **Status Review** shortcuts. Start it again after Windows restarts. The one-time
password is in the private local `Review access.txt`; it is not in Git. Other devices
need only the Review link and password, never the desktop token.

Agent B integrated A's exact ready `5efa3a8` under the delegated publication scope.
The canonical checkout and A's active runtime/store, saved band-pass symbol, unsaved
ADC draft, port 8793 and unrelated `docs/research` remain untouched.

## Remaining checks and limits

Physical phone and second Windows device testing remain user checks. Use the short
[action → expected result checklist](../DEVELOPMENT.md#test-on-both-windows-devices)
with Batch 03 candidates. Processing needs this desktop online; reviewing
and saving feedback do not.

A's separate host limitations remain: Claude embedded download/creation retests,
fresh-chat retrieval, general text-font export and refinement terminal movement.
See [host evidence](../docs/HOST_VERIFICATION.md). No A test symbols were promoted.
