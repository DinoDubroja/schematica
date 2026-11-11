# Current checkpoint

Updated: 11-11-2026. Read this first when resuming; verify the checkout before acting.

Scope discussion (11-11-2026): the user clarified two core Schematica outcomes:
beautiful component-level electronic schematics and beautiful system/signal-flow
diagrams, with integrated plots, annotations, writing and teaching explanations.
Simulation and eventual component sourcing belong in the broader vision; separating
simulation into a companion project remains an open proposal. The assistant
recommends one amplifier demonstration first: a real SPICE run, a polished schematic,
a response plot and a short explanation, with a bounded feedback-resistor comparison.
The next system-diagram example would be an RF receiver. These are proposed tasks,
not implementation approval; no new project, integration, drawing or preference has
been adopted. See [scope and proposed first milestone](LOG.md#visual-explanation-and-simulation-boundary).

## Objective and mode

Ground-symbol preference (08-11-2026): the user selected standalone A2/B1/D1 shapes and explicitly authorized saving them at a common width of 25 wire strokes. [G-SYMBOL-03](../preferences/symbols/ground-symbols/RULE.md) accepts a single bar or open 2:1 triangle for circuit ground and reserves the compact three-line form for PE/earth. Neither circuit-ground form is designated default. The [standalone examples](../preferences/symbols/ground-symbols/README.md), editable source, transparent SVG themes and PNG are saved, with source dimensions and exports checked. See [approval and verification](LOG.md#ground-symbols-25-widths).

Schematica Preferences & Examples (08-11-2026): implemented and installed as `$schematica-preferences`, with Schematica-specific natural-language discovery. The agent helps select a starting point from a broad topic, shows requested visual options in chat, refines the same preview, and saves preferences/examples only within explicit approval. The complete download now includes [Windows Codex installation instructions](../INSTALL.md) and a PowerShell 7 helper. Installed use is separate from development/publication authorization. Setup/discovery checks, 11 automated tests, documentation links and a fresh read-only conversation walkthrough passed; no new op-amp drawings were rendered or adopted. See [scope, checks and limits](LOG.md#schematica-preferences-guided-setup).

Resistor preferences (08-11-2026): European/default versus US is now a separate convention-rule preview. The resistor geometry/size preview retains only Small 75%, Medium (default) 100%, Large 125%, and colored Good/Bad headings; explanatory captions and dimensions are removed from the visual. All eight drawings remain unchanged. The user liked the horizontal 75%/100%/125% Good examples; the EU-height-distortion and uneven-US-zigzag Bad proposals remain for review. Medium geometry is EU 30w by 12w and US 36w by 12w. Keep line weight as a separate passive/source-outline rule, excluding op amps, and defer its own preview. Exact geometry belongs in the underlying rule definition. No permanent component rule or illustration has been saved. See [decisions and current split](LOG.md#resistor-convention-and-proportions) and [required preview behavior](../agents/BEHAVIOR.md#presenting-illustrations).

Terminal example refinement (08-11-2026): the user reviewed the RC circuit comparison in chat and explicitly authorized saving it. [G-SYMBOL-02](../preferences/symbols/signal-terminal-circles/RULE.md) now explicitly rejects omitted or solid-filled signal-terminal circles. The [Good/Bad examples](../preferences/symbols/signal-terminal-circles/README.md) show the same RC circuit: hollow terminals in Good, and two labeled incorrect treatments together in Bad. All three retain the correct internal junction dot and accepted marker/wire dimensions. Source, SVGs, PNGs and the Symbols gallery are updated and locally verified. See [approval and checks](LOG.md#terminal-circuit-examples).

Preferences scope (08-11-2026): the user approved removing the general cross-project Preferences setup and focusing on the existing Schematica preferences-and-examples workflow. The general skill files, Codex link and personal reading routes are removed; Codex discovery confirms that the Schematica workflow remains enabled. Existing project preferences, examples and workflow files are unchanged. Generalization is deferred until practical use produces a workflow the user wants to reuse. See [the cleanup decision and verification](LOG.md#preferences-general-setup-cleanup).

Default in-chat presentation (08-11-2026): explicitly approved and saved in [chat behavior](../agents/BEHAVIOR.md#presenting-illustrations) and [the presentation procedure](../scripts/PRESENTATION.md#chat). Schematica delivers illustrations and comparisons directly in the conversation unless the user requests another format or destination. Discussion previews remain separate from implementation/preservation approval. Native vector presentation, theme-aware colors, labeled equal-scale comparisons, useful controls and capability fallbacks are documented. Direction and existing reading links are consistent. See [authorization and verification](LOG.md#default-in-chat-presentation).

Crossing presentation correction (08-11-2026): the user reviewed the in-chat preview and explicitly authorized the [updated comparison](../preferences/connections/unconnected-crossings/README.md). The left Good cell contains the labeled straight/default and bridged drawings side by side; the right Bad cell contains the gap crossing at the same drawing scale. The previous Bad-below layout was rejected and had been implemented without approval. The accepted 0.65 pt wire choice is retained. See [the correction, scope and checks](LOG.md#crossing-good-cell-correction). The separate in-chat presentation proposal was subsequently approved and saved; see [the adopted workflow](LOG.md#default-in-chat-presentation).

Terminal-circle size (08-11-2026): the user selected C from the 8/10/12 comparison and explicitly authorized adopting a visible outer diameter of 12 times wire width. [G-SYMBOL-02](../preferences/symbols/signal-terminal-circles/RULE.md) and both input/output examples now specify hollow circles with outlines equal to wire thickness. Source, SVG themes and PNG are updated and locally verified; the separate 10-times junction-dot rule is unchanged. See [approval and checks](LOG.md#twelve-width-terminal-circles).

Fastest release path proposed (08-11-2026): [focused pass](LOG.md#first-release-fast-path), starting in the local project chat with a reusable AOE preset and Norton-equivalent drawing as the first visual review milestone, followed by two fresh-prompt cases and a generic-default pass. Five general preferences are now accepted. Style consolidation and new trials remain proposed pending the user's go-ahead; the original-image import is already authorized.

Connection preferences (08-11-2026): the user approved and authorized two separate rules: [explicit wire junctions](../preferences/connections/explicit-wire-junctions/RULE.md) and [unconnected crossings](../preferences/connections/unconnected-crossings/RULE.md). Both four-way and staggered T-junctions require circles, using the existing appearance rule. Plain unconnected crossings are the default; the exact instruction **wire bridges** selects the bridge variant; gap crossings are rejected. Rules, separate Good/Bad comparisons, the bridge illustration, editable sources and both SVG themes are implemented and locally verified. User review of the newly saved illustrations remains open. See [scope and checks](LOG.md#separate-junction-and-crossing-rules).

Attachment-transfer handoff (08-11-2026): the user confirms the settings are already configured and identifies these recurring restrictions as a cloud-chat issue. Follow the [saved behavior](../agents/BEHAVIOR.md#recurring-cloud-chat-access-failures): suggest continuing in the local project chat, preserve task context, and do not repeat settings advice or require manual screenshot collection. The previous settings-change recommendation is superseded; the network-disabled observation describes only this executor. See [the correction and pending cross-project save](LOG.md#cloud-chat-local-handoff).

First-release review (08-11-2026): the user defined the minimum release outcome and requested an audit. The [readiness review](RELEASE_READINESS.md) identifies the remaining style preset, synthetic trials, broader approved preferences, full picture gallery, installation/customization, and release packaging work. Review is complete; implementing those proposed stages is not yet authorized. The original-image transfer still failed before any file reached the checkout. All 26 missing pictures remain outstanding; continue the original-attachment import in the local project chat without asking the user to collect them manually.

Style organization migration (08-11-2026): explicitly authorized, implemented, and locally verified. The collection now lives under [styles/](../styles/INDEX.md). The Art of Electronics has [shared guidance](../styles/THE_ART_OF_ELECTRONICS/STYLE.md), [schematic guidance](../styles/THE_ART_OF_ELECTRONICS/SCHEMATICS.md), and [qualitative plot/signal guidance](../styles/THE_ART_OF_ELECTRONICS/PLOTS.md), with 15 schematic, 1 plot, and 15 mixed example records. No writing guide/category was created. Existing guidance remains at its previous review status; no new style parameters were adopted. See [scope and verification](LOG.md#style-organization-migration).

Current collection focus: the user clarified that every collected example must have a visible picture in the deeper category galleries. The showcase remains a small selection of SVG favorites. The gallery is incomplete: 31 records exist, but only five have saved images and 26 remain text-only. Completing the remaining original-image imports is the correction target; the previous two-image pilot does not fulfill the full requirement. Source-image access was blocked during the prior attempt. No new style generalization or LaTeX recreation is authorized. See [the clarified requirement and actual state](LOG.md#all-examples-visible).

Style analysis is deferred (08-11-2026): the user explicitly instructed not to infer style generalization from examples during this implementation. Existing qualitative observations remain provisional; no numeric parameters or shared preset were added. The earlier [numeric-style proposal](LOG.md#aoe-numeric-style-gap) remains a possible later activity, not current authorization.

Image-reference workflow (08-11-2026): implemented. Authorized original pictures may be saved unchanged and shown directly with their original backgrounds; image-only references are complete without LaTeX or themed variants. The save/record/presentation instructions now describe this route. Two pilot imports remain blocked; see [actual state and completion steps](LOG.md#aoe-image-gallery-pilot).

Curated AOE gallery (08-11-2026): the five existing SVGs remain temporary showcase highlights. The user chooses favorites; category/subcategory organization is delegated. The new all-examples index and category pages expose every record, distinguishing available visuals from notes without images. See [implementation and outstanding import](LOG.md#aoe-image-gallery-pilot).

Develop The Art of Electronics illustration style through reference examples and practical drawing trials, including the agent's preservation behavior. Project scope includes schematics, conceptual diagrams, waveforms, plots, equations, and integrated figures; see [DIRECTION.md](../DIRECTION.md).

The user authorized the full gallery plan: add human browsing pages, simplify the main README, finish Figures 1.1, 1.6, and 1.11 as LaTeX/PNG recreations, check navigation, and push. The implementation is complete; user review of the gallery and those three recreations is pending. See [the gallery checkpoint](LOG.md#gallery-completion).

The user explicitly approved SVG as the default for chat and GitHub and authorized updating all five examples while retaining PNGs. The repair is implemented: transparent light/dark SVGs, updated galleries and workflow, and repeatable exports. Both themes were checked locally and on live GitHub, including an explicit light site theme with a dark system theme; the original site setting was restored. All five LaTeX sources and PNGs are unchanged. See [the completed presentation checkpoint](LOG.md#svg-presentation-complete).


The user approved a style-independent preferences layer and an agent-led suggestion workflow. [General preferences](../preferences/GENERAL.md), explicit style inheritance, automatic suggestions during Schematica use, and continued correction of one example are implemented and checked. The output-stage trial's four supply arrows are restored; its two signal terminals remain hollow black circles and values remain 9 pt. The delivered ZIP was updated in place. Routine context updates and their commits/pushes remain authorized under [AGENTS.md](../AGENTS.md); adding the trial to the permanent example collection still needs approval.

The approved preference-bank migration is implemented: [Symbols gallery](../preferences/symbols/README.md), separate [supply-arrow rule](../preferences/symbols/power-supply-arrows/RULE.md) and [signal-terminal rule](../preferences/symbols/signal-terminal-circles/RULE.md), minimal human READMEs, and a deterministic gallery builder. Root AGENTS routes chat behavior and maintenance to the two files in `agents/`. Earlier awaiting-approval notes are superseded by explicit implementation/validation/commit/push authorization. Local validation is complete (17 acceptance checks, both display themes, and a fresh read-only inheritance/recovery audit). GitHub synchronization is blocked by name-resolution failures; see [the migration checkpoint](LOG.md#preference-bank-migration).

## What exists

- The [example collection workflow](../skills/schematica-preferences/SKILL.md), [collection index](../styles/INDEX.md), and [The Art of Electronics style guide](../styles/THE_ART_OF_ELECTRONICS/STYLE.md) are implemented. The collection is still developing; shared visual patterns are provisional.
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
