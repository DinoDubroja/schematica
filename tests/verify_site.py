from support import APP, FIXTURES
"""Validate the static bundle, optional browser downloads, and Inkscape round trips."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import fitz
from build_site import DIST
from core import ROOT, SVG, INK, run, tool, validate_svg_references


def verify(downloads=None):
    manifest = json.loads((DIST / 'build.json').read_text())
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((DIST / name).read_bytes()).hexdigest() == digest, name
    data = json.loads((DIST / 'library/catalog.json').read_text())
    work = ROOT / 'build/site-verification'
    work.mkdir(parents=True, exist_ok=True)
    results = []
    for preset, name in data['exports'].items():
        source = DIST / name
        original = ET.parse(source).getroot()
        if downloads:
            actual = Path(downloads) / source.name
            assert actual.read_bytes() == source.read_bytes(), f'Download mismatch: {actual.name}'
        saved = work / source.name
        run([tool('inkscape'), str(source), f'--export-filename={saved}'], work)
        root = ET.parse(saved).getroot()
        validate_svg_references(root)
        symbols = list(root.iter(f'{{{SVG}}}symbol'))
        assert len(symbols) == 6, preset
        before = [p.get('data-part') for p in original.iter() if p.get('data-part')]
        after = [p.get('data-part') for p in root.iter() if p.get('data-part')]
        assert before == after, preset
        assert all(p.get(f'{{{INK}}}label') == p.get('data-part') for p in root.iter() if p.get('data-part'))
        pdf = work / f'{preset}.pdf'
        run([tool('inkscape'), str(saved), f'--export-filename={pdf}'], work)
        with fitz.open(pdf) as document:
            page = document[0]
            assert abs(page.rect.width * 25.4 / 72 - float(original.get('width')[:-2])) < .01
            assert abs(page.rect.height * 25.4 / 72 - float(original.get('height')[:-2])) < .01
            drawings = page.get_drawings()
            assert drawings, preset
            assert all(page.rect.contains(d['rect']) for d in drawings), preset
        results.append({'preset': preset, 'symbols': 6, 'named_parts': len(after),
                        'references': 'passed', 'physical_page_size': 'passed', 'clipping': 'passed',
                        'browser_download': 'byte-identical' if downloads else 'not checked'})
        print(f'Verified library: {preset}', flush=True)
    if downloads:
        actual = Path(downloads) / 'inductor-coil-small-thick.svg'
        assert actual.read_bytes() == (DIST / 'library/svg' / actual.name).read_bytes()
    report = {'build_id': manifest['build_id'], 'libraries': results,
              'single_browser_download': 'byte-identical' if downloads else 'not checked',
              'note': 'Inkscape command-line save/reopen and PDF rendering; no GUI actions implied.'}
    (work / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'build_id': manifest['build_id'], 'libraries_passed': len(results)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--downloads', type=Path, help='Folder containing actual browser downloads with their original filenames')
    verify(parser.parse_args().downloads)
