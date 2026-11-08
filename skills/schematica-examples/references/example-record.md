# Example record format

Use the same format for reference and generated examples. Omit sections that have no content; do not create empty placeholders or assets.

## Files

```text
<example>/
├── EXAMPLE.md
├── drawing.tex       # When a drawing exists
├── preview.png       # Rendered from that source
└── iterations/       # Only for selected, approved instructive versions
    └── <version>/
        ├── drawing.tex
        └── preview.png
```

## EXAMPLE.md contents

- **Title and origin:** full descriptive title; `reference` or `generated`.
- **Source:** book/author/edition/figure/page for a reference, or the prompt and relevant inputs for generated work. A redraw is still a reference example.
- **User feedback:** specific praise or criticism, or liked overall. Identify whether feedback is a quotation or a summary.
- **Recreation and review:** say whether source/preview exist, what was visually reviewed, and what remains pending. Record the actual scope of approval.
- **Preview:** embed `![Descriptive figure text](preview.png)` only when present. Link to the editable source alongside it.
- **Caption and explanation:** keep the supplied original caption verbatim, with attribution, immediately with the picture. Normalize line wrapping and typographic ligatures without changing meaning. Preserve associated explanation when supplied; identify summaries or additions separately.
- **What it demonstrates:** describe the concrete drawing and its distinctive contribution beyond shared style rules.
- **Inferred lessons:** observations to consider, distinguished from explicit feedback and confirmed shared rules.
- **Use and limits:** when this example is useful, when its conventions do not apply, and any known implementation limitations.

Generated examples additionally need the style/reference versions used, useful feedback and corrections, and the accepted result. Include concise before/after explanations and links to approved retained iterations when those teach something useful. Do not reconstruct missing prompts as though they were exact transcripts.

## Collection-level state

Keep continuation state in `STYLE.md`: current collection/review status, example availability, open questions, and next useful action. The top-level index needs only enough information to choose a collection. Neither file is a complete transcript or a record of blanket authorization.
