"""Batch 03: render isolated sources, then submit only explicitly inspected candidates."""
import argparse, json, os, sys, uuid
from pathlib import Path

HERE=Path(__file__).resolve().parent
APP=HERE.parents[1]
sys.path.insert(0,str(APP))
import core
from custom_renderer import render_all, validate_custom
from review_client import Client, digest, package_symbol, write_json
from review_desktop import render_proof

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def tools(config):
    for name in ('tectonic','dvisvgm','inkscape'):
        if config.get(name): os.environ['SCHEMATICA_'+name.upper()]=config[name]

def prepare(symbol_id,work,config):
    tools(config)
    source_dir=HERE/'symbols'/symbol_id
    definition=read(source_dir/'definition.json');recipe=(source_dir/'custom.tex').read_text(encoding='utf-8')
    fingerprint=digest({'definition':definition,'recipe':recipe})
    target=Path(work)/symbol_id/fingerprint[:12]; target.mkdir(parents=True,exist_ok=True)
    if (target/'symbol.json').exists():
        symbol=read(target/'symbol.json')
    else:
        symbol=render_all(definition,recipe,target/'rendered');symbol['batch']='Batch 03'
        write_json(target/'symbol.json',symbol)
    validate_custom(definition,recipe)
    if symbol['source_fingerprint']!=fingerprint:
        # Reused drafts retain their original render fingerprint and exact SVGs.
        assert definition.get('lineage',{}).get('drawing_changes') is False
        assert read(target/'technical.json')['source_sha256']==fingerprint,'Cached render belongs to different source'
    assert len(symbol['configurations'])==len(core.configuration_choices(definition))
    for c in symbol['configurations']:
        raw=(target/'rendered'/c['svg']).read_bytes()
        assert digest(raw)==c['sha256']
        assert all(all(abs(v-round(v))<1e-6 for v in p) for p in c['pins_mm'].values())
    if not (target/'proof.png').exists():render_proof(symbol,target/'rendered',target/'proof',definition['name'])
    write_json(target/'technical.json',{'source_sha256':fingerprint,'configurations':len(symbol['configurations']),'metadata_pins_parts_bounds_exports':'passed','human_verified':False})
    print(json.dumps({'id':symbol_id,'configurations':len(symbol['configurations']),'proof':str(target/'proof.png'),'work':str(target)}),flush=True)
    return target

def submit(symbol_id,target,config,note):
    assert note.strip(),'A real visual inspection note is required'
    tools(config);client=Client(config);entry=client.state()['symbols'].get(symbol_id)
    definition=read(HERE/'symbols'/symbol_id/'definition.json');recipe=(HERE/'symbols'/symbol_id/'custom.tex').read_text(encoding='utf-8')
    symbol=read(target/'symbol.json');assert symbol['revision']==definition['revision']
    assert read(target/'technical.json')['source_sha256']==digest({'definition':definition,'recipe':recipe}),'Render current source before submitting'
    source={'format':'custom','definition':definition,'recipe':recipe,
            'helpers':{p.name:p.read_text(encoding='utf-8') for p in (APP/'tex').glob('*') if p.is_file()},
            'presets':core.read_yaml(APP/'presets.yaml')}
    identity=str(uuid.uuid5(uuid.NAMESPACE_URL,'schematica/batch-03/'+symbol_id+'/'+digest({'definition':definition,'recipe':recipe})))
    if entry:
        assert identity in entry['revisions'],'Existing live design must be reused or deliberately revised; never overwrite it'
        saved=client.revision(identity)
    else:
        package=target/'package'
        if not package.exists():package_symbol(symbol,source,package,target/'rendered',{'by':'Agent B','summary':note},batch='Batch 03',revision_id=identity,
            change={'kind':'batch-03-submission','why':'User-authorized Batch 03 candidate; awaits human review.','construction':definition.get('reference'), 'lineage':definition.get('lineage')})
        else:
            existing=read(package/'revision.json');assert existing['source']==source
        client.upload(package);saved=Client(config).revision(identity)
    assert saved['source']==source
    state=Client(config).state()['symbols'][symbol_id]
    assert state['candidate'] and state['batch']=='Batch 03' and identity in state['revisions']
    for c in saved['symbol']['configurations']:
        assert digest(client.request('/review/assets/'+c['sha256']))==c['sha256']
    manifest=read(HERE/'manifest.json')
    row=next(r for r in manifest['targets'] if r['id']==symbol_id)
    row.update(status='submitted',revision_id=identity,revision=saved['symbol']['revision'],configurations=len(saved['symbol']['configurations']),fingerprint=saved['fingerprint'])
    write_json(HERE/'manifest.json',manifest)
    write_json(target/'hosted-receipt.json',{'id':symbol_id,'revision_id':identity,'configurations':len(saved['symbol']['configurations']),'private_assets_checked':True})
    print(json.dumps({'submitted':symbol_id,'revision':identity,'configurations':len(saved['symbol']['configurations'])}),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',required=True);parser.add_argument('--work',required=True)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('id')
    p=sub.add_parser('submit');p.add_argument('id');p.add_argument('--target',required=True);p.add_argument('--visual-note',required=True)
    a=parser.parse_args();config=read(a.config)
    if a.command=='prepare':prepare(a.id,a.work,config)
    else:submit(a.id,Path(a.target),config,a.visual_note)
