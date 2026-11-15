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
| `GET /api/review/revisions/{uuid}` | Exact source, metadata, configurations and readiness evidence |
| `GET /review/assets/{sha256}` | Private immutable drawing or comparison proof |
| `POST /api/review/assets` | Stage validated SVG `{hash, body}`; never makes it public |
| `POST /api/review/actions/upload` | Finalize a complete `{revision}` after every asset exists |
| `POST /api/review/actions/{action}` | Browser decisions or authenticated desktop job transitions |
| `GET /api/review/evidence?after={sequence}` | Append-only event pages, including original comments and edits |
| `GET /api/review/backup?table={name}&after={cursor}` | Desktop-only complete storage export in bounded pages |

Browser actions: `cursor`, `comment`, `verify`, `unverify`, `discard`, `restore`,
`process`, `approve`, `reject`, `retry`. Desktop actions: `heartbeat`, `claim`,
`renew`, `proposal`, `publication`, `published`, `fail`, `complete`, `upload`.
The executable request examples are in [hosted checks](../tests/verify_review_hosted.py).

Source/evidence export is independent of Git checkout state:

```powershell
python app\review_client.py --config C:\private\desktop.json source REVISION-UUID C:\exports\revision
```

It exports source, helpers, exact SVGs, fingerprints and the private event chain.
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
wrangler deploy --config app\wrangler.jsonc --env validation
# After the isolated checks pass:
wrangler deploy --config app\wrangler.jsonc
```

Initial migration reuses the exact accepted artwork and existing approval evidence.
It requires temporary `MIGRATION_ENABLED=true`, the desktop token and the `migrate`
client command. Close that switch afterward. Imported historical comments are
explicitly unknown; no earlier review story is fabricated. Removed designs stay absent.

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
python tests\check_docs.py
python tests\verify_review_hosted.py --config C:\private\validation.json --output C:\private\validation-checks
```

The hosted check refuses production URLs. It checks independent sessions, edits,
shared targets, revision selection, discard/restore, stale proposals, job exclusion,
authentication, exact exports and retained evidence. It expects the two isolated
ground fixtures and a real completed subscription correction. Reuse unchanged
rendering evidence for comments and decisions; no full-library render is required.

Targeted browser checks additionally cover phone/desktop layout, failed-save draft
retention, noninterrupting arrivals, History comparison and existing Library controls.
Record actual hosted checks separately from state-machine simulations and physical
phone/laptop testing. [Current delivery status](../context/CURRENT.md) names the tested
build, deployment and remaining limits.
