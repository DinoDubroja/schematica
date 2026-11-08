# The Art of Electronics

Style collection under development from selected examples in *The Art of Electronics*, third edition, Paul Horowitz and Winfield Hill (2015).

[Browse the showcase](README.md) or [all examples](examples/README.md). This is the shared entry point, collection inventory, and composition guidance for agents.

**Collection status:** collecting. Thirty-one reference records are saved: five have LaTeX source, light/dark SVG previews, PNG downloads, captions, and browsing pages; twenty-six have captions and observations without saved images. Image references are supported independently of optional recreation. Import of the original PNGs for Figures 5.77 and 5.78 is authorized but blocked by host name-resolution failure. The example guide below identifies each record and its available assets. The shared drawing patterns here and in the domain guides remain provisional. A first practical output-stage trial has been drawn and refined separately; it is not yet a saved collection example or evidence of a fully validated style. See [the current checkpoint](../../context/CURRENT.md).

## Purpose

Create electronics illustrations that look as though they belong in the book: clear, compact, carefully composed, and useful for explaining how a circuit or concept works.

Include practical schematics, conceptual circuits, abstract diagrams, waveforms, plots, equations, and combined figures. Preserve the requested connections, names, values, and technical meaning.

## Domain guides

- [Schematics](SCHEMATICS.md): circuit symbols, connection diagrams, routing, and circuit-specific example selection.
- [Plots and signal sketches](PLOTS.md): existing qualitative waveform guidance and references. Quantitative plot conventions are not established.

Read only the guides needed for the task. A combined circuit/waveform figure uses both.
Writing guidance has not been collected; there is no writing guide or writing example category yet.
The common book source does not make rules interchangeable across domains.

## Use this style

Read [general schematic preferences](../../preferences/GENERAL.md) before this guide, then read the relevant domain guide above and select examples below. View available previews and read their captions and feedback; inspect LaTeX when useful for construction. Select by the drawing problem, including annotations and composition, not only by circuit category.

### Explicit exceptions to general preferences

None currently. Inherit every applicable accepted general preference. A reference image or provisional observation does not implicitly override it. If an exception is approved, record the general rule ID, exact replacement behavior, scope, and decision/evidence in its owning domain guide, or here when shared across domains; do not copy the full general rule. Link domain exceptions from this section so they remain discoverable.

The five completed previews can be inspected from this checkout without the source book. The twenty-six references without saved images are text records only; their source screenshots were inspected in the collecting chat and are not saved as repository previews. Read the selected record's recreation and review status; availability is not the same as user approval of the recreation. Do not claim to have seen an image based only on its record.

## Confirmed preferences

- Include diagrams that explain concepts even when they do not describe practical circuits.
- Treat circuits, waveforms, equations, and annotations as parts of one illustration when they belong together.
- Use small signal sketches near terminals when they help explain the signal.
- Preserve accompanying captions and descriptions with the example in the repository.
- A reference supplied without comments is liked overall. Specific praise does not make every other detail a shared requirement.

## Shared visual character: provisional observations

These are candidate patterns inferred from the selected references, not yet approved fixed drawing parameters.

### Composition

Arrange the figure around the relationship it explains. Keep labels close to their subjects with visible clearance. Horizontal and vertical routing are useful for orderly circuits, while a conceptual network can use angled branches to expose its topology, as in [Figure 1.11](examples/schematics/fig-01-11-thevenin-equivalent/EXAMPLE.md).

Place related equations, equivalent circuits, and waveform panels beside or below the circuit. Use matching labels to connect panels, as in [Figure 1.43](examples/mixed/fig-01-43-leading-edge-detector/EXAMPLE.md).

### Typography and labels

Use a clean sans-serif appearance for ordinary diagram text and appropriate italics and subscripts for mathematical symbols. Keep identifiers, values, node labels, and explanatory text visually consistent and clear of drawing elements.

