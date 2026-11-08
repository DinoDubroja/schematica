---
name: schematica-examples
description: Start or resume an electronics illustration style collection from books, screenshots, or generated work. Add examples and captions, capture feedback, and consolidate style patterns. Also use during Schematica drawing reviews to offer to preserve useful generated examples or corrections. Does not make an unrequested drawing or approve publication merely because a result is liked.
---

# Schematica examples

Turn supplied examples and ordinary drawing feedback into a reusable style collection. Support a new source as readily as an existing collection; The Art of Electronics is the first collection, not a special case in this workflow.

## Find the collection in a fresh chat

Resolve this skill directory to its physical location first if it is installed through a symlink or Windows junction. The Schematica repository is two levels above that physical directory. For example, Python's `Path(skill_file).resolve().parents[2]` finds it from `SKILL.md`. Relative links below refer to that physical location, not the installed alias.

Read the repository's [AGENTS.md](../../AGENTS.md) and [examples/INDEX.md](../../examples/INDEX.md). Match the user's full source/style name to a collection. Read its `STYLE.md`, including status and next steps, then only example records needed for the request. Do not require the old chat to resume.

If the user explicitly selects another Schematica checkout, use that checkout after verifying its index. If no repository can be located, ask for the checkout rather than silently creating a second library. Never put user examples inside the installed skill directory.

## Establish scope once

Identify whether the user wants to collect, discuss, recreate, use, review, or save an example. Follow existing explicit authorization. An explicit request to create or save a sufficiently identified collection/example permits that work; do not ask for the same approval again.

If the destination or save scope is not established, propose the collection and what will be saved once. An authorized collection session can save incoming examples, supplied captions, explicit feedback, and index updates without prompting for every item. Drawing recreations, wider revisions, and unrelated publication remain subject to the actual authorized scope.

Discussion, proposed wording, praise, silence, and a collection's saved status do not independently authorize changes. On resume, recover content and next steps from files; assess authorization from the current request and relevant established instructions.

## Start or add to a collection

1. Reuse a matching collection if one exists. Otherwise use a readable full name for `examples/<COLLECTION>/`, such as `THE_ART_OF_ELECTRONICS`. Create only the needed files.
2. Create or update `STYLE.md` with purpose, source, collection status, confirmed preferences, provisional patterns, an example guide, unresolved questions, and the next useful step. Add its link and selection cues to `examples/INDEX.md`.
3. Give each example a stable descriptive folder name. For a numbered source figure, use a name such as `fig-01-07-adjustable-divider`; for new generated work, use the subject rather than a book figure number. Check for duplicates before adding.
4. Follow [the example record format](references/example-record.md). Save `EXAMPLE.md` with the original supplied caption, source reference, a description, user feedback, inferred lessons, and accurate asset/review status. Preserve important associated explanations with clear attribution.
5. Screenshots and original PDFs are working references. Do not commit them as finished drawings or establish a separate permanent screenshot archive by default. Captions are repository content, alongside the example. Source information should identify the work and figure without depending on a private machine path.
6. When a recreation is authorized and ready, keep `drawing.tex` and `preview.png` together. Compile and inspect the rendered figure, preserve technical meaning, and verify that the preview represents the saved source. Do not claim a visual recreation is a reusable semantic CircuitikZ implementation unless it actually is.
7. If no recreation exists, save the caption and feedback record with recreation marked pending. Do not fabricate a preview, broken asset link, or visual approval. Tell the user which material remains unavailable for visual use.
8. Update the style's example guide and current next steps. Report what was captured briefly, including what remains pending.

When examples are submitted to this workflow without additional comments, record that the user likes the example overall. Specific praise identifies a feature; it does not approve every detail as a general rule. Preserve explicit comments separately from inferred observations.

## Review and consolidate a style

Collection and consolidation are separate activities. Adding examples does not require finishing a style. When asked to review the collection:

- Compare relevant examples, identifying recurring choices, meaningful exceptions, and each example's additional contribution.
- Put shared guidance in `STYLE.md`; keep detailed captions and feedback with the examples. Link every inferred pattern to supporting examples where useful.
- Keep candidate rules labelled provisional until confirmed. State coverage gaps instead of extending a few examples into unsupported book-wide claims.
- Propose the next targeted example or a new practical drawing to test the style. After user review, record the resulting state and next step so another chat can continue.

The index chooses styles; the style guide chooses examples. Avoid loading all collections, source files, and previews on routine tasks. Actually inspect selected images when visual comparison is needed.

## Preserve a generated example

During ordinary Schematica work, notice clear positive feedback, a useful correction, or a result demonstrating a new capability. When preservation would help future work, offer once to save the specific result and lesson, naming the destination and useful context. Do not offer every routine output, repeat a declined offer, or label an unreviewed result good.

If the user already explicitly asks to save the result, carry out that request without a second permission question. Otherwise wait for approval before saving. An approval to retain one result does not authorize unrelated style changes.

Save the final source and preview with an `EXAMPLE.md` containing:

- The task prompt and relevant inputs, preserving exact wording when available and useful; label reconstructions as summaries.
- The style and reference examples used, with a repository revision when available.
- The user's feedback, the accepted result, and what it adds to the collection.
- Selected corrections or intermediate versions that demonstrate a reusable lesson, when included in the approved scope.

Use `Origin: generated` for a new illustration, even if it uses a reference style. A faithful recreation of an external figure retains `Origin: reference`. Keep origin separate from review status.

For an instructive intermediate version, state precisely what was deficient and how it changed. Do not declare every aspect of a version bad. Store complete source and preview files for selected revisions under `iterations/<descriptive-version>/` when needed, and explain them in the main example record. Do not save every iteration automatically. Difference-only storage is not implemented.

Preserve relevant prompt/feedback context rather than copying entire private chats. Use repository-relative links for saved assets. Update the style's example guide with the new contribution; propose any new general rule separately unless its adoption was explicitly authorized.

## Finish the authorized save

- Read the saved records back. Check captions, attribution, links, asset availability, review status, and the index-to-style-to-example reading path.
- Confirm new screenshots, temporary PDFs, build output, and unrelated material have not entered the repository.
- Keep source and preview synchronized. If only metadata changed, do not redraw an already accepted figure unnecessarily.
- Follow repository instructions for checks, commits, and pushes within the approved scope. Report any limitation, including whether fresh-chat discovery and real drawing behavior have actually been tested.
