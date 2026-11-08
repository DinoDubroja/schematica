# Example record format

Use the same format for reference and generated examples. Omit sections that have no content; do not create empty placeholders or assets.

## Location

Store the complete record and its assets once at `styles/<COLLECTION>/examples/<category>/<example>/`. Categories describe the figure's main form, not approval or asset status. A mixed example stays intact and can be linked from several domain guides. Use the collection workflow for category selection; create no empty categories.

## Files

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

Pending references may have only `EXAMPLE.md`; mark them pending in the style guide rather than calling them completed gallery examples.

## README.md contents

Keep the human page short: title, visible theme-appropriate SVG, a useful sentence about the drawing, and links to the full image, editable LaTeX, detailed record, and gallery. Preserve the original caption and source with the picture; a long caption can use an expandable section. Link the collection gallery to this page rather than directly to the detailed agent record.

## EXAMPLE.md contents

- **Title and origin:** full descriptive title; `reference` or `generated`.
- **Source:** book/author/edition/figure/page for a reference, or the prompt and relevant inputs for generated work. A redraw is still a reference example.
- **User feedback:** specific praise or criticism, or liked overall. Identify whether feedback is a quotation or a summary.
- **Recreation and review:** say whether source/preview exist, what was visually reviewed, and what remains pending. Record the actual scope of approval.
- **Preview:** embed the light/dark SVG pair only when present, following [the presentation procedure](../../../scripts/PRESENTATION.md). Link to both SVGs, the retained PNG download, and editable source alongside it.
- **Caption and explanation:** keep the supplied original caption verbatim, with attribution, immediately with the picture. Normalize line wrapping and typographic ligatures without changing meaning. Preserve associated explanation when supplied; identify summaries or additions separately.
- **What it demonstrates:** describe the concrete drawing and its distinctive contribution beyond shared style rules.
- **Inferred lessons:** observations to consider, distinguished from explicit feedback and confirmed shared rules.
- **Preference scope and decisions:** for a useful correction or lesson, identify general, named-style, or example-local scope; record proposed/accepted/deferred/rejected status, a short decision/date, the reviewed revision, and a link to the authoritative rule or pending proposal. Distinguish the user's statement from the agent's interpretation. Approval of a local edit is not approval of a general rule or of asset publication.
- **Use and limits:** when this example is useful, when its conventions do not apply, and any known implementation limitations.

Generated examples additionally need the style/reference versions used, useful feedback and corrections, and the accepted result. Include concise before/after explanations and links to approved retained iterations when those teach something useful. Do not reconstruct missing prompts as though they were exact transcripts.

Continue the same record as the example develops. Keep consequential corrections and their reasons, explicitly supersede mistaken interpretations, and preserve only the intermediate assets included in the approved scope. One example can support both general and style-specific lessons without copying the drawing into separate collections. Until an example is approved for preservation, use the authorized project context for its feedback instead of creating a permanent example record.

## Collection-level state

Keep continuation state in `STYLE.md`: current collection/review status, example availability, open questions, and next useful action. Put domain-specific guidance and selection links in the relevant domain guide, and keep shared guidance in `STYLE.md`. The top-level `styles/INDEX.md` needs only enough information to choose a collection and see its available domains. Maintain a separate `README.md` gallery for people, with previews linking to the example pages. These files are not complete transcripts or records of blanket authorization.
