# Current status

16-11-2026 · **Schematica Review is deployed and the desktop connector is running.**

[Library](https://schematica-preview.dinodubroja.workers.dev/)
· [Private Review](https://schematica-preview.dinodubroja.workers.dev/review)
· [Using Review](../docs/REVIEW.md)
· [Setup, API and recovery](../docs/REVIEW_SETUP.md)

## Current work

The authorized Review delivery is complete. It adds persistent private feedback,
exact-revision decisions, Variations, History, recoverable discard, explicit proposal
approval, subscription-authenticated desktop correction jobs and atomic publication.
The public Library retains its presentation and exports; verification lives in Review.

**91 published / 91 Verified / 0 Unverified**, with all **1,035 configurations** and
36 library exports preserved. Production has no test candidates. Its Review queue is
empty until an agent submits a real candidate; accepted symbols are already published.

## Tested delivery

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
once a real candidate is submitted. Processing needs this desktop online; reviewing
and saving feedback do not.

A's separate host limitations remain: Claude embedded download/creation retests,
fresh-chat retrieval, general text-font export and refinement terminal movement.
See [host evidence](../docs/HOST_VERIFICATION.md). No A test symbols were promoted.
