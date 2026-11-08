# The Art of Electronics — plots and signal sketches

Read [the shared style guide](STYLE.md) and applicable [general preferences](../../preferences/GENERAL.md) first. Apply general rules only within their stated scope; circuit-symbol rules do not govern waveform traces.

## Scope and status

Existing content covers qualitative signal sketches, timing relationships, and annotated overlapping waveforms. This guide extracts that content from the former combined guide. It does not define a quantitative plot style, measured axes, numerical sampling, Bode conventions, or new accepted rules. Shared typography and composition remain in [STYLE.md](STYLE.md#shared-visual-character-provisional-observations).

## Signals and annotations — provisional

For qualitative signals, emphasize shape and timing. Axes, ticks, and grids should carry needed information rather than appear automatically. Small waveform sketches can describe signals locally, as in [Figure 1.7](examples/mixed/fig-01-07-adjustable-divider/EXAMPLE.md); larger panels can explain several circuit points, as in [Figure 1.43](examples/mixed/fig-01-43-leading-edge-detector/EXAMPLE.md).

Use concise annotations and clear leaders. A dashed trace needs an understood meaning; its presence in one figure is not a default for all signals. Quantitative plot conventions remain to be established.

## Select examples

- Local signal sketches: [Figure 1.7](examples/mixed/fig-01-07-adjustable-divider/EXAMPLE.md), with a saved recreation and previews; [Figure 2.29](examples/mixed/fig-02-29-complementary-followers/EXAMPLE.md), a text record without a repository preview.
- Circuit points linked to stacked waveform panels: [Figure 1.43](examples/mixed/fig-01-43-leading-edge-detector/EXAMPLE.md), with a saved recreation and previews.
- Standalone overlapping signals and nonideal transitions: [Figure 4.62](examples/plots/fig-04-62-clamp-output-glitches/EXAMPLE.md), a text record without a repository preview. Its source supplies no time scale, frequency, sampled data, or numerical slew rate. Preserve that limitation; do not treat explanatory geometry as measured data. The separate [Figure 4.61 circuit](examples/schematics/fig-04-61-active-clamp/EXAMPLE.md) is linked from the record.

Mixed examples remain in `examples/mixed/`; read [SCHEMATICS.md](SCHEMATICS.md) when drawing their circuits. Obtain unavailable source images before recreation or measurement. The [collection inventory](STYLE.md#example-guide) retains each example's feedback and review status.

## Explicit exceptions to general preferences

None currently. Apply the inheritance and exception procedure in [STYLE.md](STYLE.md#explicit-exceptions-to-general-preferences).

[Visual gallery](README.md) · [Shared style guide](STYLE.md)
