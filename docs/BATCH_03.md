# Batch 03

84 designs for private [Schematica Review](https://schematica-preview.dinodubroja.workers.dev/review).
Select **Batch 03** in Review. These are candidates, awaiting your feedback and verification.
Ordinary Library is unchanged by these submissions.

**Complete: 84 submitted · 792 configurations · 0 deferred · 0 blocked.**
All 84 were Unverified at delivery. Submission does not select or publish a drawing.

| Family | Submitted | Configurations |
|---|---:|---:|
| Data conversion | 6 | 54 |
| Filters | 6 | 90 |
| Signal processing | 8 | 72 |
| Digital building blocks | 10 | 90 |
| RF | 8 | 72 |
| Optoelectronics | 8 | 72 |
| Power semiconductors | 6 | 54 |
| Transducers and basic motors | 6 | 54 |
| Additional transistor styles | 12 | 108 |
| Additional motors | 4 | 36 |
| Generators | 2 | 18 |
| Relays and contactors | 6 | 54 |
| Pushbuttons | 2 | 18 |

- [Completion manifest](../app/batches/batch-03/manifest.json): targets, status, configuration counts and immutable hosted revision IDs.
- [Exact sources](../app/batches/batch-03/symbols/): each candidate's definition and parameterized TeX.
- [Submission runner](../app/batches/batch-03/run.py): isolated rendering and the existing authenticated Review client.
- [Validation receipt](../app/batches/batch-03/validation.json): delivery checks, separated from human verification.

## Review

| Action | Expected result |
|---|---|
| Open Review and choose Batch 03 | 84 candidates, with saved drawings and source. |
| Open a candidate and switch size/stroke | All nine combinations; band-pass and tunable band-pass each have three response widths. |
| Inspect Medium/Medium, then Small/Thick | Clear leads, arrows, labels and electrical distinctions. |
| Open History | Saved source, construction basis and immutable opening revision. |
| Leave a real modification request | Feedback is retained; a correction requires a linked proposal/revision. |
| Open ordinary Library | Existing published symbols remain available. |

Start with the enclosed PNP, JFET pair, simplified MOSFET pair, an optocoupler,
DPDT relay and unipolar stepper. Check arrow direction, clearance, resting contacts
and winding connections. On the second Windows device, open the same Review link:
your saved feedback should appear after reloading. No local checkout is needed.

## Construction and checks

The saved ADC and band-pass drafts retain their original artwork and Unverified status.
Enclosed transistor derivatives preserve accepted internals; PNP uses the settled live revision
`aade4544-ddc3-50f3-b89e-6510eb114858`. Relays and pushbuttons are fresh redraws.
Only the two enclosed explicit-bulk MOSFETs extend their bulk lead/terminal to clear
the circle; other terminals and all internal parts are preserved. This is recorded
in each definition's lineage and requires review as a new design.
Functional blocks describe generic behavior, not manufacturer pinouts or standards certification.
Labels use Latin Modern Sans outlines, matching the ADC draft's approved export approach.

Each submission records its source and an actual visual inspection note. Rendering checks every
configuration, named parts, pins, grid alignment and stroke independence. Hosted readback checks
exact source and asset hashes. Agent checks establish readiness for human review, not acceptance.

Delivery readback checked all 1,584 candidate SVG/fragment hashes plus 72 accepted
parent SVGs. All 594 comparisons of inherited transistor parts matched in geometry
and effective stroke styling. The reused ADC and band-pass retain all 36 original
SVGs byte for byte. All 84 opening events, prior decisions and comments were retained.
The public catalog and all 1,035 published SVG hashes matched the before-task snapshot;
the website remains build `826fc3ddf903`.

Generated SVGs, contact sheets, upload packages and private receipts live outside Git under the
desktop's `Local/batch-03/rendered`; immutable hosted revisions retain source and artwork.
Credentials and user feedback are excluded from public commits. No application redeployment is needed.

## Reproduce one candidate

From the repository, using the configured desktop Python and a private connection file:

```powershell
python app/batches/batch-03/run.py --config <private-config.json> --work <own-output-folder> prepare <symbol-id>
```

Inspect the generated proof before submitting. The runner reuses an identical source cache;
submission uses a stable revision ID, retrieves the saved source, and checks every hosted SVG.
Do not modify a source already under review: corrections use the normal linked Review workflow.

For source checks without rendering or credentials:

```powershell
python -m unittest discover -s tests -p test_batch_03.py -v
```

For a fresh read-only hosted check with the existing private desktop connection:

```powershell
python tests/verify_batch_03.py --config <private-config.json>
```

Expected: 84 designs, 792 configurations, 1,584 hosted hashes, zero service writes.
Use [the normal test commands](../DEVELOPMENT.md#test-and-review) after source changes.
