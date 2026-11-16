# Review

[Open Review](https://schematica-preview.dinodubroja.workers.dev/review)
· [Library](https://schematica-preview.dinodubroja.workers.dev/)
· [Desktop and developer setup](REVIEW_SETUP.md)

Review is the private workspace for filling the library. One password works on
your phone and both Windows devices. Comments, images and decisions are saved online;
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
| **Verify & next** | Saves that exact revision, then opens the next candidate needing review; nothing publishes yet |
| Write feedback; **Save comment & next** | Saves the complete comment and images, then advances; **Save comment** stays here |
| **Select** candidates, then comment on selected | The dialog lists exact targets; verified symbols are excluded unless you include them |
| **Discard**, then **Undo** or **Discarded → Restore** | The candidate is recoverable; its published predecessor stays in Library |
| **Process Review** | Explicitly verified revisions publish; the desktop applies submitted feedback and returns new **Unverified** drawings |
| **Updates → Open drawing / Answer** | Opens the exact correction or an essential question; opening alone never verifies it |

The desktop can be off while you browse, comment, verify or discard. Processing
waits for it. **Updates** groups Ready to review, Working / queued, and Needs your
answer / failed. Its badge counts revised symbols still needing review. Seen updates
remain until you review them. Arrivals preserve your drawing, draft and scroll position.

On a phone, **Previous · Comment · Verify & next** stays at the bottom. The bar moves
out of the way while typing. **Undo** remains beside the inline Saved/Verified state;
Description remembers whether you left it open. A completed queue is labelled clearly.

## Image feedback

Use **Add images** or **Take photo** on a phone; paste or drop an image into desktop
feedback. Remove a thumbnail before saving; tap a saved image to enlarge it.
Up to four PNG, JPEG or WebP images, each up to 10 MB before resizing. Photos are
resized to at most 1600 pixels and 1 MB for storage. Convert HEIC/GIF first.

**Saved** appears only after every image and the comment reach the server. Failed
uploads keep text, images and the exact target on that browser, including after
reload. Reconnect and retry. Unsaved drafts are local; saved feedback is available
on your other devices. Images remain private and linked to the exact revision;
History retains earlier comment edits, including removed images.

Process Review authorizes corrections directly. A genuine ambiguity produces a
focused question while other symbols continue. Stale feedback/source cannot be
overwritten: close the stale job and process the current review. Old unapproved
proposals remain in history and do not start automatically. A changed drawing
always needs fresh verification; individual creation in chat keeps its own confirmation.

## Quick check on both devices

1. Review several candidates on your phone → Verify & next keeps the drawing visible;
   Undo restores the previous decision without a success popup to dismiss.
2. Save an image comment → open Review on the other device → text and enlarged image match.
3. Open History, then Discard and Undo → earlier drawings/comments remain and the candidate returns.
4. When ready to apply your feedback, Process Review → corrections run without a plan gate;
   the status clearly waits if the desktop is offline.
5. Open Updates after a correction → its exact new **Unverified** revision opens;
   seen status persists, and the published drawing stays unchanged until you verify and process it.

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
