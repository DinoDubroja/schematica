"""Explicit registrations for reviewed batch-02 TeX recipes. No schema changes."""

BATCH_MACROS = {
    'capacitor-feedthrough': 'SCBatchCapacitorFeedthrough',
    'capacitor-polarized': 'SCBatchCapacitorPolarized',
    'capacitor-polarized-curved': 'SCBatchCapacitorPolarizedCurved',
    'capacitor-trimmer': 'SCBatchCapacitorTrimmer',
    'capacitor-variable': 'SCBatchCapacitorVariable',
    'diode': 'SCBatchDiode',
    'diode-led': 'SCBatchDiodeLed',
    'diode-photo': 'SCBatchDiodePhoto',
    'diode-schottky': 'SCBatchDiodeSchottky',
    'diode-tvs-bidirectional': 'SCBatchDiodeTvsBidirectional',
    'diode-varactor': 'SCBatchDiodeVaractor',
    'diode-zener': 'SCBatchDiodeZener',
    'igbt-n': 'SCBatchIgbtN',
    'jfet-n': 'SCBatchJfetN',
    'jfet-p': 'SCBatchJfetP',
    'mosfet-n-depletion': 'SCBatchMosfetNDepletion',
    'mosfet-n-enhancement': 'SCBatchMosfetNEnhancement',
    'mosfet-n-enhancement-bulk': 'SCBatchMosfetNEnhancementBulk',
    'mosfet-p-depletion': 'SCBatchMosfetPDepletion',
    'mosfet-p-enhancement': 'SCBatchMosfetPEnhancement',
    'mosfet-p-enhancement-bulk': 'SCBatchMosfetPEnhancementBulk',
    'phototransistor-npn': 'SCBatchPhototransistorNpn',
    'transistor-npn': 'SCBatchTransistorNpn',
    'transistor-pnp': 'SCBatchTransistorPnp',
}

BATCH_LABEL_RECIPES = frozenset(())
