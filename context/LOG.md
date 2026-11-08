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

<a id="gallery-completion"></a>

## 08-11-2026 — Human gallery and completion of missing examples

**Status:** explicitly authorized and implemented; assistant verification complete; user visual review pending.

The user liked browsing the collection but found the agent-oriented `STYLE.md` too verbose as a landing page. They corrected the missing visual assets in three examples and the main README's premature skill-invocation and installation instructions. A collection should open as a short visual gallery, with readable example pages; detailed style and feedback records remain available separately. Public README content should describe finished, available work rather than an unestablished product interface.

Implementation authority: “Add the style gallery README, simplify the main README, and finish the three missing examples with LaTeX and PNGs. Check the browsing flow and push the changes.” The approved plan also covered individual example pages and keeping the reusable collection workflow consistent with that browsing structure.

The main README now links to [The Art of Electronics gallery](../examples/THE_ART_OF_ELECTRONICS/README.md). All five example folders have a picture-first README with file links, original caption/source information, and navigation. Figures 1.1, 1.6, and 1.11 now have editable LaTeX and PNGs rendered from it, including their captions. Figures 1.7 and 1.43 retain their existing source and PNG unchanged. The collection guide, index, direction, agent instructions, and record workflow now distinguish human galleries from detailed agent guidance. Pending metadata records remain possible within authorized collection scope but must not be presented as finished visual examples.

The new sources preserve the book's geometry as editable TikZ paths inside CircuitikZ, using TeX Gyre Heros as a typography approximation. They do not embed source screenshots and are not semantic native-component templates. Original reference feedback is preserved separately from the still-pending user review of these recreations. No new inferred style pattern was promoted into an approved rule.

Verification on this machine: all three standalone sources compiled with Tectonic to single-page PDFs, then rendered to PNG; the PNGs were checked against those compiled PDFs and visually compared with the book. All resistor/source labels in Figure 1.11, its accented caption, hollow terminals, and the other figures' annotations were inspected. A local preview using GitHub's Markdown renderer was browsed from the main README through the gallery and all five pages, including expandable captions and return navigation; all five gallery images loaded. Relative links, caption consistency, and preservation of the earlier source/PNG pairs were checked. Working references, temporary PDFs, and review helpers remain outside versioned content.

The separate output-stage/preferences discussion remains as recorded above. This gallery approval does not authorize preserving that trial or implementing the proposed shared-preferences layer. Next: user review of the gallery and the three new drawings, then further reference collection.

<a id="general-preferences-implementation"></a>

## 08-11-2026 - General preferences and automatic agent suggestions

**Status:** implementation explicitly authorized; foundation implemented and checked, corrected drawing delivered. A later visual-bank extension remains a proposal.

The user approved the shared-preferences proposal: "Okay. I agree. You can go ahead and do that." They asked whether corrections to the same concrete example can continue while the workflow is developed, and whether suggestions require manual invocation. The intended behavior is to keep the same example open across corrections and activate suggestions automatically whenever an agent uses the updated Schematica guidance. This is task-driven review, not an unattended background process or a claim about agents without the updated files.

The foundation adds `preferences/GENERAL.md`, establishes task request > explicit style exception > accepted shared default, and accepts G-SYMBOL-01 for supply arrows versus hollow signal ports. Agent instructions, the collection index, the AOE guide, the existing example workflow, and the example-record format route to those defaults, retain decision scope, and separate inactive suggestions from accepted rules. The user can keep working without naming a preference-building mode. Useful generalizations are proposed for review; local adjustments do not silently become universal rules. Saving a rule and publishing an example remain separate decisions.

The output-stage source was corrected to restore four supply-arrow connections while retaining two hollow black signal ports and 9 pt values. Its PDF compiles to one page, all labels and value counts remain present, and the terminal counts were checked. The source and diagram exports remain working artifacts outside the permanent collection.

During this work the user requested a more visual bank: every preference must be documented for agents and shown visually for humans, including README illustrations and optional two-picture before/after or good/bad comparisons. They want ordinary drawing/correction sessions to develop the bank cleanly without repeated special invocation. The proposed extension is a visual preference gallery with one focused card/record per preference, linked evidence and comparison images, clear draft/accepted states, and agent-managed deduplication, links, and rule conflicts. Its organization and standing capture authorization are being proposed, not silently implemented.