Exact fonts, sizes, spacing, and stroke measurements have not been established as shared parameters. The existing recreations use TeX Gyre Heros as a close substitute; that implementation choice is not a confirmed global font requirement.

## Example guide

Examples are stored once by their main form: `schematics/` includes conceptual connection diagrams and circuit comparisons; `plots/` holds standalone signal/plot figures; `mixed/` combines circuits with substantial waveform, equation, physical, or block-diagram content. Ordinary component labels and annotations alone do not make a schematic mixed. A mixed record can support several guides; follow links rather than copying or splitting it. These categories describe the saved figure, not its approval or asset status.

| Example | Category | Select when | Distinctive contribution | Available assets |
| --- | --- | --- | --- | --- |
| [Figure 1.1: Parallel connection](examples/schematics/fig-01-01-parallel-connection/EXAMPLE.md) | Schematics | Explaining connectivity independently of components | Generic shapes sharing two terminals | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.6: Voltage divider](examples/mixed/fig-01-06-voltage-divider/EXAMPLE.md) | Mixed | Combining a circuit with voltage relationships and an equation | Voltage-span annotations beside an equation | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.7: Adjustable voltage divider](examples/mixed/fig-01-07-adjustable-divider/EXAMPLE.md) | Mixed | Adjustable elements, alternate implementations, or signals at terminals | Small input signals, control labels, and curved annotations | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.11: Thévenin equivalent circuit](examples/schematics/fig-01-11-thevenin-equivalent/EXAMPLE.md) | Schematics | Explaining equivalence or reducing a conceptual network | An irregular network beside its compact equivalent | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.43: Leading-edge detector](examples/mixed/fig-01-43-leading-edge-detector/EXAMPLE.md) | Mixed | Explaining signals at several points of a circuit | Matched A/B/C labels, stacked waveforms, and a time-constant annotation | LaTeX, SVG, PNG, caption, and feedback |
| [Figure 1.67: Voltage multipliers](examples/schematics/fig-01-67-voltage-multipliers/EXAMPLE.md) | Schematics | Comparing related circuits; transformers, polarized capacitors, and external loads | Three stacked panels, bracket-like circuit-name annotations, and dashed loads | Caption and observations; image not saved |
| [Figure 1.68: Regulated dc power supply](examples/mixed/fig-01-68-regulated-dc-power-supply/EXAMPLE.md) | Mixed | Mixing explicit circuitry with a functional block | Diamond bridge layout, internal block-terminal labels, and exposed output connections | Caption and observations; image not saved |
| [Figure 1.83: Inductive kick](examples/schematics/fig-01-83-inductive-kick/EXAMPLE.md) | Schematics | Explaining a switching event in a simple circuit | Current/node labels and localized spark/BOOM annotation | Caption and observations; image not saved |
| [Figure 1.84: Blocking inductive kick](examples/schematics/fig-01-84-blocking-inductive-kick/EXAMPLE.md) | Schematics | Distinguishing current paths and operating conditions | Straight on-current arrow and curved turnoff annotation | Caption and observations; image not saved |
| [Figure 1.139: Oscilloscope probe](examples/mixed/fig-01-139-oscilloscope-probe/EXAMPLE.md) | Mixed | Combining a physical object, circuit model, and functional block | Probe outline, grouped scope input, and stacked model labels | Caption and observations; image not saved |
| [Figure 2.25: AC-coupled emitter follower](examples/schematics/fig-02-25-ac-coupled-emitter-follower/EXAMPLE.md) | Schematics | Transistor layout, bias dividers, and coupling capacitors | Subscripted identifiers and orderly vertical branches | Caption and observations; image not saved |
| [Figure 2.29: Complementary followers](examples/mixed/fig-02-29-complementary-followers/EXAMPLE.md) | Mixed | Combining a transistor circuit with local signal sketches | Signed voltage-shift annotations and input/output waveforms | Caption and observations; image not saved |
| [Figure 2.64: Differential amplifier performance](examples/mixed/fig-02-64-differential-amplifier-performance/EXAMPLE.md) | Mixed | Combining a schematic with performance equations | Mirrored transistor pair, polarity labels, and three adjacent equations | Caption and observations; image not saved |
| [Figure 2.66: Single-ended dc amplifier](examples/schematics/fig-02-66-single-ended-dc-amplifier/EXAMPLE.md) | Schematics | Differential-pair composition with asymmetric connections | Central current source and grounded reference input | Caption and observations; image not saved |
| [Figure 2.68: Loudspeaker amplifier](examples/mixed/fig-02-68-loudspeaker-amplifier/EXAMPLE.md) | Mixed | Combining a circuit, physical load, and thermal annotation | Loudspeaker icon, heat-sink fins, and local input waveform | Caption and observations; image not saved |
| [Figure 2.78: Sziklai-pair power stage](examples/schematics/fig-02-78-sziklai-pair-power-stage/EXAMPLE.md) | Schematics | Dense practical power-stage layout and part labels | Stacked identifiers/part numbers, bias adjustment, and continuation leads | Caption and observations; image not saved |
| [Figure 3.111: Low-power piezo driver](examples/schematics/fig-03-111-piezo-driver/EXAMPLE.md) | Schematics | Dense mixed op-amp/discrete circuitry and detailed ratings | Perimeter feedback, shared device leaders, and paired signal/return terminals | Caption and observations; image not saved |
| [Figure 4.7: Amplifiers for ac signals](examples/mixed/fig-04-07-ac-signal-amplifiers/EXAMPLE.md) | Mixed | Comparing capacitor placement in related op-amp circuits | Stacked A/B panels with an adjacent cutoff equation | Caption and observations; image not saved |
| [Figure 4.13: FET-bipolar current source](examples/schematics/fig-04-13-fet-bipolar-current-source/EXAMPLE.md) | Schematics | Annotated control circuits and thermal details | Voltage-span/current arrows, alternative-device text, and a dashed device outline | Caption and observations; image not saved |
| [Figure 4.29: Voltage regulator](examples/schematics/fig-04-29-voltage-regulator/EXAMPLE.md) | Schematics | Composite-device grouping and horizontal power paths | Darlington boundary, port specification stacks, and compensation label | Caption and observations; image not saved |
| [Figure 4.58: Op-amp peak trackers](examples/schematics/fig-04-58-peak-trackers/EXAMPLE.md) | Schematics | Multi-op-amp feedback routing and circuit comparisons | Stacked alternatives with storage nodes and distinct diode/feedback paths | Caption and observations; image not saved |
| [Figure 4.61: Active clamp](examples/schematics/fig-04-61-active-clamp/EXAMPLE.md) | Schematics | A direct signal path with a supporting control branch | Compact clamp circuit paired with Figure 4.62 | Caption and observations; image not saved |
| [Figure 4.62: Clamp output glitches](examples/plots/fig-04-62-clamp-output-glitches/EXAMPLE.md) | Plots | Qualitative nonideal behavior and overlapping signals | Direct waveform labels, dashed transition markers, and curved glitch leaders | Caption and observations; image not saved |
| [Figure 4.63: Active full-wave rectifier](examples/mixed/fig-04-63-active-full-wave-rectifier/EXAMPLE.md) | Mixed | Conditional explanations and symbolic component ratios | Braced node annotation, curved leader, and an output relationship | Caption and observations; image not saved |
| [Figure 4.73: Split-supply generator](examples/schematics/fig-04-73-split-supply-generator/EXAMPLE.md) | Schematics | Explicit op-amp supplies and an output-defined reference node | Follower output marked as ground and capacitor polarity between rails | Caption and observations; image not saved |
| [Figure 4.80: Single-supply photometer](examples/mixed/fig-04-80-single-supply-photometer/EXAMPLE.md) | Mixed | Sensor-to-readout composition and instrument annotations | Photodiode light/current arrows and separate meter/readout scales | Caption and observations; image not saved |
| [Figure 4.87: Laboratory dc amplifier](examples/schematics/fig-04-87-laboratory-dc-amplifier/EXAMPLE.md) | Schematics | Complex project schematics; explicitly liked for this role | Main signal chain, auxiliary offset circuit, boxed controls, connectors, and meter | Caption and observations; image not saved |
| [Figure 4.105: Power-source output amplifier](examples/mixed/fig-04-105-power-source-amplifier/EXAMPLE.md) | Mixed | Transformer-coupled power circuitry and a long feedback path | Winding-polarity dots, heat-sink/rating labels, and an output receptacle | Caption and observations; image not saved |
| [Figure 5.64: Inherently differential signals](examples/mixed/fig-05-64-differential-signals/EXAMPLE.md) | Mixed | Combining schematics, alternative sources, and physical interconnects | Bridge panel beside shielded twisted pair, XLR connector, and receiver requirements | Caption and observations; image not saved |
| [Figure 5.77: Instrumentation amplifier](examples/mixed/fig-05-77-instrumentation-amplifier/EXAMPLE.md) | Mixed | Paired input stages, sense/ref terminals, and scoped equations | A brace ties gain equations to the first stage rather than the full circuit | Caption and observations; image not saved |
| [Figure 5.78: Signal guarding](examples/mixed/fig-05-78-signal-guarding/EXAMPLE.md) | Mixed | Multi-panel guard circuits and mixed abstraction levels | Five unequal panels, shield/guard distinctions, and partial IC internals | Caption and observations; image not saved |

