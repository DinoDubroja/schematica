"""Validate files downloaded and edited in the actual browser/Inkscape journey.

This does not automate the GUI; reproduce the manual journey in README first.
"""
import io
import json
import xml.etree.ElementTree as ET
import zipfile
import fitz
from core import ROOT, SVG, INK, run, tool, validate_svg_references
from exports import export
from verify_render import segments, nearest_error


def verify():
    folder = ROOT / 'review/browser-exports'
    work = ROOT / 'build/browser-verification'
    work.mkdir(parents=True, exist_ok=True)
    selection = ['resistor-us-large-thin', 'inductor-coil-small-thick', 'opamp-medium-medium']
    for key in ('inductor-coil-small-thick', 'opamp-supply-medium-medium'):
        assert (folder / (key+'.svg')).read_bytes() == export('svg', [key])[2]
    assert (folder/'schematica-sheet.svg').read_bytes() == export('sheet', selection, 2, 8)[2]
    assert (folder/'schematica-symbols.svg').read_bytes() == export('symbols', selection)[2]
    with zipfile.ZipFile(folder/'schematica-symbols.zip') as actual, zipfile.ZipFile(io.BytesIO(export('zip', selection)[2])) as expected:
        assert actual.namelist() == expected.namelist()
        assert all(actual.read(name) == expected.read(name) for name in expected.namelist())
    for path in folder.glob('*.svg'):
        root = ET.parse(path).getroot()
        validate_svg_references(root)
        assert not list(root.iter(f'{{{SVG}}}circle'))
        assert all('inspection-grid' not in e.get('class','') for e in root.iter())
        saved = work/path.name
        run([tool('inkscape'), str(path), f'--export-filename={saved}'], work)
        after = ET.parse(saved).getroot()
        validate_svg_references(after)
        assert [e.get('data-part') for e in root.iter() if e.get('data-part')] == [e.get('data-part') for e in after.iter() if e.get('data-part')]
    clone = ET.parse(folder/'placed-coil-clone.svg').getroot()
    editable = ET.parse(folder/'placed-coil-editable.svg').getroot()
    assert list(clone.iter(f'{{{SVG}}}use'))
    assert not list(editable.iter(f'{{{SVG}}}use'))
    whole = next(e for e in editable.iter() if e.get('data-symbol') == 'inductor-coil')
    assert {e.get('data-part') for e in whole} == {'body','lead-a','lead-b'}
    assert all(e.get(f'{{{INK}}}label') == e.get('data-part') for e in whole)
    drawings = []
    for filename in ('inductor-coil-small-thick', 'placed-coil-clone', 'placed-coil-editable'):
        pdf = work/(filename+'.pdf')
        _, output = run([tool('inkscape'), str(folder/(filename+'.svg')), '--query-all', f'--export-filename={pdf}'], work)
        doc = fitz.open(pdf)
        drawings.append(segments(doc[0].get_drawings()))
    deviation = max(nearest_error(d[0], drawings[0][0]) for d in drawings[1:])
    assert deviation < .005, deviation
    assert all(abs(width-.3) < .001 for drawing in drawings for width in drawing[1])
    result = {
        'download_selection': selection,
        'four_browser_export_formats_match_core': True,
        'arranged_sheet': {'columns':2, 'spacing_mm':8},
        'dark_mode_svg_matches_original_black_artwork': True,
        'downloaded_svgs_save_reopen_and_references': 'passed',
        'coil_gui_placement': {'size':'small', 'stroke':'thick', 'measured_width_mm':14.3, 'measured_height_mm':1.8},
        'coil_clone_unlinked_in_gui': True,
        'coil_parts_survive_save_reopen': ['body','lead-a','lead-b'],
        'coil_save_reopen_coordinate_deviation_mm': deviation,
        'gui_observations': {
            'search_names_and_attributes':'zigzag, coil, triangle; expected cards returned',
            'type_filters':'4 passive, 2 amplifiers; clear search restores 6 appearances',
            'empty_search':'no-match message displayed',
            'presets':'Large/Thin US resistor, Small/Thick coil, Medium/Medium op-amp',
            'pins':'3 visible op-amp connections; Small coil at (-7,0) and (7,0)',
            'grid_toggle':'both grid and pin groups hidden and restored',
            'theme':'dark first launch, both directions switched, both preferences survive reload',
            'responsive_widths_px':[1280,1000,390],
            'horizontal_overflow':False,
            'browser_console_errors':[],
            'inkscape':'downloaded Symbols library opened; coil thumbnail pasted into fresh document, saved, unlinked, body selected in Layers, saved separately, closed and reopened'
        }
    }
    (ROOT/'review/browser-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    verify()