Validation: two independent read-only tasks used the updated guidance. One correctly kept supply arrows while changing signal terminals and kept the accepted 9 pt value size local to the figure. The other correctly applied a style exception only to supply symbols, a current-task exception only to the output port, and left the remaining shared defaults intact. Both treated new inferred lessons as inactive pending scoped approval. They found stale checkpoint wording and a missing decision anchor during concurrent editing; both were corrected before handoff. Markdown routes/anchors, simple frontmatter fields, and implicit-invocation metadata were checked directly. The bundled format validator could not run because PyYAML was unavailable; no installation or application-wide availability is claimed. The circuit was compiled and visually checked, and its delivered ZIP was replaced with the corrected version.

Proposed visual-bank layout: `preferences/README.md` is the human gallery; each preference has a focused folder and README holding the one authoritative rule, scope, decision status, visible example/comparison, and evidence links. `preferences/GENERAL.md` would become the agent index and precedence guide rather than duplicate card text. The existing accepted terminal rule would migrate into the first card; no GND convention would be invented before the user supplies/selects examples. Draft suggestions stay visibly separate from accepted guidance, with selective before/after assets and links back to the source circuit. This extension remains unapproved.

<a id="transparent-presentation"></a>

## 08-11-2026 - White backgrounds in chat and GitHub

**Status:** user-reported presentation defect confirmed; repair proposed, implementation pending.

The user supplied screenshots showing white rectangles around the new figures in dark chat and GitHub views and asked for the cause and remedy. All five saved PNGs were checked: RGB, white background, no transparency. The export used `alpha=False`, and both chat and READMEs embedded those same files. The earlier browsing verification established working images and links, not compliance with seamless theme-aware presentation.

The proposed repair preserves editable LaTeX and downloadable PNGs while deriving transparent SVG presentation assets. Drawing lines, text, dots, and arrows must also contrast with the active theme; transparency alone would leave dark ink on a dark page. Use the chat's theme-aware inline presentation and GitHub light/dark image selection, verifying actual theme behavior in both places. GitHub documents `<picture>` with `prefers-color-scheme`; the implementation must test the selected site theme as well as the system theme. Update browsing embeds and rendering checks for all five examples after authorization. This proposal does not change circuit content, approve the recreations, or implement the repair.

Follow-up clarification: the user correctly recalled that transparent, theme-aware SVG in chat is already agreed; embedding PNGs there was an implementation mistake, not a new format decision. GitHub's display format remains under discussion. Paired transparent light/dark PNGs are viable, but the assistant recommends SVG variants for these vector line drawings because labels and geometry remain sharp when resized or zoomed. Retain one ordinary PNG per example for easy downloading and reuse, keep LaTeX authoritative, and generate display variants from that same source. This recommendation is not approval to standardize or implement the GitHub asset change.

<a id="visual-preference-bank"></a>

## 08-11-2026 - First visual preference: supply symbols

**Status:** visual bank and first preference page explicitly authorized, implemented, and checked locally; user review of the illustration and remote synchronization remain pending.

The user approved the visual-bank proposal and selected the supply-arrow correction as its first entry. The bank is linked from the main README. `preferences/README.md` provides human browsing; `preferences/GENERAL.md` owns precedence, the agent index, and inactive suggestions; the authoritative wording of G-SYMBOL-01 moved to `preferences/supply-and-signal-terminals/README.md` without changing its accepted scope or identifier. The new page includes before/after images, evidence and exclusions, source links, and return navigation.

The visuals are newly drawn, focused illustrations of the output-stage correction, explicitly labeled as reconstructions rather than historical screenshots. In the before panel supply connections incorrectly use circles; in the after panel they use arrows. Signal I/O circles are identical. This isolates the rejected feature without publishing the full output-stage circuit or declaring every aspect of its earlier revision wrong. Arrow direction is illustrative, not a new sign-to-direction rule; no GND-symbol or numerical typography preference was added.