Figures 1.7 and 1.43 received positive feedback on their recreated appearance. The new recreations of Figures 1.1, 1.6, and 1.11 were compiled and visually checked by the assistant on 08-11-2026; user review is pending. All five use editable TikZ paths inside a CircuitikZ environment, not semantic native-component examples. Their implementation details are not all approved style rules.

## Review a new illustration

Check technical correctness, typography, symbol proportions, spacing, line weights, and label clearance against selected references. Check that panel labels agree and that the SVG and PNG exports represent the saved LaTeX source. Preserve the new task's actual circuit and signals rather than copying example values or topology as defaults.

Use transparent SVG by default for generated/recreated drawings in chat and on GitHub, with ink appropriate to the active theme; retain the PNG for convenient downloads and visual inspection. Saved reference images may display directly as PNG with their original background, without a LaTeX recreation. Follow the [presentation procedure](../../scripts/PRESENTATION.md), including light/dark checks. The caption remains readable text in the example record.

## Open questions and next step

Latest authorized work (08-11-2026): a curated SVG showcase and category browsing are implemented; the existing five figures are temporary highlights until the user selects favorites. The workflow accepts original-image references without requiring recreation. Both Figures 5.77 and 5.78 are recorded, but their authorized PNG imports remain blocked by a download/name-resolution failure. Complete those imports and their visual pages when the originals become accessible. The user explicitly deferred style generalization; this update adds no inferred rules or numeric parameters. The following are options, not authorization to start drawings, analysis, or another import batch.

- Review the three newly completed recreations and continue collecting supplied examples. Twenty-six further figures have text records but no saved images. Importing additional source images or recreating figures follows the approved scope; neither is required merely to retain a record.
- Style generalization and numeric-parameter extraction are deferred at the user's request; do not start them as part of gallery maintenance.
- Add coverage for larger practical circuits and quantitative plots.
- Continue the separate output-stage trial's review and preservation discussion. Its initial feedback and refinements are in [the trial checkpoint](../../context/LOG.md#output-stage-trial); saving it as an example remains unapproved.

Collection can continue before consolidation is complete. Use the shared [workflow](../../skills/schematica-examples/SKILL.md) to resume; this file records the current state, not approval to perform every suggested next step.
