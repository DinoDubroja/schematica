# Context log

Concise project history, with proposals, decisions, implementation, and verification kept distinct. [CURRENT.md](CURRENT.md) is the maintained starting point. Dates below identify recorded checkpoints; earlier discussion is summarized where an exact event date is not established. User statements are summarized unless quoted.

## 08-11-2026 — Product direction and approval boundary

**Status:** agreed direction; earlier experiments are not blanket implementation approval.

The user wants agents to produce beautiful, useful electronics illustrations from the first prompt using predefined preferences, realistic examples, and design patterns inferred from those examples. Supplied circuit connections, names, values, and technical meaning must be preserved. The scope expanded from schematics to conceptual diagrams, graphs, symbolic notation, equations, and combined circuit-and-waveform figures. The approved direction is maintained in [DIRECTION.md](../DIRECTION.md).

Discussion, brainstorming, and approval of a visual presentation do not authorize implementing every idea or preserving every displayed feature as a rule. A prematurely built package and earlier drawing experiments were outside the initially approved three-document repository. Later explicit approval covered saving the existing examples and the reusable collection workflow; it did not adopt that earlier package.

Source: user instructions and corrections in the project conversations, reflected in the repository's direction and agent instructions. Original context-recovery sources were the chats titled “Design template creation skill” and “Review design template approval flow”; their availability is not required to resume from these records.

## 08-11-2026 — The Art of Electronics collection

**Status:** collection structure and workflow agreed and implemented; shared visual patterns provisional.

The user chose a dedicated folder for each full source/style name and the filename `STYLE.md`. [INDEX.md](../examples/INDEX.md) selects relevant style guides; a style guide generalizes patterns and selects particular examples. Agents should inspect relevant rendered examples and their context rather than reading the whole library every time.

Keep editable LaTeX and a PNG preview together for developed examples. The source supports reuse and generation; the PNG supports human browsing and agent visual inspection. Preserve captions and useful descriptions in the repository with the example. Original screenshots are working inputs, not outputs to import into the repository. A reference supplied without comments is liked overall; specific praise identifies the feature liked and does not approve every other detail.

The first collection has five references:

- Figure 1.1: abstract parallel connection, useful beyond component-level schematics.
- Figure 1.6: voltage divider with voltage relationships and an adjacent equation.
- Figure 1.7: adjustable divider alternatives, with small signal sketches near terminals.
- Figure 1.11: a conceptual network and its Thevenin equivalent, illustrating a principle rather than a practical layout.
- Figure 1.43: a leading-edge detector combining circuit points A/B/C with corresponding waveform panels.

The two recreated figures, 1.7 and 1.43, received positive feedback on appearance. Their traced TikZ geometry and substitute typography are not confirmed universal implementation choices. Three other references remain description/caption records with recreation pending. See the [style guide](../examples/THE_ART_OF_ELECTRONICS/STYLE.md) for authoritative per-example availability and provisional patterns.

Implementation authority: the user explicitly requested, “Save our existing examples with their captions in the repo and set up the reusable collection workflow so I can start or resume it in a new chat.” Completed in commit `88e9231`; the implementation checkpoint recorded successful compilation of both drawings, fresh-session workflow discovery, and isolated collection/feedback checks. A full new practical-circuit trial is still pending.

## 08-11-2026 — Learning from generated illustrations

**Status:** reusable preservation workflow implemented; broader validation and storage design remain open.

The user proposed generating new work from a developing style, iterating with feedback, and retaining accepted results as useful examples. Prompts, relevant context, feedback, corrections, and selected intermediate versions add evidence that a reference image alone lacks. The agent should notice preservation opportunities and offer a concrete save, while the user controls what becomes lasting guidance.

The [implemented workflow](../skills/schematica-examples/SKILL.md) distinguishes origin (reference or generated) from evaluation. It offers preservation after useful feedback, saves with explicit or established scoped approval, and uses complete source/preview files for selected instructive revisions. It does not automatically save every iteration or treat praise as publication permission. Difference-only storage remains an idea to evaluate later.

The broader ambition is a reusable way to build styles from examples in other domains. Electronics plots and notation are already within Schematica's direction; general artifact-template tooling, plugin distribution, and personal customization/storage remain undecided.

## 08-11-2026 — Presentation and documentation

**Status:** agreed preferences; operational details remain subject to the user's current request.

Show schematics inline in chat, using transparent, theme-aware SVG where supported. This presentation preference does not replace the saved PNG used for browsing or require a particular feature in every drawing. Keep the user's technical meaning and source-specific annotations intact.

Useful examples and lessons should be preserved as work progresses, with scope and approval visible. Shared style claims remain provisional until confirmed. Do not require finishing a whole style before collecting another example. Approved documentation and the example records carry reusable knowledge; a conversation alone is not the durable project record.

<a id="context-workflow"></a>

## 08-11-2026 — Reliable continuation and context logging

**Status:** workflow approved, implemented, and independently tested; ongoing scoped maintenance authorized.

The user experienced unreliable continuation across devices. A later user-reported Cloud test showed conversation continuity and fresh reads from the original connected computer; this did not establish independent execution with that computer offline. The project should therefore be recoverable from synchronized repository files regardless of chat availability. Private account and machine details are intentionally omitted.

The agreed structure is a short `context/CURRENT.md` checkpoint and dated `context/LOG.md` history, with startup/update instructions in `AGENTS.md`. Existing product direction and style documents remain authoritative for their subjects. The reusable procedure belongs in the Project_Workflow repository and is reachable through personal instructions; Schematica's local instructions must remain sufficient for repo-only recovery.