One editable LaTeX source generates the two panels and their comparison. Derived transparent PNGs and light/dark/adaptive SVGs support inspection and display. The new preference pages follow the shared presentation procedure, using paired links with GitHub theme fragments to select SVG variants. This change covers the authorized new preference assets only; the five book examples were handled separately.

Agent entry points and the existing example workflow now read applicable preference pages, preserve one authoritative rule, and maintain gallery/index/evidence links. A dedicated record guide covers supplied image pairs, selected revisions, focused reconstructions, explicit status, and scoped approval. Ordinary drawing and corrections continue to trigger suggestions automatically; active defaults remain separate from local edits and unapproved candidates.

Verification: the editable source compiled to a single-page PDF. The agent inspected the light and dark SVG renders: labels fit, hollow signal terminals stay intact, and the isolated change is the supply-circle replacement. Automated checks passed for eight guidance/gallery documents, 62 local links and anchors, nine well-formed SVGs, three transparent RGBA PNGs, equal comparison-panel dimensions, and skill frontmatter; `git diff --check` passed. The headless browser failed to launch because of environment permission errors, so live chat/GitHub theme selection and click navigation are not claimed as verified. The earlier fresh-agent tests covered shared-rule inheritance and local-versus-general correction handling; a new independent behavior test was not run for this visual-bank extension.

<a id="existing-solutions"></a>

## 08-11-2026 - Existing solutions for Schematica's broader goals

**Status:** user-requested research completed at documentation level. All integration choices, architecture and pilots below are assistant proposals, not approved implementation or product direction. No candidate was installed, exercised, benchmarked, or proven compatible with current drawings.

**Scope and evidence:** the user asked to explore existing solutions useful for Schematica's goals. Read the current project direction, checkpoint, earlier graphical-editor review, preference index and presentation procedure. Consulted primary project documentation and repositories on 08-11-2026. Schematica's target covers circuits, conceptual diagrams, waveforms, plots, equations, image/sketch inputs and consistent agent-led preferences. The reviewed checkout has guidance, examples and an SVG export helper; no general-purpose editor or shared circuit-document adapter was established. Existing presentation work uses LaTeX/PDF and PyMuPDF SVG export, so replacing that pipeline is not a prerequisite.

### Comparison criteria

Candidates need a concrete role in the current direction, inspectable documentation, and a credible local/library/file integration route. Assess editable CircuitikZ compatibility, preservation of component identities/values/connections, visual preferences, headless use, dependencies, and ongoing adapter maintenance. A documented role is not proof of a working Schematica integration. Effort ratings are relative engineering judgments: low means a focused wrapper/template, medium adds mapping and validation, high introduces a document/layout subsystem. They are not calendar or cost quotations.

### Candidate pool

Twelve distinct tool families were compared. Designer and its VisioCirkit fork count as one family rather than padding the pool. Ten can supply supporting capabilities without replacing CircuitikZ as the final renderer; Schemdraw and netlistsvg are separately identified as alternative SVG paths. None is a verified drop-in integration.

