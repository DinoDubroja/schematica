"""Independent accepted-palette fidelity and full-library Inkscape checks."""
import json
import xml.etree.ElementTree as ET
import fitz
from core import ROOT, SVG, INK, BP_MM, run, tool, validate_svg_references
from exports import catalog, export
from verify_render import segments, nearest_error


def verify():
    data=catalog();work=ROOT/'build/library-verification';work.mkdir(parents=True,exist_ok=True)
    palette=fitz.open(ROOT/'references/accepted-palette/preset-comparison-10mm-shorter-opamp.pdf')
    drawings=[d for d in palette[0].get_drawings() if d['color'] and max(d['color'])<.01]
    rect=drawings[0]['rect'];origin=((rect.x0+rect.x1)/2,(rect.y0+rect.y1)/2)
    rows=[(0,'small','medium'),(23,'medium','medium'),(46,'large','medium'),(80,'medium','thin'),(103,'medium','medium'),(126,'medium','thick'),(160,'small','thick')]
    fidelity=[];margins=[]
    for col,symbol in enumerate(data['symbols']):
        for c in symbol['configurations']:
            source=ROOT/'library'/c['svg'];root=ET.parse(source).getroot();group=root.find(f'{{{SVG}}}g')
            validate_svg_references(root)
            assert {p.get('data-part') for p in group}=={p['id'] for p in symbol['parts']}
            assert all(p.get(f'{{{INK}}}label')==p.get('data-part') for p in group)
            assert all(not list(p.iter(f'{{{SVG}}}g'))[1:] for p in group)
            _,output=run([tool('inkscape'),str(source),'--query-all',f"--export-filename={work/(c['key']+'.pdf')}"],work)
            bounds=next(line.split(',')[1:] for line in output.splitlines() if line.startswith(group.get('id')+','))
            x,y,w,h=[float(v)*25.4/96 for v in bounds]
            margin=min(x,y,c['width_mm']-x-w,c['height_mm']-y-h)
            assert margin>.9,(c['key'],margin);margins.append(margin)
        for y,size,stroke in rows:
            c=next(c for c in symbol['configurations'] if c['size']==size and c['stroke']==stroke)
            cx,cy=origin[0]+28*col/BP_MM,origin[1]+y/BP_MM
            box=fitz.Rect(cx-12/BP_MM,cy-10/BP_MM,cx+12/BP_MM,cy+10/BP_MM)
            reference=[d for d in drawings if box.contains(d['rect'])]
            expected,widths=segments(reference)
            pdf=fitz.open(work/(c['key']+'.pdf'));actual,actual_widths=segments(pdf[0].get_drawings())
            error=nearest_error(actual,expected);stroke_error=max(abs(a-b) for a in widths for b in actual_widths)
            assert error<.005,(c['key'],error)
            assert stroke_error<.001
            fidelity.append({'configuration':c['key'],'coordinate_deviation_mm':error,'stroke_deviation_mm':stroke_error})
        print('Verified '+symbol['id'],flush=True)
    # Save/reopen all parts in every configuration, together with local references.
    for name in ('library-sheet','library-symbols'):
        source=ROOT/'review'/f'{name}.svg';saved=ROOT/'review'/f'{name}-saved.svg'
        run([tool('inkscape'),str(source),f'--export-filename={saved}'],work)
        before=ET.parse(source).getroot();after=ET.parse(saved).getroot();validate_svg_references(after)
        assert [p.get('data-part') for p in before.iter() if p.get('data-part')]==[p.get('data-part') for p in after.iter() if p.get('data-part')]
        assert all(p.get(f'{{{INK}}}label')==p.get('data-part') for p in after.iter() if p.get('data-part'))
        reopened=work/f'{name}-reopened.svg'
        run([tool('inkscape'),str(saved),f'--export-filename={reopened}'],work)
        validate_svg_references(ET.parse(reopened).getroot())
    keys=[s['configurations'][4]['key'] for s in data['symbols']]
    for kind in ('svg','zip','sheet','symbols'):
        name,mime,body=export(kind,keys[:1] if kind=='svg' else keys,columns=3,spacing=8)
        (ROOT/'review'/('sample-'+name)).write_bytes(body)
    results={'configurations':54,'palette_comparisons':fidelity,'minimum_page_margin_mm':min(margins),'max_coordinate_deviation_mm':max(f['coordinate_deviation_mm'] for f in fidelity),'max_stroke_deviation_mm':max(f['stroke_deviation_mm'] for f in fidelity),'all_parts_save_reopen':'passed','sheet_and_symbol_references':'passed'}
    (ROOT/'review/library-verification.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in results.items() if k!='palette_comparisons'},indent=2))


if __name__=='__main__':verify()
