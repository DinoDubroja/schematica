# Current status

16-11-2026 · **Review usability deployed and verified.**

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

Validation: all 91 Python tests, 39 JavaScript tests, 32 hosted browser interaction
checks and 14 Updates/history checks. The deployed grid passed 324 configuration/layout cases,
24 real browser zoom checks and four continuous resizes, with no alignment defects.
Two actual subscription-backed corrections returned 18 configurations each,
Unverified; one independent ambiguous fixture asked a focused question. The agent
identified the number visible only in the attached image. Its private receipt retains
the observation. Synthetic tests made no production writes or test publications.
The additive image schema preserves existing rows and supports old backup formats.

Product [`5e383c5`](https://github.com/DinoDubroja/schematica/commit/5e383c59df9d73093d4db811fea0aaadaeb79ba5)
is verified on GitHub `main` and `feat/review-usability`; A integrated and B deployed.
Live build **`2c54ba517f0c`**, Worker **`ef3d3cce-415f-4d14-8cb3-816347e7f1bc`**.
Five hosted UI hashes match the tested source. The connector restarted successfully,
reports Ready with protocol 2 and has no queued work. No real feedback was processed.
Older browsers preserve saved images when editing text without an attachments field;
this compatibility guard also passed an actual hosted validation request.

Fresh readback preserves all 175 symbol entries, two comments, three completed jobs,
cursor and exact choices. Database comparison preserves all 178 revision rows,
3,701 artwork rows and 1,585 earlier events/requests byte for byte. SQLite integrity
passes; the only schema additions are private image storage and a history lookup index.
This is preservation evidence, not a live disaster-recovery exercise.

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

Earlier delivery receipts remain in Git history and the
[original Review decision](DECISIONS.md#hosted-review-implementation).
Synthetic decisions belong only to validation, never human acceptance of production artwork.

## Desktop operation

The implementation runs from the isolated `Local/review-implementation` checkout.
This desktop's `Local/review-desktop` folder has **Start Review**, **Stop Review**
and **Status Review** shortcuts. Start it again after Windows restarts. The one-time
password is in the private local `Review access.txt`; it is not in Git. Other devices
need only the Review link and password, never the desktop token.

The canonical checkout and A's active runtime/store, saved band-pass symbol, unsaved
ADC draft, port 8793 and unrelated `docs/research` remain untouched.

## Remaining checks and limits

Physical phone and second Windows device testing remain user checks. Use the short
[action → expected result checklist](../DEVELOPMENT.md#test-on-both-windows-devices)
with Batch 03 candidates. Processing needs this desktop online; reviewing
and saving feedback do not.

At 200% browser zoom in a 390-pixel window (195 CSS pixels), the existing narrow
layout can scroll horizontally; grid/terminal alignment remains correct. Normal
390-pixel phone layout passed without horizontal overflow. HEIC/GIF must be converted
to PNG/JPEG/WebP; four images per comment, up to 10 MB input and 1 MB stored each.

A's separate host limitations remain: Claude embedded download/creation retests,
fresh-chat retrieval, general text-font export and refinement terminal movement.
See [host evidence](../docs/HOST_VERIFICATION.md). No A test symbols were promoted.