| Candidate and primary source | Documented capability and proposed use | Effort / cost drivers | Disposition and limitations |
| --- | --- | --- | --- |
| [CircuiTikZ-Designer](https://github.com/Circuit2TikZ/CircuiTikZ-Designer) / [VisioCirkit](https://github.com/StockCurves/VisioCirkit) | Visual editing, components and TikZ/SVG exports. VisioCirkit adds code/canvas synchronization, reusable symbols and agent utilities. Start with a companion editor on disposable copies. | Medium for a limited adapter; high for reliable existing-document support. Browser/Node dependencies and parser maintenance. Repositories display GPL-3.0. | Shortlist for human corrections. VisioCirkit warns that applying code rewrites it and removes comments. Arbitrary macros, relative coordinates and native source formatting cannot be assumed to survive. Designer export alone does not establish TeX import. |
| [Lcapy schematics](https://lcapy.readthedocs.io/en/stable/schematics.html) and [analysis overview](https://lcapy.readthedocs.io/en/stable/overview.html) | Netlist plus placement hints produces CircuitikZ. The same supported circuit model can drive symbolic analysis and annotated figures. | Medium: Python/SymPy/TeX plus style and component mappings. [Repository](https://github.com/mph-/lcapy) displays LGPL-2.1. | Shortlist for structured generation. Layout needs directional hints. Symbolic analysis is for linear time-invariant circuits; drawing a transistor does not mean it can analyse its nonlinear behavior. Not a universal model for every integrated illustration. |
| [PGFPlots](https://github.com/pgf-tikz/pgfplots) / [package description](https://www.ctan.org/pkg/pgfplots?lang=en) | Data/function plots with axes and logarithmic scales inside TeX/TikZ. Compose frequency or time plots beside a circuit using shared figure styling. | Low for templates and data inputs; compilation cost grows with data volume. CTAN identifies GPL-3.0-or-later. | Shortlist for integrated figures. It renders supplied data/functions; it is not a simulator. No new plot preference is adopted by this recommendation. |
| [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) | Screenshot baselines and differences. Render existing SVG fixtures in controlled light/dark browser pages and compare changes. | Low-medium; maintain pinned browser/fonts/rendering environment and approved baselines. | Shortlist for protecting examples and preferences. Reports visual changes, not whether a circuit or aesthetic choice is correct. Use independent structured connection/value checks; approve new baselines deliberately. |
| [ELK / elkjs](https://github.com/kieler/elkjs) / [layered algorithm](https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-layered.html) | Computes node and wire-bend positions with ports, hierarchy and orthogonal routing. Map functional blocks and terminals to a graph, then emit TikZ coordinates. | High for robust schematic use: circuit graph, pin constraints, orientation and layout-to-TikZ adapter. [License](https://github.com/kieler/elkjs/blob/master/LICENSE.md) is EPL-2.0. | Shortlist as a later layout experiment. It does not render symbols or understand the selected book style. Prefer block diagrams first; automatic graph placement is not evidence of good analog schematic composition. |
| [libavoid](https://www.adaptagrams.org/documentation/libavoid.html) | Routes orthogonal/polyline connectors around obstacles; useful when a person moves a component while keeping the rest fixed. | Medium-high; C++ integration or a separately vetted binding, pin/obstacle extraction and junction rules. | Pair with later layout/editor work. Routing and placement are separate jobs. Do not imply libavoid is bundled into elkjs; [ELK's integration](https://eclipse.dev/elk/blog/posts/2022/22-11-17-libavoid.html) is separate. Connectivity must come from the document, not inferred wire intersections. |
| [WaveDrom](https://github.com/wavedrom/wavedrom/blob/trunk/README.md) / [tutorial](https://wavedrom.com/tutorial.html) | WaveJSON descriptions generate digital timing SVGs with clocks, data and events. | Low for standalone SVG; medium for unified figure typography and composition. | Useful optional digital-timing capability. Separate renderer/source format; PGFPlots is a closer first fit for current analog and TeX-integrated work. |
| [Heaviside](https://github.com/whileman133/Heaviside) | Desktop circuit editor, versioned .hv source, actual pdflatex preview and refreshed TeX/PDF/PNG exports. | Medium: .hv adapter, Python/PySide6/TeX and style mapping. Main project MIT; dependencies are separate. | Alternative to the browser editor if offline desktop work becomes the priority. Describes itself as work in progress. Arbitrary existing TeX import was not established. |
| [KiCad CLI](https://docs.kicad.org/9.0/en/cli/cli.html) | Schematic netlist/SVG export and electrical rule checking. Can supply real design connectivity to a publication-figure adapter. | Medium-high: symbol and field mapping, netlist import, selected-sheet handling and presentation layout. | Later EDA import route. SVG export alone gives a KiCad drawing, not an editable CircuitikZ recreation. ERC applies to the KiCad source, not arbitrary TikZ. |
| [Penrose overview](https://penrose.cs.cmu.edu/docs/ref) / [constraints](https://penrose.cs.cmu.edu/docs/ref/constraints) | Separates diagram content from reusable style programs and optimizes geometric constraints. Could inform or power label spacing, containment and arrangement. | High: domain/style definitions and geometry-to-TikZ adapter; optimization behavior needs testing. [Repository](https://github.com/penrose/penrose) is MIT. | Strong research direction for executable visual preferences, lower immediate payoff than rendering checks. It does not automatically convert prose preferences into correct constraints or offer a verified CircuitikZ round trip. |
| [Schemdraw](https://schemdraw.readthedocs.io/en/stable/usage/start.html) | Python component placement with SVG and other image output; image bytes can be embedded in an app. | Low for standalone drawing, high if trying to match the existing TeX assets and styles. | Conditional alternative SVG renderer. Useful for Python/notebook deployments, but a second symbol/rendering stack adds work while editable TikZ remains central. No CircuitikZ export was established by reviewed docs. |
| [netlistsvg](https://github.com/nturley/netlistsvg) | JSON netlist to SVG using configurable symbol skins and ELK; includes analog and digital examples. | Low-medium for previews; higher for Schematica-specific symbol styling and exporting editable TeX. Main repository MIT. | Conditional alternative preview path or digital/block prototype. Its editable input is a netlist/skin, not CircuitikZ; using it as the final renderer would add a separate visual system. |

### Especially reusable pieces

VisioCirkit's [sch2tikz utilities](https://github.com/StockCurves/VisioCirkit/blob/main/.agents/skills/sch2tikz/README.md) include pin-offset lookup data, a compatibility linter, and an overlay/side-by-side comparison generator. These could be more immediately useful than embedding the whole application. Their documentation limits the editor-compatible syntax, including absolute coordinates. Its compilation helper calls QuickLaTeX; any adaptation should deliberately choose its rendering service or use Schematica's existing local compiler. The image-to-TikZ workflow is agent-assisted, not proof of error-free circuit recognition. Reuse must retain applicable notices and inspect dependencies; the listed license identifiers are observations, not a redistribution assessment.

### Proposed priorities and boundaries

1. **Graphical correction:** pilot VisioCirkit's supported syntax and utilities on copies. Its useful advantage is the human/agent editing loop; its major risk is source or circuit information loss.
2. **Structured generation:** pilot Lcapy for simple circuits so components, values and nets can be checked independently from appearance. Keep the current free-form TikZ route for conceptual or unsupported content.
3. **Integrated figures:** add a small PGFPlots-based example with data, circuit labels and styles tied to one parameter source. This has lower integration effort than a new renderer.
4. **Visual consistency:** treat selected accepted examples as Playwright comparison fixtures in both themes. Differences require interpretation; supplement image tests with explicit assertions for supply arrows, signal terminals, values and graph connectivity where represented.
5. **Layout assistance later:** try ELK on functional blocks, and libavoid for routing around fixed objects, after a structured document exists. Penrose remains a separate higher-effort style/constraint experiment.

Suggested architecture: retain Schematica's accepted preferences and example bank as authoritative guidance; introduce optional structured components/nets/layout only for supported drawings; call adapters for rendering, analysis, layout and visual comparison. Use stable component/terminal IDs and revision checks for GUI edits. Unsupported source must remain intact or cause an explicit rejection. Compiled SVG paths are display artifacts and cannot by themselves recover electrical semantics. A future agent-facing wrapper can expose these operations, but no framework, MCP server, application frontend or replacement master format is selected here.

### Proposed smallest useful pilot

Use a disposable native-component voltage divider and a copy of the existing output-stage trial. For the divider, compare current direct CircuitikZ generation with Lcapy, include one data-driven plot, and record the adapter limitations. For the editor, measure no-edit import/export changes, move a label and component, save/reopen, and perform another agent edit. Require unchanged IDs, values, terminal connectivity and accepted supply-arrow/signal-circle conventions. Check final LaTeX output and transparent light/dark SVG display, source/comment losses, undo and stale edits. Keep traced book figures outside initial semantic-import claims. Report which path saves effort and which content it cannot preserve before choosing an implementation.

### Verification and synchronization limits

The reviewed primary documentation supports the capability descriptions; effort and ranking are assistant judgments. No runtime behavior, compiler/package compatibility, layout quality or end-to-end import was tested. Some package metadata pages were unavailable; no release recency or project-wide license compatibility is claimed. Research stopped after the relevant candidate pool and five integration priorities were supported. Existing uncommitted drawing/preference changes were preserved. A remote-state check failed with a Git name-resolution error, so this review could not establish current synchronization. Only this research checkpoint is in scope for routine context saving.

Verification: the editable source compiled to a single-page PDF. The agent inspected the light and dark SVG renders: labels fit, hollow signal terminals stay intact, and the isolated change is the supply-circle replacement. Automated checks passed for eight guidance/gallery documents, 62 local links and anchors, nine well-formed SVGs, three transparent RGBA PNGs, equal comparison-panel dimensions, and skill frontmatter; `git diff --check` passed. The headless browser failed to launch because of environment permission errors, so live chat/GitHub theme selection and click navigation are not claimed as verified. The earlier fresh-agent tests covered shared-rule inheritance and local-versus-general correction handling; a new independent behavior test was not run for this visual-bank extension.

<a id="svg-presentation-complete"></a>

## 08-11-2026 - SVG presentation approved, implemented, and checked

**Status:** explicitly authorized; implemented and pushed in `e1f7da4`; light/dark presentation checked. User review of the three newer recreations remains pending.

The user authorized: "Update all five examples, keep the PNGs, and document SVG as the default for chat and GitHub. Check both themes, push the changes, and show me the three new examples inline again." This supersedes the pending repair above and establishes SVG as the GitHub display default as well as the already agreed chat default.

All five examples now have transparent `preview-light.svg` and `preview-dark.svg` generated from their freshly compiled LaTeX. Root, gallery, and example pages display the appropriate SVG; PNG and source downloads remain available. Agent instructions, direction, style/index, and collection records/workflow document the default and checks. [The export and presentation procedure](../scripts/PRESENTATION.md) supplies the repeatable command and embedding convention. The helper supports monochrome vector figures and rejects raster or extra-color inputs requiring deliberate mapping.

Verification: all five sources compiled successfully. Exported vector geometry matches the unmodified PDF-to-SVG output; light and dark variants differ only in ink. SHA-256 checks confirm all five LaTeX and five original PNG files stayed byte-for-byte unchanged. Local light/dark gallery renders and 192 relative asset/navigation links passed. The three requested inline figures were inspected in both themes using the chat presentation runtime's standalone preview.

Live GitHub verification showed all five dark SVGs loaded in automatic dark mode and all five light SVGs loaded with an explicit light site theme while the system remained dark. Backgrounds are transparent, labels/captions remain readable, and exactly one version is shown per figure. GitHub's theme fragments are placed on image links to follow its site setting. Main README-to-gallery, gallery-to-example, PNG access, and return navigation were exercised. The original automatic theme with default light/dark palettes was restored. This verification covers The Art of Electronics gallery, not the concurrently developed preference gallery.

No drawing geometry, technical content, original captions, or provisional style patterns were changed. Screenshots, compiler output, and chat-preview wrappers remain working artifacts outside versioned example content. Review the three figures in chat, then continue the collection or practical trial within the user's chosen scope.

<a id="collection-resumed-after-svg"></a>

## 08-11-2026 - Resume The Art of Electronics collection

The user said the revised inline presentation "looks good" and chose to resume building The Art of Electronics style by sending more examples. This records positive visual feedback on the displayed result; it does not make every drawing detail a general style rule. Continue the existing collection workflow: preserve supplied captions and explicit comments, treat uncommented references as liked overall, and distinguish observations from confirmed preferences. No new reference or recreation was supplied in this message.

<a id="preference-gallery-refinement"></a>

## 08-11-2026 - Preference gallery and agent behavior proposal

**Status:** user feedback and requested proposal recorded; reorganization, new rule pages, gallery generation, and workflow changes are proposed, not implemented or approved for execution.

The user wants READMEs to contain minimal useful human-facing information. Move the Developing the bank instructions out of the gallery; explain and hide internal rule identifiers/status from visual browsing. Split supply arrows and hollow signal terminals into independent rules with simple titles, such as Power supply arrow symbols and Input/output terminal circles. Good examples are required, bad examples optional; show good/bad rather than before/after. Each rule should have a human README and agent RULE file. Categories should incorporate their individual rule READMEs; a category containing child categories should show one representative example and link per child. More than eight entries is a prompt to consider useful subcategories, not a reason to invent empty categories.

Assistant proposal: create `agents/BEHAVIOR.md` as the authoritative expected-behavior guide, routed from root `AGENTS.md`; existing drawing/save procedures link it without repeating its requirements. It would hold natural suggestion behavior, local-versus-general scope, approval boundaries, organization guidance, and the eight-entry review threshold. Keep `preferences/GENERAL.md` for agent selection, precedence, and inactive proposals. Start `preferences/symbols/` with separate `power-supply-arrows/` and `signal-terminal-circles/` records. Each leaf README has a short descriptive title, good visual, optional bad comparison, at most a useful explanatory sentence, and minimal navigation. RULE owns the precise instruction, applicability, exceptions, stable identifier/status, evidence, and example links. Preserve the old combined rule's provenance while updating references after the split.

Generate parent gallery sections from the authored individual README example content, adjusting headings and relative links rather than maintaining manual copies. Leaf categories include all direct rule cards; parent categories include only one representative good image and link for each immediate child. Main README's Preferences section exposes category navigation. Keep drafts out of the accepted gallery, retain user-supplied comparison provenance, and preserve explicit style exceptions. Proposed execution: migrate the first two rules and their assets, update entry points and procedure references, add gallery regeneration/checking, verify source/examples/navigation/themes, then commit and push. Estimated 20-30 minutes after approval; stop with the revised gallery ready for review. No new GND convention or broader circuit redraw is proposed.

<a id="preference-proposal-review"></a>

## 08-11-2026 - Preference proposal review: behavior and maintenance

**Status:** user requested answers and a revised plan before implementation. Agreement on individual design choices does not authorize executing the migration yet.

The user asked whether AGENTS.md should move into the proposed Agents folder; agreed to separate rules and README/RULE files; suggested green/red good/bad headings or check/cross symbols; and directed that behavior means interaction with the user in chat. Category hierarchy and repository maintenance must be documented separately as project rules. The user also requested a plain explanation of the gallery script and when it runs.

Revised assistant proposal: retain a short root `AGENTS.md` for discovery and explicit reading routes. Put chat communication, corrections, and suggestion interaction in `agents/BEHAVIOR.md`; put README/RULE responsibilities, category aggregation, eight-entry subdivision review, synchronization, and maintenance checks in root `PROJECT_RULES.md`. Existing detailed procedures reference these authoritative instructions rather than duplicating them. For visuals, start with green check/red cross plus Good/Bad text, preserving a usable label independent of color, and review the actual rendering during implementation.

The proposed gallery builder reads the designated visual content of individual rule READMEs, includes accepted rules with a good illustration, rewrites headings and relative links for the containing page, and updates only marked generated sections. Rule categories include their rule cards; higher levels use one selected good preview and link per immediate subcategory. Agents choose categories and representative examples; the builder assembles those choices. Run it after an approved rule/example/category edit and before link/theme checks and commit. A check mode reports stale sections or broken/missing references without changing files. It is a task step, not a scheduled job or continuously running service. Illustrative example: edit the supply-symbol caption once, then rebuild the Symbols page and any parent section displaying that representative preview. The revised migration remains estimated at 20-30 minutes after approval.

<a id="gallery-builder-clarification"></a>

## 08-11-2026 - Folder tree and gallery builder clarification

**Status:** discussion and revised proposal only; no organization migration or gallery script is authorized or implemented.

The user asked for the exact location of project rules, required folder trees when proposing files/organization (already specified in personal preferences), and asked whether gallery maintenance means deterministic code or agent judgment. Revised proposed location: `agents/PROJECT_RULES.md` beside `agents/BEHAVIOR.md`; retain root `AGENTS.md` as entry point. The existing personal folder-tree preference was read; no duplicate preference or personal-instruction edit is needed.

Point five proposes one deterministic Python file, `scripts/build_preference_galleries.py`, using the saved folder structure and individual rule README visual sections to regenerate marked category/main README gallery sections. It adjusts relative links/headings, uses selected representative good examples for category previews, preserves content outside generated sections, and provides a read-only check mode for stale outputs or missing required assets. The agent runs it after an approved rule/example/category edit before validation and commit. It has no LLM call or organizational judgment. The existing agent workflow reviews whether more than eight entries warrant subcategories, proposes names/groupings and representative examples, obtains applicable approval, and then updates the structure and runs the builder. This does not propose a second autonomous organization system, new scheduled task, or always-running service.
