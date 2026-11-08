# Low-power piezo driver

- **Origin:** reference.
- **Source:** Paul Horowitz and Winfield Hill, *The Art of Electronics*, third edition (2015), Figure 3.111. Printed page not supplied.
- **Received:** 08-11-2026, in the ongoing AOE collection session.
- **User feedback:** supplied without additional comments; recorded as liked overall under the collection convention. No specific feature approval is inferred.
- **Review and assets:** source screenshot visually inspected. Caption and observations are recorded; editable source and repository previews are unavailable. Recreation is pending. The screenshot remains a working input outside the repository.

## Original caption

> **Figure 3.111.** 1 kV low-power piezo driver with totem-pole output stage. A similar design is used for the high-voltage regulated dc supply shown in Figure 9.110.

Caption transcribed from the screenshot with line wrapping normalized. Figure 9.110 is a source cross-reference, not an additional collected example.

## What it demonstrates

A wide, dense schematic places two op-amps on the left and a tall discrete output stage on the right. The input and output each have a hollow signal terminal and a separate grounded return terminal. The +1kV rail also ends in a hollow terminal. Long feedback wiring follows the lower perimeter, keeping the central device labels readable.

Multiline labels combine identifiers, values, and ratings: the upper resistor is marked $R_{\mathrm{D}}$, 660k, 3W, and (3 × 220k); the output resistor is $R_{\mathrm{O}}$, 3.3k, ½W. Capacitors include 10nF 2kV, 470pF 3kV, and 10pF 3kV. The lower feedback resistor reads 10.0M 1%. A shared leader annotation lists IRFBG20, FQD2N100, and “(3 places)” beside the MOSFET stage. Two leaders associate the lower 1N4148 annotation with two diode symbols.

The U1 follower, U2 compensation network, bias/reference branches, and output stage are distinguished by placement rather than enclosing boxes. Filled junctions identify branch connections. A downward 0.5mA arrow sits beside Q3, separate from the wiring.

## Inferred lessons to review

- Route long feedback paths around functional groups while preserving clear junctions and crossings.
- Stack ratings and construction notes locally; use shared leaders when one annotation applies to repeated devices.
- Keep current arrows, signal terminals, supply connections, and grounded returns visually distinguishable by their electrical roles.

These are provisional observations. The source's supply terminal does not establish an exception to accepted supply-arrow guidance. Select for dense mixed op-amp/discrete layouts and detailed ratings. The caption's operating claims are source claims; this record is not a validated design or complete netlist. Obtain the original image for recreation.

[Collection guide](../../../STYLE.md) · [Available visual examples](../../../README.md)
