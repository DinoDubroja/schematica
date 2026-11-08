---
name: schematica-examples
description: Use whenever creating, editing, or reviewing a Schematica illustration, and when starting or resuming an electronics example collection. Apply shared preferences and explicit style exceptions, collect references, track corrections, and proactively suggest reusable general or style-specific lessons. Suggestions are automatic within Schematica use; saving active rules or example assets requires the user's scoped approval. Does not authorize unrequested drawings or publication merely because a result is liked.
---

# Schematica examples

Turn supplied examples and ordinary drawing feedback into a reusable style collection. Support a new source as readily as an existing collection; The Art of Electronics is the first collection, not a special case in this workflow.

## Find the collection in a fresh chat

Resolve this skill directory to its physical location first if it is installed through a symlink or Windows junction. The Schematica repository is two levels above that physical directory. For example, Python's `Path(skill_file).resolve().parents[2]` finds it from `SKILL.md`. Relative links below refer to that physical location, not the installed alias.

Read the repository's [AGENTS.md](../../AGENTS.md), [general preference index](../../preferences/GENERAL.md) and applicable `RULE.md` files/README visuals, then [examples/INDEX.md](../../examples/INDEX.md). Match the user's full source/style name to a collection. Read its `STYLE.md`, including explicit exceptions, status and next steps, then only example records needed for the request. General preferences apply even without a named style. Follow their precedence and treat inferred/proposed rules as inactive. Do not require the old chat to resume.

If the user explicitly selects another Schematica checkout, use that checkout after verifying its index. If no repository can be located, ask for the checkout rather than silently creating a second library. Never put user examples inside the installed skill directory.

## Scope and corrections

Follow [chat behavior](../../agents/BEHAVIOR.md) for authorization, continuing one
example through corrections, and when to suggest preservation. Identify whether the
task is collecting, discussing, recreating, using, reviewing, or saving. An authorized
collection session covers its incoming references, captions, feedback, and index
updates; recreations and broader publication depend on the actual approved scope.

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
2. Record pending/deferred/rejected proposals there with existing evidence links, or
   retain discussion in authorized context. Keep their actual decision status.
3. Save approved general guidance using [the preference record procedure](references/preference-record.md).
   Put named-style rules/exceptions in `STYLE.md` and local feedback in `EXAMPLE.md`
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

1. Reuse a matching collection if one exists. Otherwise use a readable full name for `examples/<COLLECTION>/`, such as `THE_ART_OF_ELECTRONICS`. Create only the needed files.
2. Create or update `STYLE.md` with purpose, source, collection status, confirmed preferences, provisional patterns, an example guide, unresolved questions, and the next useful step. Add its link and selection cues to `examples/INDEX.md`. Maintain a separate collection `README.md` for human browsing: a short introduction and clickable previews with titles and one-line descriptions. Link the main README to this gallery, keeping detailed guidance in `STYLE.md`.
3. Give each example a stable descriptive folder name. For a numbered source figure, use a name such as `fig-01-07-adjustable-divider`; for new generated work, use the subject rather than a book figure number. Check for duplicates before adding.
4. Follow [the example record format](references/example-record.md). Save `EXAMPLE.md` with the original supplied caption, source reference, a description, user feedback, inferred lessons, and accurate asset/review status. Preserve important associated explanations with clear attribution.
5. Screenshots and original PDFs are working references. Do not commit them as finished drawings or establish a separate permanent screenshot archive by default. Captions are repository content, alongside the example. Source information should identify the work and figure without depending on a private machine path.
6. When a recreation is authorized and ready, keep `drawing.tex`, `preview-light.svg`, `preview-dark.svg`, and `preview.png` together. Compile and inspect the rendered figure, preserve technical meaning, and verify that the preview represents the saved source. Add an example `README.md` showing the appropriate SVG immediately, a brief useful description, original caption/source information, and links to both SVGs, the PNG, LaTeX, detailed record, and collection gallery. Long captions may be expandable but remain in the repository. Use the [presentation procedure](../../scripts/PRESENTATION.md): SVG is the default in chat and GitHub, with transparent backgrounds and theme-appropriate ink; PNG remains a download. Verify both themes and the source/export match. Do not claim a visual recreation is a reusable semantic CircuitikZ implementation unless it actually is.
7. If no recreation exists, save the caption and feedback record with recreation marked pending in the agent index/guide. Do not present it as a completed gallery example, fabricate a preview, or leave a broken asset link. Tell the user which material remains unavailable for visual use; follow the actual authorization for completing it.
8. Update the style's example guide and current next steps. Report what was captured briefly, including what remains pending.

When examples are submitted to this workflow without additional comments, record that the user likes the example overall. Specific praise identifies a feature; it does not approve every detail as a general rule. Preserve explicit comments separately from inferred observations.

## Review and consolidate a style

Collection and consolidation are separate activities. Adding examples does not require finishing a style. When asked to review the collection:

- Compare relevant examples, identifying recurring choices, meaningful exceptions, and each example's additional contribution.
- Put collection-specific guidance in its `STYLE.md`; route approved cross-style preferences to [general preferences](../../preferences/GENERAL.md). Keep detailed captions and feedback with the examples and link inferred patterns to supporting evidence.
- Keep candidate rules labelled provisional until confirmed. State coverage gaps instead of extending a few examples into unsupported book-wide claims.
- Propose the next targeted example or a new practical drawing to test the style. After user review, record the resulting state and next step so another chat can continue.

The index chooses styles; the style guide chooses examples. Avoid loading all collections, source files, and previews on routine tasks. Actually inspect selected images when visual comparison is needed.

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

- Read the saved records back. Check captions, attribution, links, asset availability, review status, and the index-to-style-to-example reading path. Also check the human path from the main README through the collection gallery to each example, its image/source, and back. Keep public READMEs brief and focused on available work; do not introduce unestablished installation or invocation instructions.
- Check the general-preferences-to-style reading route, explicit exceptions, rule/evidence links, and separation of accepted rules from pending suggestions. Confirm that a local correction has not silently become a universal rule.
- For a visual preference, check main README -> categories -> rule README -> images/source/back links, plus agent index -> RULE.md. Run the gallery builder and its `--check` mode per [project rules](../../agents/PROJECT_RULES.md#deterministic-gallery-generation). Inspect good/bad images at the same scale and in their documented display themes; verify the named difference, preserved technical meaning, and accurate approval/provenance labels. Do not call a text-only placeholder a completed visual preference.
- Confirm new screenshots, temporary PDFs, build output, and unrelated material have not entered the repository.
- Keep source, SVG previews, and PNG synchronized. Check both light and dark presentation, including GitHub's selected site theme. If only metadata or display packaging changed, do not redraw an already accepted figure unnecessarily; preserve unchanged source and PNG files.
- Follow repository instructions for checks, commits, and pushes within the approved scope. Report any limitation, including whether fresh-chat discovery and real drawing behavior have actually been tested.
