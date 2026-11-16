"""Create synthetic private fixtures only on the isolated Review validation service."""
from support import APP
import argparse
import copy
import json
from pathlib import Path
import urllib.parse
from review_client import Client, package_symbol, write_json


def prepare(config, output):
    client=Client(config);root=Path(output);root.mkdir(parents=True,exist_ok=True)
    assert urllib.parse.urlparse(client.url).hostname.startswith('schematica-review-validation.'), 'Validation service required'
    state=client.state();parent=client.revision(state['symbols']['test-ground']['revisions'][0])
    raw={c['sha256']:client.request('/review/assets/'+c['sha256']) for c in parent['symbol']['configurations']}
    manifest={}
    names={'fast-a':'Navigation A','fast-b':'Navigation B','fast-c':'Navigation C','image-a':'Image feedback A','image-b':'Image feedback B','question':'Clarification fixture','stale':'Stale feedback fixture','failure':'Failure fixture'}
    for short,name in names.items():
        identity='review-ui-'+short;folder=root/identity;art=folder/'artwork';art.mkdir(parents=True,exist_ok=True)
        if identity in state['symbols']:
            manifest[short]={'symbol':identity,'revision':state['symbols'][identity]['revisions'][0]}
            continue
        source=copy.deepcopy(parent['source']);symbol=copy.deepcopy(parent['symbol'])
        for target in (source['definition'],symbol):
            target.update(id=identity,name=name,revision=1,description='Isolated usability test fixture; never publish to the real Library.')
        old=parent['symbol']['id']
        for c in symbol['configurations']:
            c['symbol_id']=identity;c['key']=c['key'].replace(old,identity);c['svg']=c['key']+'.svg'
            # Reuse the existing synthetic drawing without changing its geometry.
            (art/c['svg']).write_bytes(raw[c['sha256']].replace(old.encode(),identity.encode()).replace(parent['symbol']['name'].encode(),name.encode()))
        package=folder/'package'
        revision=json.loads((package/'revision.json').read_text()) if (package/'revision.json').exists() else package_symbol(symbol,source,package,art,{'by':'Validation fixture','summary':'Exact existing synthetic ground geometry; only fixture identity differs.'},batch='Usability navigation' if short.startswith('fast') else 'Usability feedback')
        existing=state['symbols'].get(identity)
        if existing:
            manifest[short]={'symbol':identity,'revision':existing['revisions'][0]}
        else:
            client.upload(package);manifest[short]={'symbol':identity,'revision':revision['id']}
    write_json(root/'fixtures.json',manifest)
    # A visible challenge is only in the pixels, never in the filename or job text.
    import fitz
    svg=b'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360"><rect width="640" height="360" fill="white"/><circle cx="150" cy="150" r="90" fill="#e89430"/><text x="106" y="178" font-family="Arial" font-size="78">47</text><path d="M330 100H520" stroke="black" stroke-width="24"/><text x="318" y="188" font-family="Arial" font-size="32">Reference</text></svg>'
    source=fitz.open(stream=svg,filetype='svg');pdf=fitz.open(stream=source.convert_to_pdf(),filetype='pdf')
    pdf[0].get_pixmap().save(root/'reference.png');pdf.close();source.close()
    print(json.dumps({'fixtures':len(manifest),'manifest':str(root/'fixtures.json'),'publications':0}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args();prepare(a.config,a.output)
