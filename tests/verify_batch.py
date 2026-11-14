"""Inkscape checks for a selected family in an isolated candidate library.

Set SCHEMATICA_LIBRARY to the merged candidate, then pass --batch <stable-id>.
The command does not promote artwork or change official approvals.
"""
from support import APP
import argparse
import concurrent.futures
import hashlib
import json
import uuid
import xml.etree.ElementTree as ET
import fitz

from core import SVG, INK, tool, run, validate_svg_references
from exports import LIBRARY, catalog, sheet

def inkscape(args, work):
    # Each check gets its own CLI instance; never route commands to a user's GUI.
    return run([tool('inkscape'),'--app-id-tag=schematica_b_'+uuid.uuid4().hex,*args],work)


def verify(batch, workers=4):
    data=catalog();symbols=[s for s in data['symbols'] if s.get('batch')==batch]
    if not symbols:raise ValueError('Unknown or empty batch: '+batch)
    work=APP/'build/batch-checks'/batch;work.mkdir(parents=True,exist_ok=True)
    items=[(s,c) for s in symbols for c in s['configurations']]
    def check(item):
        symbol,c=item;source=LIBRARY/c['svg'];root=ET.parse(source).getroot();group=root.find(f'{{{SVG}}}g')
        validate_svg_references(root)
        assert {p.get('data-part') for p in group}=={p['id'] for p in symbol['parts']}
        assert all(p.get(f'{{{INK}}}label')==p.get('data-part') for p in group)
        assert all(not list(p.iter(f'{{{SVG}}}g'))[1:] for p in group)
        assert not list(root.iter(f'{{{SVG}}}text')),'Symbol labels must be vector outlines'
        pdf=work/(c['key']+'.pdf')
        _,output=inkscape([str(source),'--query-all',f'--export-filename={pdf}'],work)
        queried={row.split(',')[0]:[float(v)*25.4/96 for v in row.split(',')[1:]] for row in output.splitlines() if len(row.split(','))==5}
        x,y,w,h=queried[group.get('id')]
        margin=min(x,y,c['width_mm']-x-w,c['height_mm']-y-h)
        assert margin>.9,(c['key'],margin)
        annotation_clearance=None
        if symbol.get('family')=='analog' and symbol['id']!='ota':
            parts={g.get('data-part'):g for g in root.iter() if g.get('data-part')}
            bx,by,bw,bh=queried[parts['body'].get('id')];stroke=c['settings']['stroke_mm']
            labels=[queried[g.get('id')] for pid,g in parts.items() if pid!='body' and not pid.startswith('lead-')]
            gaps=[]
            for lx,ly,lw,lh in labels:
                gaps.extend([lx-bx-stroke,ly-by-stroke,bx+bw-stroke-lx-lw,by+bh-stroke-ly-lh])
            annotation_clearance=min(gaps)
            assert annotation_clearance>=.2999,(c['key'],'mark/label too close to functional block border',annotation_clearance)
        with fitz.open(pdf) as document:
            assert document.page_count==1 and document[0].get_drawings(),c['key']
            assert not document[0].get_images(),c['key']
        result={'configuration':c['key'],'margin_mm':margin,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
        if annotation_clearance is not None:result['minimum_annotation_clearance_mm']=annotation_clearance
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:checks=list(pool.map(check,items))
    configs=[c for _,c in items]
    for symbols_mode in (False,True):
        name='symbols' if symbols_mode else 'instances';source=work/(name+'.svg')
        source.write_bytes(sheet(configs,6,6,symbols_mode))
        expected=[p.get('data-part') for p in ET.parse(source).getroot().iter() if p.get('data-part')]
        for suffix in ('saved','reopened'):
            target=work/(name+'-'+suffix+'.svg')
            inkscape([str(source),f'--export-filename={target}'],work)
            tree=ET.parse(target).getroot();validate_svg_references(tree)
            assert [p.get('data-part') for p in tree.iter() if p.get('data-part')]==expected
            assert all(p.get(f'{{{INK}}}label')==p.get('data-part') for p in tree.iter() if p.get('data-part'))
            source=target
    result={'batch':batch,'designs':len(symbols),'configurations':len(checks),
            'minimum_margin_mm':min(c['margin_mm'] for c in checks),'inkscape_vectors_and_bounds':'passed',
            'instances_and_symbols_save_reopen':'passed','checks':checks,
            'scope':'Command-line Inkscape; agent visual inspection is recorded separately. No human approval.'}
    (work/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--batch',required=True);parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args();verify(args.batch,args.workers)