Routine context notes and their commits/pushes are authorized at meaningful checkpoints, including during discussion. Logging an idea does not authorize its implementation. Preserve decisions, reasons, corrections, open questions, completed work, and actual verification. Avoid raw chat dumps, duplicate specifications, and private material in this public repository. Report a synchronization failure instead of claiming another device can already recover the latest state.

Implementation authority: the user requested, “Set up the reusable context logging workflow, apply it to Schematica, and save our decisions and open questions. Then test that a fresh chat can continue from the repo alone.”

**Verification on 08-11-2026:** an independent ephemeral session ran read-only with prior-memory injection, automatic instruction preloading, and web access disabled. It was given only a request to recover this project from the working checkout, with no expected answers or old conversation. It explicitly read `AGENTS.md`, followed the local context/direction/collection routes, checked the file inventory, and correctly recovered the product objective, five reference records/two drawings, provisional patterns, missing source assets, open decisions, standing logging authorization, and the distinction between logging and implementation approval. It recommended Figure 1.6 as a next recreation while explicitly retaining the need for the user's choice and its missing visual source. That recommendation is not an adopted task.

The first test attempt could not read files because the isolated test configuration omitted the configured Windows execution setting. Restoring that setting for the test process allowed the read-only audit to finish; no global settings were changed. The successful run's tool trace used only repository content, and a before/after hash check found all 20 project files unchanged. Entry-point links and the updated personal reading routes were also checked. Raw test evidence remains a local working artifact, not a dependency for resumption.

This validates recovery of project context in a fresh session. It does not validate a full new-circuit drawing/review cycle, every future logging action, a second machine's installed tools, or independent execution with the original computer offline.

<a id="output-stage-trial"></a>

## 08-11-2026 - First practical output-stage style trial

**Status:** drawing authorized and rendered; user review and permanent collection preservation pending.

The user requested one test of the current The Art of Electronics style using a screenshot of their hand-drawn output stage, before continuing to add reference examples. This selected the practical trial previously left open. The request authorized a faithful redraw, not circuit redesign or adoption of new global style rules.

The drawing uses native CircuitikZ components, preserving the supplied connections, eight transistor identifiers, component values, offset trim, optional resistor/short annotation, and current annotation. The existing divider and leading-edge-detector previews informed monochrome treatment, typography, symbols, and label clearance. The first rendering was inspected and refined for trimmer orientation, resistor spacing, ground symbols, and label clearance. TeX compiled to one page; the exports' identifiers and value counts were checked, and the connections were compared visually with the sketch. No circuit simulation or electrical performance validation was performed.

Editable TeX and SVG/PNG/PDF exports are available as working artifacts in the ignored `build/aoe-output-stage-test/` directory and were packaged for delivery. They are not yet versioned collection assets. The original screenshot remains a working input. The shared style guide and reference collection were not changed.

The default compiler could not load its bundle in this session. Using an existing local Tectonic cache and available sans-serif fonts allowed compilation. This establishes this drawing's renderability on the current machine, not general portability of the runtime. Git synchronization encountered a network name-resolution failure; check the actual remote before assuming this checkpoint is available on another device.

Next: obtain user feedback on the trial, make requested refinements, offer a concrete preservation step when useful, and then resume example collection. A positive reaction alone does not authorize publication of the drawing.

### First user feedback and terminal/typography revision

**Status:** first rendering liked overall; requested revision implemented and exported; collection preservation not yet authorized.

The user called the result "pretty good" and asked for hollow black terminal circles and slightly smaller component-value text. The revision uses six unfilled black circles for the input/output and exposed supply terminals, with wires ending at their boundaries. Component values, including the offset potentiometer, changed from 10 pt to 9 pt; transistor identifiers and other annotations retain their sizes. One nearby resistor label moved to clear the trim supply label. The source compiles, all supplied values and transistor identifiers remain present, the six unfilled black terminal paths and reduced value font size were checked in the PDF, and the rendering was visually inspected. The delivered ZIP was updated in place. These are drawing-specific changes, not approved global style rules.

### Correction and proposal for shared schematic preferences

**Status:** user clarified the intended symbol distinction and requested a proposal; implementation pending.

The user rejected applying the hollow-circle change to supply rails: supply connections should retain arrows, while signal input/output terminals use hollow circles. This corrects the preceding revision's interpretation; that revision's successful rendering checks did not establish that the requested scope was followed. The current delivered drawing has not yet been repaired.

The user wants general preferences that apply regardless of the chosen style, explicit style-specific overrides, and a workflow that develops guidance from multiple examples and corrections. Agents should proactively suggest useful additions instead of waiting for the user to manage documentation.

The assistant's proposal is a shared `preferences/GENERAL.md` containing accepted defaults and a clearly inactive proposal section; existing example records hold feedback and selected before/after evidence, with scope and links to the applicable rules. Existing style guides declare only explicit exceptions. Extend the existing collection workflow and agent entry point to read general guidance before the selected style, classify feedback as general/style/local, propose useful rules with evidence, and check applicable rules before delivery. New inferred rules require review; rejected suggestions should not be repeated without new evidence. Current task requirements take precedence, then explicit style exceptions, then shared defaults; visual preferences cannot alter circuit connectivity or technical meaning.

The proposed implementation includes restoring supply arrows in the trial, updating discovery/reading routes and the example record format, and checking inheritance and explicit exceptions on small cases. No preference file, style rule, or workflow definition has been changed by this proposal checkpoint.
