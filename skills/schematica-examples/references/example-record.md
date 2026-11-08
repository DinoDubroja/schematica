# Example record format

Use the same format for reference and generated examples. Omit sections that have no content; do not create empty placeholders or assets.

## Location

Store the complete record and its assets once at `styles/<COLLECTION>/examples/<category>/<example>/`. Categories describe the figure's main form, not approval or asset status. A mixed example stays intact and can be linked from several domain guides. Use the collection workflow for category selection; create no empty categories.

## Files

An image-only reference is complete with these files:

```text
<example>/
├── README.md         # Image, short description, caption, downloads and navigation
├── EXAMPLE.md        # Provenance, explicit feedback and accurate asset/review state
└── reference.png     # Original bytes; keep actual extension for another format
```

An optional recreation adds the following files beside any original image:

```text
<example>/
├── README.md         # Human page when a visual example is ready
├── EXAMPLE.md        # Detailed record and agent guidance
├── drawing.tex       # Editable drawing
├── preview-light.svg # Transparent, dark ink for light presentation
├── preview-dark.svg  # Same geometry, light ink for dark presentation
├── preview.png       # Convenient download from the same source
└── iterations/       # Only for selected, approved instructive versions
    └── <version>/
        ├── drawing.tex
        ├── preview-light.svg
        ├── preview-dark.svg
        └── preview.png
```

Records without saved images may have only `EXAMPLE.md`; mark their image unavailable
in the inventory and category notes. Recreation is optional, not a prerequisite for
a visual reference. Do not create empty source files, fake SVGs, or broken previews.

## README.md contents

Keep the human page short: title, original image or theme-appropriate SVG, a useful
sentence, caption/source, available downloads, notes, category, and showcase links.
An original PNG retains its background. Link LaTeX only when it exists; distinguish
an original from a recreation when both exist. A long caption may be expandable.
Link visual gallery entries to this page; text-only entries link to `EXAMPLE.md`.

## EXAMPLE.md contents

- **Title and origin:** full descriptive title; `reference` or `generated`.
- **Source:** book/author/edition/figure/page for a reference, or the prompt and relevant inputs for generated work. A redraw is still a reference example.
- **User feedback:** specific praise or criticism, or liked overall. Identify whether feedback is a quotation or a summary.
- **Assets and review:** identify original-image, recreated, or text-only availability;
  both images may coexist in one record. State what was inspected, any import blocker,
  and actual approval. A saved original image is not an approved recreation or rule.
- **Preview:** link the human page and available original/derived files using
  [the presentation procedure](../../../scripts/PRESENTATION.md). Original PNGs do
  not need SVG partners. Add recreation downloads only when they exist.
- **Caption and explanation:** keep the supplied original caption verbatim, with attribution, immediately with the picture. Normalize line wrapping and typographic ligatures without changing meaning. Preserve associated explanation when supplied; identify summaries or additions separately.
- **What it demonstrates:** describe the concrete drawing and its distinctive contribution beyond shared style rules.
- **Inferred lessons:** optional observations within an approved analysis scope,
  distinguished from explicit feedback and confirmed rules. Omit new inference
  when the user asks only to save or organize without generalization.
- **Preference scope and decisions:** for a useful correction or lesson, identify general, named-style, or example-local scope; record proposed/accepted/deferred/rejected status, a short decision/date, the reviewed revision, and a link to the authoritative rule or pending proposal. Distinguish the user's statement from the agent's interpretation. Approval of a local edit is not approval of a general rule or of asset publication.
- **Use and limits:** when this example is useful, when its conventions do not apply, and any known implementation limitations.

Generated examples additionally need the style/reference versions used, useful feedback and corrections, and the accepted result. Include concise before/after explanations and links to approved retained iterations when those teach something useful. Do not reconstruct missing prompts as though they were exact transcripts.

Continue the same record as the example develops. Keep consequential corrections and their reasons, explicitly supersede mistaken interpretations, and preserve only the intermediate assets included in the approved scope. One example can support both general and style-specific lessons without copying the drawing into separate collections. Until an example is approved for preservation, use the authorized project context for its feedback instead of creating a permanent example record.

## Collection-level state

Keep continuation state and complete asset inventory in `STYLE.md`, with domain
guidance in its existing owning guides. The top-level `styles/INDEX.md` routes
selection. The collection `README.md` shows selected highlights; `examples/README.md`
and category READMEs expose all records. Store each example once. Category and
showcase links may reuse its assets. These files do not grant blanket authorization.
