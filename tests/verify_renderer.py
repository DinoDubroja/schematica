"""Recheck the bounded renderer, native CircuitikZ and editable-label proof."""
from support import APP, FIXTURES
import json
import uuid
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import fitz

from core import SVG, render_symbol, run, tool, validate_svg_references, write_svg, get_definition, resolve_settings, tex_document


def verify():
    work = APP / "build/renderer-verification"
    work.mkdir(parents=True, exist_ok=True)
    rendered = render_symbol("opamp-supply", "small", "thick", work / "fresh-symbol")
    accepted = json.loads((FIXTURES / "accepted-geometry.json").read_text(encoding="utf-8"))
    svg = ET.parse(rendered["output"]).getroot()
    assert [p.get("d") for p in svg.iter(f"{{{SVG}}}path")] == accepted["opamp-supply-small-thick"]["paths"]
    validate_svg_references(svg)
    for helper in (APP / "tex").iterdir():
        shutil.copy2(helper, work / helper.name)
    shutil.copy2(FIXTURES / "native-circuitikz.tex", work / "native-circuitikz.tex")
    run([tool("tectonic"), "-X", "compile", "--untrusted", "native-circuitikz.tex"], work)
    assert (work / "native-circuitikz.pdf").stat().st_size > 0
    for sid in ('thermistor-ntc-eu', 'thermistor-ptc-us', 'resistor-variable-us'):
        definition = get_definition(sid)
        options = {'orientation': 'down-left'} if definition.get('options') else None
        settings = resolve_settings(definition, 'small', 'thick', options)
        file = work / f'{sid}.tex'
        file.write_text(tex_document(definition, settings, 'native-proof', svg=False), encoding='utf-8')
        run([tool('tectonic'), '-X', 'compile', '--untrusted', file.name], work)
        with fitz.open(file.with_suffix('.pdf')) as pdf:
            assert pdf[0].get_drawings(), sid
            if 'thermistor' in sid:
                assert ('NTC' if 'ntc' in sid else 'PTC') in pdf[0].get_text(), sid
    label = ET.parse(FIXTURES / "editable-label.svg").getroot()
    original = json.loads((FIXTURES / "editable-label.strings.json").read_text(encoding="utf-8"))
    text = next(label.iter(f"{{{SVG}}}text"))
    assert text.text == original["label"]
    text.text = "Label B"
    edited = work / "editable-label-edited.svg"
    write_svg(label, edited)
    for name in ["editable-label-saved.svg", "editable-label-reopened.svg"]:
        saved = work / name
        run([tool("inkscape"), "--app-id-tag=schematica_b_"+uuid.uuid4().hex, str(edited), f"--export-filename={saved}"], work)
        again = ET.parse(saved).getroot()
        assert next(again.iter(f"{{{SVG}}}text")).text == "Label B"
        assert any(p.get("data-original-text") == original["label"] for p in again.iter())
        edited = saved
    report = {"fresh_small_thick_opamp": "accepted paths match", "native_circuitikz": "compiled",
              "native_thermistors_and_orientation": "Small/Thick PDF compile and NTC/PTC text passed",
              "editable_label": "edit/save/reopen passed", "scope": "bounded fixture, command-line only"}
    (work / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    verify()
