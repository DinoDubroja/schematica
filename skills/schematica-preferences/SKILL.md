---
name: schematica-preferences
description: Guide Schematica preferences and example sessions from a topic through in-chat visual options, refinement and approved saves. Use for requests such as "start Schematica Preferences", "work on Schematica's op-amp symbols" or "add this example to Schematica", and when creating, editing or reviewing a Schematica illustration. Apply existing preferences and styles. Scope this workflow to Schematica; general personal preferences and unrelated electronics questions do not activate it.
---

# Schematica Preferences & Examples

Help the user explore a topic, compare visual options in chat, refine a choice and,
when authorized, preserve its preference or example. Follow the
[guided session behavior](../../agents/BEHAVIOR.md#guided-preferences-sessions)
when starting or resuming exploration. A broad topic calls for a useful suggested
starting point; a concrete request for previews calls for the previews.

Support new source collections as readily as existing ones. The Art of Electronics
is the first collection, not a special case. Ordinary Schematica drawing work also
uses this workflow without requiring a separate preferences session.

## Find the collection in a fresh chat

Resolve this skill directory to its physical location first if it is installed through a symlink or Windows junction. The Schematica repository is two levels above that physical directory. For example, Python's `Path(skill_file).resolve().parents[2]` finds it from `SKILL.md`. Relative links below refer to that physical location, not the installed alias.

Read [chat behavior](../../agents/BEHAVIOR.md), the [general preference index](../../preferences/GENERAL.md) and applicable `RULE.md` files/README visuals, then [styles/INDEX.md](../../styles/INDEX.md). Match the user's full source/style name to a collection. Read its `STYLE.md`, including shared guidance, explicit exception links, status and next steps, then the applicable domain guides it links and only example records needed for the request. Select domains independently; a mixed circuit/waveform task may need both schematic and plot guidance. A planned or absent domain guide does not supply rules. General preferences apply even without a named style. Follow their precedence and treat inferred/proposed rules as inactive. Do not require an old chat, personal instruction folder or project-development checkpoint for ordinary use.

If the user explicitly selects another Schematica checkout, use that checkout after verifying its index. If no repository can be located, ask for the checkout rather than silently creating a second library. Never put user examples inside the installed skill directory.

Approved saves belong to that selected library. Follow its organization/validation
rules when saving; installation alone authorizes no context logging, Git operations
or publication. Read the repository's [AGENTS.md](../../AGENTS.md) development route
only when the user is working on the Schematica project itself. Historical project
approvals do not transfer to a downloaded copy or a new user's session.

## Scope and corrections

Follow [chat behavior](../../agents/BEHAVIOR.md) for authorization, continuing one
example through corrections, and when to suggest preservation. Identify whether the
task is collecting, discussing, recreating, using, reviewing, or saving. An authorized
collection session covers its incoming references, captions, feedback, and index
updates; recreations and broader publication depend on the actual approved scope.
Treat saving pictures, choosing showcase highlights, recreating drawings, and
inferring reusable style rules as distinct scopes. An instruction to collect or
organize without style generalization means preserve the examples and explicit
feedback only: do not add inferred lessons, measured defaults, or new rules.
Existing observations keep their prior status.

Record the concrete change, its reason, reviewed revision, and local versus wider
scope. Keep unsaved-example feedback in authorized context notes; consolidate it into
the example record after preservation is approved. Mark superseded interpretations.

<a id="agent-suggestions"></a>

## Agent suggestions

Suggestion interaction is active during ordinary Schematica use as specified in
[BEHAVIOR.md](../../agents/BEHAVIOR.md#corrections-and-suggestions); no separate command
or background service is needed. After discussing a useful lesson:

1. Check accepted rules and the inactive queue in [GENERAL.md](../../preferences/GENERAL.md).
   Classify the destination as general, named style, or current example.
2. Keep pending/deferred/rejected proposals in the conversation unless recording
   them is authorized. Within an authorized collection/context scope, record them
   with evidence links and their actual decision status; no proposed rule is active.
3. Save approved general guidance using [the preference record procedure](references/preference-record.md).
   Put domain-specific style rules/exceptions in the relevant domain guide (linked from `STYLE.md`), shared style guidance in `STYLE.md`, and local feedback in `EXAMPLE.md`
   (or context for an unsaved example). Link evidence in both directions when available.
4. Follow [project rules](../../agents/PROJECT_RULES.md) for category/README maintenance,
   gallery generation, validation, and synchronization. Before delivery, check the
   current request, applicable accepted rules, explicit style exceptions, technical
   meaning, and relevant previews. Propose narrower rules or explicit exceptions when
   counterexamples appear rather than silently weakening existing guidance.

## Build the visual preference bank

Follow [the preference record procedure](references/preference-record.md). Reuse a
matching rule instead of duplicating it. [PROJECT_RULES.md](../../agents/PROJECT_RULES.md#preference-hierarchy)
defines the hierarchy and README/RULE split. Keep accepted preferences stable during
experiments, and leave pending proposals out of accepted galleries.

## Start or add to a collection

1. Reuse a matching collection if one exists. Otherwise use a readable full name for `styles/<COLLECTION>/`, such as `THE_ART_OF_ELECTRONICS`. Create only the needed files.
2. Create or update `STYLE.md` with source, collection status, domain links, inventory, and next step. Create domain guides only when there is actual content. Preserve existing guidance and its review status; infer or consolidate patterns only within the approved analysis scope. Add the collection and available-domain cues to `styles/INDEX.md`. Maintain a short collection `README.md` showcase linking prominently to `examples/README.md` and category galleries. Follow [project rules](../../agents/PROJECT_RULES.md#style-collections) for highlights, subdivision, and minimal human pages; do not load every descendant onto the showcase.
3. Store each example once under `styles/<COLLECTION>/examples/<category>/<example>/`. Choose its main form: `schematics` includes conceptual connection diagrams and circuit comparisons; `plots` holds standalone plots/signals; `mixed` combines circuit, waveform, equation, physical, or block-diagram content. Ordinary component labels and annotations alone do not make a schematic mixed. Keep complete mixed figures together and link them from all relevant guides. Create only categories with content; proposed writing guidance does not justify an empty `writing/` folder. Give each example a stable descriptive folder name. For a numbered source figure, use a name such as `fig-01-07-adjustable-divider`; for new generated work, use the subject rather than a book figure number. Check for duplicates before adding.
4. Follow [the example record format](references/example-record.md). Save `EXAMPLE.md` with the supplied caption, source, description, explicit feedback, and accurate asset/review status. Preserve associated explanations with attribution. Inferred lessons are optional and must respect the task's analysis boundary.
5. When saving the supplied image is authorized, preserve its original bytes as `reference.png` (or the actual original format) in the existing example folder. Create a human `README.md` showing the image directly, a short description, original caption/source, download, notes, category, and showcase links. Use its original background; no transparency, theme conversion, SVG wrapper, or LaTeX is required. Treat this as a complete image reference, not a pending recreation. Check the downloaded file's identity and integrity before updating availability. An inaccessible image remains a text-only record with a concrete blocker, not a broken preview. Do not import entire source PDFs or unrelated screenshots under a single-figure approval.
6. When a recreation is authorized and ready, keep `drawing.tex`, `preview-light.svg`, `preview-dark.svg`, and `preview.png` together. Compile and inspect the rendered figure, preserve technical meaning, and verify that the preview represents the saved source. Add an example `README.md` showing the appropriate SVG immediately, a brief useful description, original caption/source information, and links to both SVGs, the PNG, LaTeX, detailed record, and collection gallery. Long captions may be expandable but remain in the repository. Use the [presentation procedure](../../scripts/PRESENTATION.md): SVG is the default in chat and GitHub, with transparent backgrounds and theme-appropriate ink; PNG remains a download. Verify both themes and the source/export match. Do not claim a visual recreation is a reusable semantic CircuitikZ implementation unless it actually is.
7. If only caption/feedback metadata is available, keep `EXAMPLE.md` and list it in the category's reference notes with image availability explicit. Do not fabricate a visual page or imply that recreation is required. A later authorized image import completes its visual reference; an authorized recreation may be added independently. Keep original and recreated images clearly identified when both exist.
8. Update the inventory, category galleries, relevant selection links, and next steps. Count saved image references, recreations, and records without images accurately; an example with both asset types is still one example. Retain the current showcase unless its selection changes within the approved scope. Report actual completion and blockers.

When examples are submitted to this workflow without additional comments, record that the user likes the example overall. Specific praise identifies a feature; it does not approve every detail as a general rule. Preserve explicit comments separately from inferred observations.

## Review and consolidate a style

Collection and consolidation are separate activities. Adding examples does not require finishing a style. When asked to review the collection:

- Compare relevant examples, identifying recurring choices, meaningful exceptions, and each example's additional contribution.
- Put collection-specific guidance in its owning domain guide, or `STYLE.md` when shared across domains; route approved cross-style preferences to [general preferences](../../preferences/GENERAL.md). Keep detailed captions and feedback with the examples and link inferred patterns to supporting evidence.
- Keep candidate rules labelled provisional until confirmed. State coverage gaps instead of extending a few examples into unsupported book-wide claims.
- Propose the next targeted example or a new practical drawing to test the style. After user review, record the resulting state and next step so another chat can continue.

The index chooses styles; `STYLE.md` selects available domain guides; domain guides select examples. `STYLE.md` keeps the complete inventory. Mixed examples have one record and can be linked from several guides. Avoid loading all collections, source files, and previews on routine tasks. Actually inspect selected images when visual comparison is needed.

## Preserve a generated example

Use [BEHAVIOR.md](../../agents/BEHAVIOR.md) for preservation suggestions and approval boundaries.

Save the final source and preview with an `EXAMPLE.md` containing:

- The task prompt and relevant inputs, preserving exact wording when available and useful; label reconstructions as summaries.
- The style and reference examples used, with a repository revision when available.
- The user's feedback, the accepted result, and what it adds to the collection.
- Selected corrections or intermediate versions that demonstrate a reusable lesson, when included in the approved scope.

Use `Origin: generated` for a new illustration, even if it uses a reference style. A faithful recreation of an external figure retains `Origin: reference`. Keep origin separate from review status.

For an instructive intermediate version, state precisely what was deficient and how it changed. Do not declare every aspect of a version bad. Store complete source and preview files for selected revisions under `iterations/<descriptive-version>/` when needed, and explain them in the main example record. Do not save every iteration automatically. Difference-only storage is not implemented.

Preserve relevant prompt/feedback context rather than copying entire private chats. Use repository-relative links for saved assets. Update the style's example guide with the new contribution; propose any new general rule separately unless its adoption was explicitly authorized.

## Finish the authorized save

- Read the saved records back. Check captions, attribution, links, asset availability, review status, and the index-to-style-to-domain-to-example reading path. Also check the human path from the main README through the collection gallery to each example, its image/source, and back. Keep public READMEs brief and focused on available work; do not introduce unestablished installation or invocation instructions.
- Check the general-preferences-to-style reading route, explicit exceptions, rule/evidence links, and separation of accepted rules from pending suggestions. Confirm that a local correction has not silently become a universal rule.
- For a visual preference, check main README -> categories -> rule README -> images/source/back links, plus agent index -> RULE.md. Run the gallery builder and its `--check` mode per [project rules](../../agents/PROJECT_RULES.md#deterministic-gallery-generation). Inspect good/bad images at the same scale and in their documented display themes; verify the named difference, preserved technical meaning, and accurate approval/provenance labels. Do not call a text-only placeholder a completed visual preference.
- Confirm only the authorized original reference images entered the repository;
  exclude unrelated screenshots, source-book PDFs, temporary exports, and build output.
- For recreations, keep source, SVG previews, and PNG synchronized. For image
  references, verify unchanged original bytes and usable display on both backgrounds.
  Check navigation from showcase through all examples, category, example, and back.
  Review GitHub's selected site themes when accessible and report unverified parts.
  Do not redraw accepted figures for metadata or navigation changes.
- Complete local checks and report the save. Commit, push or update development
  notes only within separately established maintenance/publication authorization.
  Report any limitation, including whether fresh-chat discovery and real drawing
  behavior have actually been tested.
