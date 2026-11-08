# Current checkpoint

Updated: 08-11-2026. Read this first when resuming; verify the checkout before acting.

## Objective and mode

Current collection focus: collection is paused at the user's request after recording Figures 3.111, 4.7, 4.13, 4.29, 4.58, 4.61, 4.62, 4.63, 4.73, 4.80, and 4.87. The AOE collection now has twenty-seven reference records: five recreated and twenty-two awaiting a drawing request. Captions, source relationships, and provisional visual observations are saved. Figure 4.87 is explicitly liked as a more complex project schematic. No new drawings or general rules were adopted. See [the collection wrap-up](LOG.md#aoe-opamp-project-reference-wrapup).

Develop The Art of Electronics illustration style through reference examples and practical drawing trials, including the agent's preservation behavior. Project scope includes schematics, conceptual diagrams, waveforms, plots, equations, and integrated figures; see [DIRECTION.md](../DIRECTION.md).

The user authorized the full gallery plan: add human browsing pages, simplify the main README, finish Figures 1.1, 1.6, and 1.11 as LaTeX/PNG recreations, check navigation, and push. The implementation is complete; user review of the gallery and those three recreations is pending. See [the gallery checkpoint](LOG.md#gallery-completion).

The user explicitly approved SVG as the default for chat and GitHub and authorized updating all five examples while retaining PNGs. The repair is implemented: transparent light/dark SVGs, updated galleries and workflow, and repeatable exports. Both themes were checked locally and on live GitHub, including an explicit light site theme with a dark system theme; the original site setting was restored. All five LaTeX sources and PNGs are unchanged. See [the completed presentation checkpoint](LOG.md#svg-presentation-complete).


The user approved a style-independent preferences layer and an agent-led suggestion workflow. [General preferences](../preferences/GENERAL.md), explicit style inheritance, automatic suggestions during Schematica use, and continued correction of one example are implemented and checked. The output-stage trial's four supply arrows are restored; its two signal terminals remain hollow black circles and values remain 9 pt. The delivered ZIP was updated in place. Routine context updates and their commits/pushes remain authorized under [AGENTS.md](../AGENTS.md); adding the trial to the permanent example collection still needs approval.

The approved preference-bank migration is implemented: [Symbols gallery](../preferences/symbols/README.md), separate [supply-arrow rule](../preferences/symbols/power-supply-arrows/RULE.md) and [signal-terminal rule](../preferences/symbols/signal-terminal-circles/RULE.md), minimal human READMEs, and a deterministic gallery builder. Root AGENTS routes chat behavior and maintenance to the two files in `agents/`. Earlier awaiting-approval notes are superseded by explicit implementation/validation/commit/push authorization. Local validation is complete (17 acceptance checks, both display themes, and a fresh read-only inheritance/recovery audit). GitHub synchronization is blocked by name-resolution failures; see [the migration checkpoint](LOG.md#preference-bank-migration).

## What exists

- The [example collection workflow](../skills/schematica-examples/SKILL.md), [collection index](../examples/INDEX.md), and [The Art of Electronics style guide](../examples/THE_ART_OF_ELECTRONICS/STYLE.md) are implemented. The collection is still developing; shared visual patterns are provisional.
- Twenty-seven AOE reference records are saved. Five have editable LaTeX, transparent light/dark SVG previews, PNG downloads, captions, and human browsing pages; twenty-two have captions and observations only (including source equations where supplied). The pending source images were inspected in the collecting chat and are not available as repository previews. Start at [the gallery](../examples/THE_ART_OF_ELECTRONICS/README.md) for completed drawings and [the style guide](../examples/THE_ART_OF_ELECTRONICS/STYLE.md) for all records.
- All five drawings are visual recreations using TikZ paths inside CircuitikZ, not semantic native-component templates. Figures 1.7 and 1.43 retain their previously reviewed source and PNG unchanged. The assistant checked the three new recreations against the book; user review is pending. Appearance approval does not approve every implementation detail or make the style complete.
- The collection workflow and first records were saved in commit `88e9231`. Earlier validation recorded successful compilation and fresh-session collection discovery. These are historical results, not a new test of all rendering tools on another device.
- Original screenshots, the source book PDF, earlier experiments, and the prematurely built package remain outside the repository. Their existence does not make them approved project content. A repo-only session can now visually inspect all five saved recreations without the book.
- The output-stage trial uses native CircuitikZ devices and has editable TeX, SVG, PNG, and PDF exports. Working artifacts are in the ignored `build/aoe-output-stage-test/` directory on the creating machine, with a downloadable ZIP delivered separately. These artifacts have not been added to the versioned collection and are not synchronized by Git. See [the trial checkpoint](LOG.md#output-stage-trial).

## Current checkpoint verification

On 08-11-2026 an independent read-only session recovered the objective, five records/two drawings, provisional style, open questions, approval boundary, and a proposed next step using only this checkout. Memory injection and web access were disabled; no prior conversation or expected answers were supplied. Its tool trace followed the repository reading path, and all 20 project files were byte-for-byte unchanged. This verifies context recovery, not offline tool installation or the unperformed new-circuit trial. See [the context-workflow decision and audit](LOG.md#context-workflow).

The later gallery update compiled all three new standalone sources, compared their renders with the book, and checked that each PNG matches its compiled PDF. Browser review followed the main README into the gallery, through all five example pages and back, with all gallery images loaded. Captions and relative links were checked; the earlier two source/PNG pairs remain unchanged. This is gallery/drawing verification, not a new independent context-recovery test.

## Open decisions

- User review of the gallery and three newly completed recreations, and which reference to collect next.
- User review of the split visual preference pages, further examples/corrections for the bank, and whether to preserve the full output-stage trial as an example.
- Which observed patterns become confirmed rules; exact typography, spacing, line weights, symbol proportions, and quantitative plot conventions remain unsettled.
- Personal customization and storage, distribution as a plugin, and generalization beyond electronics remain to be designed.
- Difference-only storage for intermediate drawings remains undecided. The present workflow uses complete files for selected useful revisions.
- The preserve-after-feedback workflow has been exercised in a limited earlier trial, but has not yet been validated through the planned full new-circuit creation and review cycle.
- Repo-based recovery is the agreed durable fallback. Independent operation on another device still requires its checkout and necessary tools/references; offline execution and automatic transfer of local tools have not been established.

## Next useful step

Review the gallery and new recreations, then continue collecting references. Figure 1.6 was explicitly selected and completed as part of the three missing examples, superseding its earlier status as an assistant-only suggestion.

Continue correcting the output-stage example or reviewing supplied references normally; the split visual preferences are ready for user review. The agent should notice reusable lessons, propose their scope, and maintain the visual bank within approved saves. Preserve the distinction between a user-confirmed rule, an inferred candidate, and a current-drawing adjustment. Verify synchronization separately; network errors have blocked pushes from this drawing session.

For reasoning and scope changes, consult [LOG.md](LOG.md). For drawing details, read selected example records and actual available previews rather than treating descriptions as images.

## Integration exploration - 08-11-2026

The user requested a broader review of existing solutions that could serve Schematica's goals. The [candidate comparison](LOG.md#existing-solutions) records 12 distinct tool families, sources, integration routes, effort, and exclusions. The assistant shortlist is VisioCirkit's editor/agent utilities, Lcapy, PGFPlots, Playwright visual comparisons, and ELK/libavoid for later layout work. These are proposals; no dependencies were installed, imports tested, or implementation authorized. The next proposed step is a small comparison using a structured voltage divider and a copy of the output-stage trial. Preserve current drawing and preference-bank work. Remote inspection failed during research, so synchronization has not been established by this review.

Preference-bank refinement (08-11-2026): the agreed migration is authorized and implemented; see [the result and verification](LOG.md#preference-bank-migration). The existing AOE collection work continues independently.
