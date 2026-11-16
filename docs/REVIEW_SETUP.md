# Review setup and development

[Using Review](REVIEW.md) · [Developer guide](../DEVELOPMENT.md)

## Desktop connector

Only the processing desktop needs Python, the existing TeX tools, Inkscape's
command-line renderer and Codex signed in with ChatGPT. Browsing devices need a browser.
The connector removes API-key environment variables for Codex and requires a
ChatGPT login. Shell, browser, computer control and subagents are disabled in its
bounded Codex calls; it receives structured results rather than modifying the checkout.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements-dev.txt
codex login status
.\app\review-desktop.ps1 -Action Check -Config C:\path\outside-repo\desktop.json
.\app\review-desktop.ps1 -Action Start -Config C:\path\outside-repo\desktop.json
.\app\review-desktop.ps1 -Action Status -Config C:\path\outside-repo\desktop.json
.\app\review-desktop.ps1 -Action Stop -Config C:\path\outside-repo\desktop.json
```

Stop preserves the current bounded operation before exiting. Start is safe to
repeat. It runs in the background until stopped or Windows exits; start it again
after restarting Windows. Subscription limits/authentication pause processing;
resolve the issue in Codex, restart the connector and choose Retry in Review.
Connectivity failures reconnect automatically. Jobs and local rendering results
survive restart; leases and immutable IDs prevent duplicate execution/publication.

The private configuration contains `url`, `token`, `work`, `python`, `codex` and,
where not on PATH, `tectonic`, `dvisvgm` and `inkscape` executable paths. Keep it
outside Git with permissions restricted to your Windows account. Never send its
desktop token to a reviewing device. The reviewing device only needs the password.

## Where to edit

```text
app/
├── review/                 # private web application
│   ├── domain.mjs          # decisions, job leases and exact revision transitions
│   ├── worker.mjs          # authentication, D1 transactions and publication
│   ├── schema.sql          # persistent storage
│   ├── images.mjs          # private raster validation
│   ├── review-tools.js     # navigation, updates and local image drafts
│   ├── review-workflow.js  # candidate search, target editor and processing summary
│   ├── index.html
│   ├── review.css          # approved responsive layout
│   └── review-app.js       # browser interactions and retained drafts
├── review_client.py        # submission, source export and recovery packages
├── review_desktop.py       # bounded Codex processing and rendering
└── review-desktop.ps1      # start / stop / status
```

The existing renderer, exports and host integration remain separate. New candidate
assets live in D1, not the public static directory. A transactional publication
switch updates the complete public catalog; individual and whole-library exports
then use that revision. Publishing a symbol does not deploy application code.

## Submit one finished candidate

Use an isolated output directory and the current custom TeX definition format.
Compare the finished rendering against the construction reference and accepted
relatives before supplying the visual note. The note describes checks, not approval.

```powershell
python app\review_client.py --config C:\private\desktop.json prepare `
  --definition C:\batch\symbol.yaml --recipe C:\batch\symbol.tex `
  --output C:\batch\rendered-symbol --batch "Batch name" `
  --visual-note "Compared Small/Thick and related symbols; no clipping or discontinuities."
python app\review_client.py --config C:\private\desktop.json upload C:\batch\rendered-symbol\package
```

For a correction, add `--parent` with the current saved revision UUID and increment
the definition revision. Every declared size/stroke/option combination must render.
Upload each finished symbol immediately. Repeating an upload recovers the same
immutable revision. Existing rendered catalogs can use `package_symbol` without
re-rendering; the caller supplies exact source and visual evidence.

## Private API

Desktop requests use `Authorization: Bearer …`. Browser requests use an HttpOnly,
Secure, SameSite session cookie and same-origin writes. All action POSTs require a
unique `Idempotency-Key`, retained when retrying the same request. A key cannot be
reused with different content. Concurrent state changes return 409 and are retried
without overwriting another device's work.

