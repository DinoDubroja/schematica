# The Art of Electronics

Illustration style under development from selected examples in *The Art of Electronics*, third edition, Paul Horowitz and Winfield Hill (2015).

[Browse the visual gallery](README.md). This document provides detailed guidance and example selection for agents.

**Collection status:** collecting. Thirty-one reference records are saved: five have LaTeX source, light/dark SVG previews, PNG downloads, captions, and browsing pages; twenty-six have captions and observations, with recreation pending. The example guide below identifies each record and its available assets. The shared drawing patterns below remain provisional. A first practical output-stage trial has been drawn and refined separately; it is not yet a saved collection example or evidence of a fully validated style. See [the current checkpoint](../../context/CURRENT.md).

## Purpose

Create electronics illustrations that look as though they belong in the book: clear, compact, carefully composed, and useful for explaining how a circuit or concept works.

Include practical schematics, conceptual circuits, abstract diagrams, waveforms, plots, equations, and combined figures. Preserve the requested connections, names, values, and technical meaning.

## Use this style

Read [general schematic preferences](../../preferences/GENERAL.md) before this guide, then select relevant examples below. View available previews and read their captions and feedback; inspect LaTeX when useful for construction. Select by the drawing problem, including annotations and composition, not only by circuit category.

### Explicit exceptions to general preferences

None currently. Inherit every applicable accepted general preference. A reference image or provisional observation does not implicitly override it. If an exception is approved, record the general rule ID, exact replacement behavior, scope, and decision/evidence here; do not copy the full general rule into this guide.

The five completed previews can be inspected from this checkout without the source book. The twenty-six pending references are text records only; their source screenshots were inspected in the collecting chat and are not saved as repository previews. Read the selected record's recreation and review status; availability is not the same as user approval of the recreation. Do not claim to have seen an image based only on its record.

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
| [Figure 1.1: Parallel connection](fig-01-01-parallel-connection/EXAMPLE.md) | Explaining connectivity independently of components | Generic shapes sharing two terminals | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.6: Voltage divider](fig-01-06-voltage-divider/EXAMPLE.md) | Combining a circuit with voltage relationships and an equation | Voltage-span annotations beside an equation | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.7: Adjustable voltage divider](fig-01-07-adjustable-divider/EXAMPLE.md) | Adjustable elements, alternate implementations, or signals at terminals | Small input signals, control labels, and curved annotations | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.11: Thévenin equivalent circuit](fig-01-11-thevenin-equivalent/EXAMPLE.md) | Explaining equivalence or reducing a conceptual network | An irregular network beside its compact equivalent | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.43: Leading-edge detector](fig-01-43-leading-edge-detector/EXAMPLE.md) | Explaining signals at several points of a circuit | Matched A/B/C labels, stacked waveforms, and a time-constant annotation | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.67: Voltage multipliers](fig-01-67-voltage-multipliers/EXAMPLE.md) | Comparing related circuits; transformers, polarized capacitors, and external loads | Three stacked panels, bracket-like circuit-name annotations, and dashed loads | Caption and observations; source/preview pending |
| [Figure 1.68: Regulated dc power supply](fig-01-68-regulated-dc-power-supply/EXAMPLE.md) | Mixing explicit circuitry with a functional block | Diamond bridge layout, internal block-terminal labels, and exposed output connections | Caption and observations; source/preview pending |
| [Figure 1.83: Inductive kick](fig-01-83-inductive-kick/EXAMPLE.md) | Explaining a switching event in a simple circuit | Current/node labels and localized spark/BOOM annotation | Caption and observations; source/preview pending |
| [Figure 1.84: Blocking inductive kick](fig-01-84-blocking-inductive-kick/EXAMPLE.md) | Distinguishing current paths and operating conditions | Straight on-current arrow and curved turnoff annotation | Caption and observations; source/preview pending |
| [Figure 1.139: Oscilloscope probe](fig-01-139-oscilloscope-probe/EXAMPLE.md) | Combining a physical object, circuit model, and functional block | Probe outline, grouped scope input, and stacked model labels | Caption and observations; source/preview pending |
| [Figure 2.25: AC-coupled emitter follower](fig-02-25-ac-coupled-emitter-follower/EXAMPLE.md) | Transistor layout, bias dividers, and coupling capacitors | Subscripted identifiers and orderly vertical branches | Caption and observations; source/preview pending |
| [Figure 2.29: Complementary followers](fig-02-29-complementary-followers/EXAMPLE.md) | Combining a transistor circuit with local signal sketches | Signed voltage-shift annotations and input/output waveforms | Caption and observations; source/preview pending |
| [Figure 2.64: Differential amplifier performance](fig-02-64-differential-amplifier-performance/EXAMPLE.md) | Combining a schematic with performance equations | Mirrored transistor pair, polarity labels, and three adjacent equations | Caption and observations; source/preview pending |
| [Figure 2.66: Single-ended dc amplifier](fig-02-66-single-ended-dc-amplifier/EXAMPLE.md) | Differential-pair composition with asymmetric connections | Central current source and grounded reference input | Caption and observations; source/preview pending |
| [Figure 2.68: Loudspeaker amplifier](fig-02-68-loudspeaker-amplifier/EXAMPLE.md) | Combining a circuit, physical load, and thermal annotation | Loudspeaker icon, heat-sink fins, and local input waveform | Caption and observations; source/preview pending |
| [Figure 2.78: Sziklai-pair power stage](fig-02-78-sziklai-pair-power-stage/EXAMPLE.md) | Dense practical power-stage layout and part labels | Stacked identifiers/part numbers, bias adjustment, and continuation leads | Caption and observations; source/preview pending |
| [Figure 3.111: Low-power piezo driver](fig-03-111-piezo-driver/EXAMPLE.md) | Dense mixed op-amp/discrete circuitry and detailed ratings | Perimeter feedback, shared device leaders, and paired signal/return terminals | Caption and observations; source/preview pending |
| [Figure 4.7: Amplifiers for ac signals](fig-04-07-ac-signal-amplifiers/EXAMPLE.md) | Comparing capacitor placement in related op-amp circuits | Stacked A/B panels with an adjacent cutoff equation | Caption and observations; source/preview pending |
| [Figure 4.13: FET-bipolar current source](fig-04-13-fet-bipolar-current-source/EXAMPLE.md) | Annotated control circuits and thermal details | Voltage-span/current arrows, alternative-device text, and a dashed device outline | Caption and observations; source/preview pending |
| [Figure 4.29: Voltage regulator](fig-04-29-voltage-regulator/EXAMPLE.md) | Composite-device grouping and horizontal power paths | Darlington boundary, port specification stacks, and compensation label | Caption and observations; source/preview pending |
| [Figure 4.58: Op-amp peak trackers](fig-04-58-peak-trackers/EXAMPLE.md) | Multi-op-amp feedback routing and circuit comparisons | Stacked alternatives with storage nodes and distinct diode/feedback paths | Caption and observations; source/preview pending |
| [Figure 4.61: Active clamp](fig-04-61-active-clamp/EXAMPLE.md) | A direct signal path with a supporting control branch | Compact clamp circuit paired with Figure 4.62 | Caption and observations; source/preview pending |
| [Figure 4.62: Clamp output glitches](fig-04-62-clamp-output-glitches/EXAMPLE.md) | Qualitative nonideal behavior and overlapping signals | Direct waveform labels, dashed transition markers, and curved glitch leaders | Caption and observations; source/preview pending |
| [Figure 4.63: Active full-wave rectifier](fig-04-63-active-full-wave-rectifier/EXAMPLE.md) | Conditional explanations and symbolic component ratios | Braced node annotation, curved leader, and an output relationship | Caption and observations; source/preview pending |
| [Figure 4.73: Split-supply generator](fig-04-73-split-supply-generator/EXAMPLE.md) | Explicit op-amp supplies and an output-defined reference node | Follower output marked as ground and capacitor polarity between rails | Caption and observations; source/preview pending |
| [Figure 4.80: Single-supply photometer](fig-04-80-single-supply-photometer/EXAMPLE.md) | Sensor-to-readout composition and instrument annotations | Photodiode light/current arrows and separate meter/readout scales | Caption and observations; source/preview pending |
| [Figure 4.87: Laboratory dc amplifier](fig-04-87-laboratory-dc-amplifier/EXAMPLE.md) | Complex project schematics; explicitly liked for this role | Main signal chain, auxiliary offset circuit, boxed controls, connectors, and meter | Caption and observations; source/preview pending |
| [Figure 4.105: Power-source output amplifier](fig-04-105-power-source-amplifier/EXAMPLE.md) | Transformer-coupled power circuitry and a long feedback path | Winding-polarity dots, heat-sink/rating labels, and an output receptacle | Caption and observations; source/preview pending |
| [Figure 5.64: Inherently differential signals](fig-05-64-differential-signals/EXAMPLE.md) | Combining schematics, alternative sources, and physical interconnects | Bridge panel beside shielded twisted pair, XLR connector, and receiver requirements | Caption and observations; source/preview pending |
| [Figure 5.77: Instrumentation amplifier](fig-05-77-instrumentation-amplifier/EXAMPLE.md) | Paired input stages, sense/ref terminals, and scoped equations | A brace ties gain equations to the first stage rather than the full circuit | Caption and observations; source/preview pending |
| [Figure 5.78: Signal guarding](fig-05-78-signal-guarding/EXAMPLE.md) | Multi-panel guard circuits and mixed abstraction levels | Five unequal panels, shield/guard distinctions, and partial IC internals | Caption and observations; source/preview pending |

