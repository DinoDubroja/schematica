# The Art of Electronics

Illustration style under development from selected examples in *The Art of Electronics*, third edition, Paul Horowitz and Winfield Hill (2015).

**Collection status:** collecting. Five reference examples are documented; two have LaTeX source and PNG previews. The shared drawing patterns below are provisional. This is not a complete description of the book or a style validated on new practical circuits.

## Purpose

Create electronics illustrations that look as though they belong in the book: clear, compact, carefully composed, and useful for explaining how a circuit or concept works.

Include practical schematics, conceptual circuits, abstract diagrams, waveforms, plots, equations, and combined figures. Preserve the requested connections, names, values, and technical meaning.

## Use this style

Read the shared guidance, then select relevant examples from the guide below. View available previews and read their captions and feedback; inspect LaTeX when useful for construction. Select by the drawing problem, including annotations and composition, not only by circuit category.

Three records currently have no visual asset in the repository. Their descriptions help selection, but are not a substitute for inspecting the original supplied reference or book figure when visual detail matters. Do not claim to have seen an image based only on its record.

## Confirmed preferences

- Include diagrams that explain concepts even when they do not describe practical circuits.
- Treat circuits, waveforms, equations, and annotations as parts of one illustration when they belong together.
- Use small signal sketches near terminals when they help explain the signal.
- Preserve accompanying captions and descriptions with the example in the repository.
- A reference supplied without comments is liked overall. Specific praise does not make every other detail a shared requirement.

## Shared visual character: provisional observations

These are candidate patterns inferred from the selected references, not yet approved fixed drawing parameters.

### Lines and symbols

Use restrained monochrome line drawings, clear symbols, and consistent proportions. Keep weights consistent within their roles; waveform traces and connection dots may be stronger than fine annotation lines. The selected circuit examples use zigzag resistors, simple capacitor plates, and uncluttered ground bars. Follow the relevant reference for geometry.

Distinguish filled junction dots, exposed terminals, annotation arrows, and signal traces. Do not transfer a symbol or annotation convention without its meaning.

### Composition

Arrange the figure around the relationship it explains. Keep labels close to their subjects with visible clearance. Horizontal and vertical routing are useful for orderly circuits, while a conceptual network can use angled branches to expose its topology, as in [Figure 1.11](fig-01-11-thevenin-equivalent/EXAMPLE.md).

Place related equations, equivalent circuits, and waveform panels beside or below the circuit. Use matching labels to connect panels, as in [Figure 1.43](fig-01-43-leading-edge-detector/EXAMPLE.md).

### Typography and labels

Use a clean sans-serif appearance for ordinary diagram text and appropriate italics and subscripts for mathematical symbols. Keep identifiers, values, node labels, and explanatory text visually consistent and clear of drawing elements.

Exact fonts, sizes, spacing, and stroke measurements have not been established as shared parameters. The existing recreations use TeX Gyre Heros as a close substitute; that implementation choice is not a confirmed global font requirement.

### Signals and annotations

For qualitative signals, emphasize shape and timing. Axes, ticks, and grids should carry needed information rather than appear automatically. Small waveform sketches can describe signals locally, as in [Figure 1.7](fig-01-07-adjustable-divider/EXAMPLE.md); larger panels can explain several circuit points, as in [Figure 1.43](fig-01-43-leading-edge-detector/EXAMPLE.md).

Use concise annotations and clear leaders. A dashed trace needs an understood meaning; its presence in one figure is not a default for all signals. Quantitative plot conventions remain to be established.

## Example guide

| Example | Select when | Distinctive contribution | Available assets |
| --- | --- | --- | --- |
| [Figure 1.1: Parallel connection](fig-01-01-parallel-connection/EXAMPLE.md) | Explaining connectivity independently of components | Generic shapes sharing two terminals | Caption and feedback; recreation pending |
| [Figure 1.6: Voltage divider](fig-01-06-voltage-divider/EXAMPLE.md) | Combining a circuit with voltage relationships and an equation | Voltage-span annotations beside an equation | Caption and feedback; recreation pending |
| [Figure 1.7: Adjustable voltage divider](fig-01-07-adjustable-divider/EXAMPLE.md) | Adjustable elements, alternate implementations, or signals at terminals | Small input signals, control labels, and curved annotations | LaTeX, PNG, caption, and feedback |
| [Figure 1.11: Thevenin equivalent circuit](fig-01-11-thevenin-equivalent/EXAMPLE.md) | Explaining equivalence or reducing a conceptual network | An irregular network beside its compact equivalent | Caption and feedback; recreation pending |
| [Figure 1.43: Leading-edge detector](fig-01-43-leading-edge-detector/EXAMPLE.md) | Explaining signals at several points of a circuit | Matched A/B/C labels, stacked waveforms, and a time-constant annotation | LaTeX, PNG, caption, and feedback |

The two recreations received positive feedback on appearance. They are editable TikZ paths inside a CircuitikZ environment, not yet semantic native-component examples. Their implementation details are not all approved style rules.

## Review a new illustration

Check technical correctness, typography, symbol proportions, spacing, line weights, and label clearance against selected references. Check that panel labels agree and that the PNG represents the saved LaTeX source. Preserve the new task's actual circuit and signals rather than copying example values or topology as defaults.

Follow the repository's inline SVG presentation guidance when showing work in chat. The saved PNG is for stable browsing and visual inspection; the caption remains readable text in the example record.

## Open questions and next step

- Continue collecting supplied examples, or choose one of the three pending figures for an authorized recreation.
- Review the proposed shared patterns and establish useful drawing parameters from evidence.
- Add coverage for larger practical circuits and quantitative plots.
- Then test the style on a new practical circuit and observe whether the agent offers to preserve a useful result after feedback.

Collection can continue before consolidation is complete. Use the shared [workflow](../../skills/schematica-examples/SKILL.md) to resume; this file records the current state, not approval to perform every suggested next step.
