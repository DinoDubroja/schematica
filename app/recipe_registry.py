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
}

BATCH_LABEL_RECIPES = frozenset(())
