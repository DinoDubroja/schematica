# Current checkpoint

Updated: 08-11-2026. Read this first when resuming; verify the checkout before acting.

## Objective and mode

Style organization migration (08-11-2026): explicitly authorized, implemented, and locally verified. The collection now lives under [styles/](../styles/INDEX.md). The Art of Electronics has [shared guidance](../styles/THE_ART_OF_ELECTRONICS/STYLE.md), [schematic guidance](../styles/THE_ART_OF_ELECTRONICS/SCHEMATICS.md), and [qualitative plot/signal guidance](../styles/THE_ART_OF_ELECTRONICS/PLOTS.md), with 15 schematic, 1 plot, and 15 mixed example records. No writing guide/category was created. Existing guidance remains at its previous review status; no new style parameters were adopted. See [scope and verification](LOG.md#style-organization-migration).

Current collection focus: the curated AOE showcase and complete category browsing are implemented. The original PNG imports for Figures 5.77 and 5.78 remain authorized but blocked by image-host name resolution. There are still 31 records: five recreations and 26 without saved images. Figure 5.78 stays intact; Figure 4.87 remains liked as a complex project schematic. No new style generalization is authorized. See [the pilot checkpoint](LOG.md#aoe-image-gallery-pilot). The changes are committed locally; the normal GitHub push failed with a name-resolution error, so remote availability is unverified.

Style analysis is deferred (08-11-2026): the user explicitly instructed not to infer style generalization from examples during this implementation. Existing qualitative observations remain provisional; no numeric parameters or shared preset were added. The earlier [numeric-style proposal](LOG.md#aoe-numeric-style-gap) remains a possible later activity, not current authorization.

Image-reference workflow (08-11-2026): implemented. Authorized original pictures may be saved unchanged and shown directly with their original backgrounds; image-only references are complete without LaTeX or themed variants. The save/record/presentation instructions now describe this route. Two pilot imports remain blocked; see [actual state and completion steps](LOG.md#aoe-image-gallery-pilot).

Curated AOE gallery (08-11-2026): the five existing SVGs remain temporary showcase highlights. The user chooses favorites; category/subcategory organization is delegated. The new all-examples index and category pages expose every record, distinguishing available visuals from notes without images. See [implementation and outstanding import](LOG.md#aoe-image-gallery-pilot).

Develop The Art of Electronics illustration style through reference examples and practical drawing trials, including the agent's preservation behavior. Project scope includes schematics, conceptual diagrams, waveforms, plots, equations, and integrated figures; see [DIRECTION.md](../DIRECTION.md).

The user authorized the full gallery plan: add human browsing pages, simplify the main README, finish Figures 1.1, 1.6, and 1.11 as LaTeX/PNG recreations, check navigation, and push. The implementation is complete; user review of the gallery and those three recreations is pending. See [the gallery checkpoint](LOG.md#gallery-completion).

The user explicitly approved SVG as the default for chat and GitHub and authorized updating all five examples while retaining PNGs. The repair is implemented: transparent light/dark SVGs, updated galleries and workflow, and repeatable exports. Both themes were checked locally and on live GitHub, including an explicit light site theme with a dark system theme; the original site setting was restored. All five LaTeX sources and PNGs are unchanged. See [the completed presentation checkpoint](LOG.md#svg-presentation-complete).


The user approved a style-independent preferences layer and an agent-led suggestion workflow. [General preferences](../preferences/GENERAL.md), explicit style inheritance, automatic suggestions during Schematica use, and continued correction of one example are implemented and checked. The output-stage trial's four supply arrows are restored; its two signal terminals remain hollow black circles and values remain 9 pt. The delivered ZIP was updated in place. Routine context updates and their commits/pushes remain authorized under [AGENTS.md](../AGENTS.md); adding the trial to the permanent example collection still needs approval.

The approved preference-bank migration is implemented: [Symbols gallery](../preferences/symbols/README.md), separate [supply-arrow rule](../preferences/symbols/power-supply-arrows/RULE.md) and [signal-terminal rule](../preferences/symbols/signal-terminal-circles/RULE.md), minimal human READMEs, and a deterministic gallery builder. Root AGENTS routes chat behavior and maintenance to the two files in `agents/`. Earlier awaiting-approval notes are superseded by explicit implementation/validation/commit/push authorization. Local validation is complete (17 acceptance checks, both display themes, and a fresh read-only inheritance/recovery audit). GitHub synchronization is blocked by name-resolution failures; see [the migration checkpoint](LOG.md#preference-bank-migration).

## What exists

- The [example collection workflow](../skills/schematica-examples/SKILL.md), [collection index](../styles/INDEX.md), and [The Art of Electronics style guide](../styles/THE_ART_OF_ELECTRONICS/STYLE.md) are implemented. The collection is still developing; shared visual patterns are provisional.
- Thirty-one AOE reference records are saved: five have LaTeX/SVG/PNG and human pages, twenty-six have notes without images. Browse the [showcase](../styles/THE_ART_OF_ELECTRONICS/README.md) or [all categories](../styles/THE_ART_OF_ELECTRONICS/examples/README.md). The two approved PNG imports are not yet complete.
- All five drawings are visual recreations using TikZ paths inside CircuitikZ, not semantic native-component templates. Figures 1.7 and 1.43 retain their previously reviewed source and PNG unchanged. The assistant checked the three new recreations against the book; user review is pending. Appearance approval does not approve every implementation detail or make the style complete.
- The collection workflow and first records were saved in commit `88e9231`. Earlier validation recorded successful compilation and fresh-session collection discovery. These are historical results, not a new test of all rendering tools on another device.
- Original screenshots and the source book PDF remain outside the repository. Original images are now permitted within approved collection scope; the two pilot imports are blocked. No source-book PDF, earlier experiment, or output-stage trial was added.
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

Preference presentation and junction dots (08-11-2026): implemented the user's
request for colored Good/Bad words without icons and a new
[Connections / Junction dots](../preferences/connections/junction-dots/RULE.md)
preference. After reviewing a 10:1 preview in chat, the user explicitly accepted
that junction diameter-to-wire-width ratio and requested updating the preference
and examples. Both supply illustrations and the junction comparison now use 10:1,
with Good/Bad side by side. The earlier 7:1 trial is superseded. See
[the approval and checks](LOG.md#ten-width-junction-adoption).

The earlier [style organization proposal](LOG.md#style-first-organization) and [domain proposal](LOG.md#source-style-domains) are superseded by the [authorized migration](LOG.md#style-organization-migration). Writing remains a future domain without content; numeric-style analysis remains deferred, while the image-reference workflow and browsing are implemented with two imports still blocked.
