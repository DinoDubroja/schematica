---
name: schematica-examples
description: Use whenever creating, editing, or reviewing a Schematica illustration, and when starting or resuming an electronics example collection. Apply shared preferences and explicit style exceptions, collect references, track corrections, and proactively suggest reusable general or style-specific lessons. Suggestions are automatic within Schematica use; saving active rules or example assets requires the user's scoped approval. Does not authorize unrequested drawings or publication merely because a result is liked.
---

# Schematica examples

Turn supplied examples and ordinary drawing feedback into a reusable style collection. Support a new source as readily as an existing collection; The Art of Electronics is the first collection, not a special case in this workflow.

## Find the collection in a fresh chat

Resolve this skill directory to its physical location first if it is installed through a symlink or Windows junction. The Schematica repository is two levels above that physical directory. For example, Python's `Path(skill_file).resolve().parents[2]` finds it from `SKILL.md`. Relative links below refer to that physical location, not the installed alias.

Read the repository's [AGENTS.md](../../AGENTS.md), [general preferences](../../preferences/GENERAL.md), and [examples/INDEX.md](../../examples/INDEX.md). Match the user's full source/style name to a collection. Read its `STYLE.md`, including explicit exceptions, status and next steps, then only example records needed for the request. General preferences apply even without a named style. Follow their precedence and treat inferred/proposed rules as inactive. Do not require the old chat to resume.

If the user explicitly selects another Schematica checkout, use that checkout after verifying its index. If no repository can be located, ask for the checkout rather than silently creating a second library. Never put user examples inside the installed skill directory.

## Establish scope once

Identify whether the user wants to collect, discuss, recreate, use, review, or save an example. Follow existing explicit authorization. An explicit request to create or save a sufficiently identified collection/example permits that work; do not ask for the same approval again.

If the destination or save scope is not established, propose the collection and what will be saved once. An authorized collection session can save incoming examples, supplied captions, explicit feedback, and index updates without prompting for every item. Drawing recreations, wider revisions, and unrelated publication remain subject to the actual authorized scope.

Discussion, proposed wording, praise, silence, and a collection's saved status do not independently authorize changes. On resume, recover content and next steps from files; assess authorization from the current request and relevant established instructions.

## Continue one example through corrections

Keep the current example open for review across messages. The user may send corrections while implementation or rendering is underway; apply relevant steering at the next safe step, preserve completed work, and rerender only affected outputs. Answer status or workflow questions briefly, then continue the authorized work. Do not require the user to finish the preferences workflow before reviewing the circuit.

Record the concrete change, its reason, the reviewed revision, and whether it applies only to this drawing or expresses a wider preference. Preserve earlier feedback as history and mark superseded interpretations explicitly. For an example not yet approved for the collection, keep concise feedback and proposed lessons in the authorized project context; do not silently publish its source or image. Once preservation is approved, consolidate relevant evidence into its example record and link the context to it.

<a id="agent-suggestions"></a>

## Agent suggestions

This workflow is active by default during every Schematica drawing, correction, review, and collection session. It does not require a separate prompt or run as an unattended background task. The agent must have access to this updated workflow; do not claim that unavailable or older installations have adopted it.

1. **Notice:** after a meaningful correction, repeated choice, or clearly liked/disliked feature, consider whether there is a reusable lesson. Do not manufacture a proposal for every message or infer approval of an entire drawing from praise of one detail.
2. **Classify:** distinguish an explicit user statement from an agent inference, and classify the scope as general, one named style, or only the current example. Check accepted rules and pending/declined suggestions before proposing anything. A local numerical adjustment is not automatically a universal parameter.
3. **Propose:** at a useful review checkpoint, give concise rule wording, scope, reason, supporting example/correction, and intended destination. Group related suggestions and prioritize those likely to prevent repeat errors. Finish the requested correction before asking about permanent adoption unless a material conflict requires clarification.
4. **Record the decision:** keep pending/deferred/rejected suggestions in the inactive section of [general preferences](../../preferences/GENERAL.md), with links to existing evidence. When the current session authorizes routine context logging, the project log may retain the discussion and decision history; this does not turn a suggestion into a rule. An unanswered or praised proposal remains pending. Do not repeat a declined suggestion without new evidence or a user request.
5. **Save accepted guidance:** with explicit scoped approval, put general rules in `preferences/GENERAL.md`, named-style rules/exceptions in the relevant `STYLE.md`, and example-local changes in `EXAMPLE.md` (or current context for an unsaved example). Give a shared rule a stable ID and link the evidence in both directions when the evidence record exists. Saving a rule does not authorize publishing example assets or redrawing historical work. Do not request the same approval again.
6. **Check use:** before delivery, check the current request, applicable accepted general rules, explicit style exceptions, technical meaning, and relevant previews. During later examples, notice counterexamples and propose a narrower rule or an explicit exception rather than silently weakening accepted guidance.

Suggested wording: "This correction may be useful beyond this drawing. Proposed [general/style] rule: ... Evidence: ... Save it in ...?" Use natural language and omit the prompt when nothing useful emerged or the scope is already approved.

## Start or add to a collection

1. Reuse a matching collection if one exists. Otherwise use a readable full name for `examples/<COLLECTION>/`, such as `THE_ART_OF_ELECTRONICS`. Create only the needed files.
2. Create or update `STYLE.md` with purpose, source, collection status, confirmed preferences, provisional patterns, an example guide, unresolved questions, and the next useful step. Add its link and selection cues to `examples/INDEX.md`. Maintain a separate collection `README.md` for human browsing: a short introduction and clickable previews with titles and one-line descriptions. Link the main README to this gallery, keeping detailed guidance in `STYLE.md`.
3. Give each example a stable descriptive folder name. For a numbered source figure, use a name such as `fig-01-07-adjustable-divider`; for new generated work, use the subject rather than a book figure number. Check for duplicates before adding.
4. Follow [the example record format](references/example-record.md). Save `EXAMPLE.md` with the original supplied caption, source reference, a description, user feedback, inferred lessons, and accurate asset/review status. Preserve important associated explanations with clear attribution.
5. Screenshots and original PDFs are working references. Do not commit them as finished drawings or establish a separate permanent screenshot archive by default. Captions are repository content, alongside the example. Source information should identify the work and figure without depending on a private machine path.
6. When a recreation is authorized and ready, keep `drawing.tex` and `preview.png` together. Compile and inspect the rendered figure, preserve technical meaning, and verify that the preview represents the saved source. Add an example `README.md` showing the PNG immediately, a brief useful description, original caption/source information, and links to the PNG, LaTeX, detailed record, and collection gallery. Long captions may be expandable but remain in the repository. Do not claim a visual recreation is a reusable semantic CircuitikZ implementation unless it actually is.
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

- Read the saved records back. Check captions, attribution, links, asset availability, review status, and the index-to-style-to-example reading path. Also check the human path from the main README through the collection gallery to each example, its image/source, and back. Keep public READMEs brief and focused on available work; do not introduce unestablished installation or invocation instructions.
- Check the general-preferences-to-style reading route, explicit exceptions, rule/evidence links, and separation of accepted rules from pending suggestions. Confirm that a local correction has not silently become a universal rule.
- Confirm new screenshots, temporary PDFs, build output, and unrelated material have not entered the repository.
- Keep source and preview synchronized. If only metadata changed, do not redraw an already accepted figure unnecessarily.
- Follow repository instructions for checks, commits, and pushes within the approved scope. Report any limitation, including whether fresh-chat discovery and real drawing behavior have actually been tested.
