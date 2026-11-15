# Review

[Open Review](https://schematica-preview.dinodubroja.workers.dev/review)
· [Library](https://schematica-preview.dinodubroja.workers.dev/)
· [Desktop and developer setup](REVIEW_SETUP.md)

Review is the private workspace for filling the library. One password works on
your phone and both Windows devices. Comments and decisions are saved online;
the desktop only needs to be running when processing corrections or publication.

![Review on desktop](images/review-desktop.png)

[Phone view](images/review-phone.png). Screenshots use isolated validation fixtures;
they are not additions to the production library.

## Use it

| Action | Expected result |
|---|---|
| Open Review and enter the password | Your browser remembers the session for 30 days |
| Choose a candidate; open **Variations** | Size, Stroke and applicable options appear in separate comparison rows |
| Open **History** | Saved drawings remain available; compare them or select an older revision |
| **Verify** | That exact drawing and its supported configurations are selected; nothing publishes yet |
| Write a comment; **Save comment** | **Saved** confirms it reached the server and is available on your other device |
| **Select** candidates, then comment on selected | The dialog lists exact targets; verified symbols are excluded unless you include them |
| **Discard**, then **Undo** or **Discarded → Restore** | The candidate is recoverable; its published predecessor stays in Library |
| **Process Review** | Verified revisions publish; actionable comments become correction proposals |
| Read the proposal; **Approve changes** | The desktop makes only those corrections and uploads them for fresh review |

The desktop can be off while you browse, comment, verify or discard. Processing
waits for it. **Progress** shows Waiting for desktop, Working, Waiting for approval,
Ready to review or Failed. New arrivals keep your current drawing and unfinished text.

If a save fails, the text stays on that browser. Reconnect and press Save again.
A stale proposal means its source drawing or relevant feedback changed; close it
and process the current review. A changed drawing always needs fresh verification.

## Quick check on both devices

1. Open the same Review link and sign in. The production queue may be empty until
   an agent submits a candidate; the existing accepted library is already published.
2. Save feedback on one device → reload Review on the other → the same feedback appears.
3. Open Variations and History → drawing changes are visible without losing your place.
4. Discard a candidate and restore it → Library still shows its published version.
5. Process Review with the desktop off → it waits; start the desktop connector → progress resumes.
6. Approve a correction → a new **unverified** revision arrives; the old published drawing remains.

Ordinary Library has search, dark/light mode, Variations and SVG exports. It does
not contain verification controls, private comments or unpublished candidates.
Phone layout is checked in a browser at phone dimensions; testing on your physical
phone and second Windows device remains your final check.

## What is preserved

Each revision keeps its source, all rendered configurations, parent, fingerprint
and rendering/reference versions. Comments retain their original text and targets
when edited. Proposals, approval decisions, exact source differences and publication
checks are linked in the private history. Discarding or publishing does not erase it.

Visual readiness checks are agent evidence, not your acceptance. Review never
automatically turns feedback or verification into design rules.