Figures 1.7 and 1.43 received positive feedback on their recreated appearance. The new recreations of Figures 1.1, 1.6, and 1.11 were compiled and visually checked by the assistant on 08-11-2026; user review is pending. All five use editable TikZ paths inside a CircuitikZ environment, not semantic native-component examples. Their implementation details are not all approved style rules.

## Review a new illustration

Check technical correctness, typography, symbol proportions, spacing, line weights, and label clearance against selected references. Check that panel labels agree and that the SVG and PNG exports represent the saved LaTeX source. Preserve the new task's actual circuit and signals rather than copying example values or topology as defaults.

Use transparent SVG by default in chat and on GitHub, with ink appropriate to the active theme; retain the PNG for convenient downloads and visual inspection. Follow the [presentation procedure](../../scripts/PRESENTATION.md), including light/dark checks. The caption remains readable text in the example record.

## Open questions and next step

Latest addition: Figures 5.77 and 5.78, explicitly requested on 08-11-2026. Both are recorded. Image-only references and optional PNG previews are under discussion; the workflow change is not implemented. The following are options for further work, not authorization to start drawings or another batch.

- Review the three newly completed recreations and continue collecting supplied examples. Twenty-six further figures are recorded; their recreations await an explicit drawing request.
- Review the proposed shared patterns and establish useful drawing parameters from evidence.
- Add coverage for larger practical circuits and quantitative plots.
- Continue the separate output-stage trial's review and preservation discussion. Its initial feedback and refinements are in [the trial checkpoint](../../context/LOG.md#output-stage-trial); saving it as an example remains unapproved.

Collection can continue before consolidation is complete. Use the shared [workflow](../../skills/schematica-examples/SKILL.md) to resume; this file records the current state, not approval to perform every suggested next step.
