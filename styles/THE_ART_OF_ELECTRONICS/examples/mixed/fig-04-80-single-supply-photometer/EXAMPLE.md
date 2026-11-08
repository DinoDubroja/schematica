# Single-supply photometer

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 4.80. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is optional and has not been requested. The original image is not saved in the repository.

## Original caption

> **Figure 4.80.** Single-supply photometer.

Caption transcribed from the supplied screenshot.

## What it demonstrates

A photodiode at the left feeds the negative input of a TLC27L1 op-amp. Small diagonal incoming light arrows identify the photosensitive device; a separate curved arrow is labeled $I_{\mathrm{DIODE}}$. The positive input and lower supply lead are grounded. The upper supply lead has the stacked text “battery” and “+5 to +15”; there is no battery symbol at that annotation.

The feedback network is arranged above the op-amp: $R_1$, 10M, and $C_1$, 10pF, occupy parallel horizontal branches. Filled dots identify their common endpoints. A 10k output resistor leads to a boxed analog meter drawing with a needle and curved scale, whose return is grounded.

Separate labels distinguish the instrument from the measured quantity. A leader identifies a “0.5mA full-scale meter”; text to the right reads “photo-current readout”, $I_{\mathrm{DIODE}}$, and 0–500nA. These are different stated scales and must not be merged into one current rating. The component name TLC27L1 is positioned below the op-amp, clear of its supply connection.

## Inferred lessons to review

- Combine recognizable sensor and instrument symbols with standard circuitry when that clarifies the measurement chain.
- Distinguish incident-light arrows, electrical-current annotations, and label leaders.
- Place instrument specifications and calibrated readout ranges separately, close to their intended subjects.

These observations remain provisional. Select for sensor-to-readout composition and compact annotations; compare [Figure 1.139](../fig-01-139-oscilloscope-probe/EXAMPLE.md) for another physical/circuit illustration. The ranges are transcribed source labels, not a new calibration analysis. Obtain the original image for recreation; no new supply or ground convention is adopted.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
