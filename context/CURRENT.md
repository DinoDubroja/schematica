# Current status

13-11-2026 · **Resistor batch and verification implemented and preview published.**

The user authorized this batch, compact viewer review controls, tests/docs,
commit/push and deployment to the existing Cloudflare preview. Implementation,
documentation and checks are complete. The [live preview](https://schematica-preview.dinodubroja.workers.dev/)
and [fixed version](https://6b23fd83-schematica-preview.dinodubroja.workers.dev/)
serve the tested build. The next step is human review, not another creation batch.

## What exists

- **28 designs / 252 configurations:** the six accepted originals plus 22 new
  resistor variants. [Inventory and reference mapping](../docs/RESISTOR_BATCH.md).
- Minimal library viewer with dark/light mode, search, family/batch filters,
  Unverified tab, design checkboxes, Verify & next, Undo, 3 × 3 comparison and
  stable symbol references. Single SVG and complete-library exports remain small.
- Separate official verification and browser-local pending selections. The
  [handoff guide](../docs/VERIFICATION.md) explains exact revision/fingerprint
  validation and publication. Only the six original designs are officially Verified.
- TeX drawing authority, YAML semantics, candidate-render/check/promote workflow,
  generated packaging, developer and Inkscape guides. Legacy material remains
  archived outside this checkout and supplies no automatic instructions.

## Verification results

**Build c7b750381988**, 270 static files. 34 Python and 4 JavaScript tests pass.
All 252 configurations render and pass Inkscape bounds/parts checks; all 54 original
SVGs are byte-identical. The 42 palette comparisons pass (maximum 0.001234 mm deviation).
All nine actual browser library downloads match and survive Inkscape save/reopen.
GUI Symbols shows 28 thumbnails; pasted/unlinked/saved/reopened US potentiometer
retains its five named editable parts. Native CircuitikZ and new resistor PDF compile.

The temporary approval loop, clipboard fallback, stale/unknown rejection,
idempotent application, local persistence/Undo and preservation/invalidation rules
were tested separately. No test approvals entered the real record. All designs
were visually inspected in the comparison view; US wiper/tap crowding was corrected.
Search, filters, themes, keyboard, downloads, reference links and 360 px layout pass.
The hosted manifest and all 268 served assets match locally. Actual hosted single/
library downloads match; live search, pending reload/Undo, themes, comparison and
references pass with no browser errors. Launch on port 8792 and its HTTP build check
pass; Windows rejected 8766, and launcher failures now return an error. Repository-only
recovery independently found the objective, authorization, checks and next review.

## Next review and limits

The user reviews **22 Unverified designs** and pastes approvals
or corrections into chat. Repeat the [developer checklist](../DEVELOPMENT.md#test-and-review)
on the laptop. Desktop checks do not establish results on the second device.
Profile-wide Inkscape Symbols installation, fresh GUI grid snapping, and clean-machine/
offline TeX setup remain unverified.

Accounts, admin privileges, personal variants, MCP and an agent-integrated creation
skill remain future work. Batch and interactive creation share tools/formats/checks,
but remain separate workflows. The broader milestone interview/order is unfinished;
see [roadmap](../docs/ROADMAP.md) and [decisions](DECISIONS.md). No expansion beyond
the current batch is authorized by those future wishes.