| Endpoint | Purpose |
|---|---|
| `GET /api/review/state` | Candidates, decisions, comments, cursor and processing status |
| `GET /api/review/candidate-previews` | Compact latest-revision thumbnail/name/alias index; artwork loads lazily |
| `GET /api/review/processing-summary` | Read-only exact correction/publication snapshot; creates no jobs |
| `GET /api/review/timeline/{symbol}` | Actual Created/Revised/Verified/Published events, without inferred dates |
| `GET /api/review/revisions/{uuid}` | Exact source, metadata, configurations and readiness evidence |
| `GET /review/assets/{sha256}` | Private immutable drawing or comparison proof |
| `POST /api/review/images` | Upload private `{hash, mime, body}`; body is base64 PNG/JPEG/WebP, at most 1 MiB decoded |
| `GET /review/images/{sha256}` | Authenticated image bytes; never public/cacheable |
| `GET /api/review/comment-history/{uuid}?after={sequence}` | Earlier text, targets and images for one comment |
| `POST /api/review/assets` | Stage validated SVG `{hash, body}`; never makes it public |
| `POST /api/review/actions/upload` | Finalize a complete `{revision}` after every asset exists |
| `POST /api/review/actions/{action}` | Browser decisions or authenticated desktop job transitions |
| `GET /api/review/evidence?after={sequence}` | Append-only event pages, including original comments and edits |
| `GET /api/review/backup?table={name}&after={cursor}` | Desktop-only complete storage export in bounded pages |

Browser actions: `cursor`, `seen`, `comment`, `comment-extend`, `verify`, `unverify`, `discard`, `restore`,
`process`, `answer`, `reject`, `retry`. Desktop actions: `heartbeat`, `claim`,
`renew`, `question`, `publication`, `published`, `fail`, `complete`, `upload`.
Legacy `proposal`/`approve` actions remain for retained history/previously approved
jobs. New `workflow: 2` jobs record final summary confirmation, one symbol per job.
The desktop claims with `{protocol: 2}`; an older desktop cannot claim new jobs.

`process` requires `{snapshot, included}` from the read-only summary. `included` is
an explicit subset of its card keys. Changed pending work returns 409; show a fresh
summary and require confirmation again. Reuse the same idempotency key and payload
after network uncertainty. An old browser calling `process` without a summary fails
safely and must reload.

`comment-extend` accepts `{comment, expected, targets}` with only the new exact targets.
It preserves saved text/images. Per-target feedback tokens keep completed targets
completed and avoid invalidating an independent working target. State includes
`comment_progress`: `revision` is the original target; `resultRevision` links its
returned drawing. No database migration or geometry change is needed for this update.
Old unapproved proposals cannot be claimed automatically. Answers refresh only the
question's exact target/signature. Changed source or feedback invalidates in-flight work.

Comments accept `attachments: [{hash, mime, bytes, name}]`, up to four uploaded images.
The server checks type, dimensions, size, hash and upload presence. The desktop
retrieves and verifies actual bytes, passes files to Codex's image input, and retains
image observations in its private work receipt. Image URLs alone are insufficient.
See [direct workflow checks](../tests/verify_review_usability.py) and
[retained API checks](../tests/verify_review_hosted.py).

Source/evidence export is independent of Git checkout state:

```powershell
python app\review_client.py --config C:\private\desktop.json source REVISION-UUID C:\exports\revision
```

It exports source, helpers, exact SVGs, fingerprints, comment images (including
earlier edits) and the private event chain.
The desktop also keeps a source/artwork receipt in its `published/{revision}`
directory after each publication. Rendering hashes and the source repository commit
identify the implementation used. Bring approved source into future repository
deliveries through the normal review/check/commit workflow; the connector never
overwrites another agent's checkout. Do not commit private comments or credentials.

## Storage, deployment and recovery

The existing `schematica-preview` Worker binds the `schematica-review` D1 database.
`schematica-review-validation` uses a separate database and synthetic fixtures.
Both use the existing Cloudflare account and free-tier limits. Exceeding free limits
can stop requests; this setup does not enable paid API usage or paid overages.
See [D1 limits](https://developers.cloudflare.com/d1/platform/limits/) and
[pricing](https://developers.cloudflare.com/d1/platform/pricing/).

Provision D1 with [schema.sql](../app/review/schema.sql). Configure Worker secrets
`DESKTOP_TOKEN_HASH` (SHA-256 of a random desktop token) and `REVIEW_PASSWORD_HASH`
(`salt:hex`, PBKDF2-HMAC-SHA256, 100,000 iterations, salt encoded as UTF-8).
The app configuration contains database IDs, never these secrets. Password changes
also require clearing the `sessions` table to revoke existing sessions.

```powershell
python app\build_site.py
wrangler d1 execute schematica-review-validation --remote --file app\review\schema.sql --config app\wrangler.jsonc --env validation
wrangler deploy --config app\wrangler.jsonc --env validation
# After the isolated checks pass:
wrangler d1 execute schematica-review --remote --file app\review\schema.sql --config app\wrangler.jsonc
wrangler deploy --config app\wrangler.jsonc
```

Initial migration reuses the exact accepted artwork and existing approval evidence.
It requires temporary `MIGRATION_ENABLED=true`, the desktop token and the `migrate`
client command. Close that switch afterward. Imported historical comments are
explicitly unknown; no earlier review story is fabricated. Removed designs stay absent.

The usability upgrade is additive: an `images` table and event lookup index, with
no revision/decision rewrite. Back up first, stop the desktop connector, apply the
schema, deploy and restart the updated connector. Keep migration closed. Backup and
recovery include private image bytes; older image-free backups remain readable.

For a portable backup, stop the connector and avoid review writes during export:

```powershell
python app\review_client.py --config C:\private\desktop.json backup C:\backups\review-YYYYMMDD
python app\review_client.py --config C:\private\desktop.json recovery-sql `
  C:\backups\review-YYYYMMDD C:\backups\review-recovery.sql
```

The checksum manifest must say `consistent: true`. Import the SQL into a **new**
empty D1 database, verify revision/asset/event counts and hashes, then deliberately
change the binding. Keep the old database until recovery is confirmed. Sessions
are not restored; sign in again. For an online snapshot, use `wrangler d1 export
schematica-review --remote --output C:\backups\review.sql`. Cloudflare also provides
seven days of Time Travel on the free plan. Test recovery before depending on it.

## Checks after changes

```powershell
python -m unittest discover -s tests -p "test_*.py"
node --test tests/*.test.cjs tests/*.test.mjs
python tests\check_docs.py --render
```

For an interface change, use the separate validation service with its connector
stopped. Choose a fresh fixture prefix/output folder for each complete run. The
preparer reads published source and writes only isolated, unpublished fixture copies.
It never renders the entire library or changes production decisions.

```powershell
python tests\prepare_review_workflow.py --source-config C:\private\desktop.json --config C:\private\validation.json --output C:\private\workflow-run\fixtures --prefix review-flow-run01-
node tests/review-workflow-browser.cjs --config C:/private/validation.json --fixtures C:/private/workflow-run/fixtures --image C:/private/reference.png --output output/playwright/workflow-run
python tests\verify_review_workflow.py --config C:\private\validation.json --root C:\private\workflow-run --stage prepare
node tests/review-workflow-results-browser.cjs --config C:/private/validation.json --root C:/private/workflow-run --output output/playwright/workflow-run
python tests\verify_review_workflow.py --config C:\private\validation.json --root C:\private\workflow-run --stage finish
```

Run these five steps in order. Browser checks need Playwright and Chrome available
on that device. Supply a non-private PNG/JPEG/WebP reference image. The test simulator
returns unchanged drawings with new fixture revisions, deliberately fails one target,
and checks extension/retry without reapplying successful work. No real agent call or
test publication is needed. Discard only the run's fixtures afterward; retain history.

| Check | Expected result |
|---|---|
| Shared NPN/PNP image comment, failure and reload | Text, image, exact targets and independent scopes survive |
| Search, multiselect, pane drag/keyboard resize, filtered verification | No lost selection, hidden controls or skipped candidates |
| Open/exclude/stale/double-click processing summary | No jobs before final confirmation; exact included snapshot, no duplicates |
| One success, one failure, then extend/retry | Completed targets stay completed; only new/failed targets run |
| History, image edits, comparison, Undo, Discard and arrivals | Evidence stays accessible; current draft/focus/scroll are undisturbed |

For coordinate changes, also run the read-only
[grid/zoom browser checks](../tests/review-grid-browser.cjs); they block every service
write. [Earlier agent/image checks](../tests/verify_review_usability.py) and
[retained API checks](../tests/verify_review_hosted.py) cover the existing subscription
processor and recovery contracts. Rerun those when those components change, not for
every layout edit. The original browser harnesses document prior interface versions.

Inspect the actual screenshots: desktop, phone drawing/editor/drawer and processing
summary. Check that images load and controls remain reachable at zoom. Report browser
viewport checks separately from physical keyboard/camera and second-device testing.
[Current delivery status](../context/CURRENT.md) records the tested build and limits.
