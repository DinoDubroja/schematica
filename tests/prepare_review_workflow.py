"""Copy published drawings into explicitly isolated, unpublished workflow fixtures."""
from support import APP
import argparse
import copy
import json
import re
import html
from pathlib import Path
from review_client import Client, package_symbol, write_json


def prepare(source_config, validation_config, output, prefix='review-flow-'):
    source, client = Client(source_config), Client(validation_config)
    assert client.url.split('//')[1].startswith('schematica-review-validation.')
    root = Path(output); root.mkdir(parents=True, exist_ok=True)
    state, saved = source.state(), client.state()
    specs = [('npn', 'darlington-npn', 'Darlington NPN', 'Workflow shared'),
             ('pnp', 'darlington-pnp', 'Darlington PNP', 'Workflow shared'),
             ('extend-npn', 'darlington-npn', 'Extension Darlington NPN', 'Workflow extension'),
             ('extend-pnp', 'darlington-pnp', 'Extension Darlington PNP', 'Workflow extension')]
    specs += [(f'nav-{letter}', 'darlington-npn', f'Navigation {letter.upper()}', 'Workflow navigation') for letter in 'abc']
    manifest = {}
    for short, original_id, name, batch in specs:
        identity = prefix + short
        if prefix!='review-flow-':batch += ' '+prefix.rstrip('-')
        original = state['symbols'][original_id]
        parent = source.revision(original['published'] or original['latest'])
        folder = root / identity; art = folder / 'artwork'; art.mkdir(parents=True, exist_ok=True)
        if identity in saved['symbols']:
            manifest[short] = {'symbol': identity, 'revision': saved['symbols'][identity]['revisions'][0], 'batch':saved['symbols'][identity]['batch']}
            continue
        exact_source, symbol = copy.deepcopy(parent['source']), copy.deepcopy(parent['symbol'])
        for target in (exact_source['definition'], symbol):
            target.update(id=identity, name=name, revision=1, description='Isolated workflow fixture. Never publish.', keywords=['Darlington', 'BJT', 'transistor'])
        for config in symbol['configurations']:
            raw = source.request('/review/assets/' + config['sha256'])
            config['symbol_id'] = identity; config['key'] = config['key'].replace(original_id, identity); config['svg'] = config['key'] + '.svg'
            text = raw.decode('utf-8').replace(original_id, identity)
            def metadata(match):
                value=json.loads(html.unescape(match[1]));value['revision']=1
                return '<metadata>'+html.escape(json.dumps(value),quote=False)+'</metadata>'
            text=re.sub(r'<metadata>([\s\S]*?)</metadata>',metadata,text)
            config['revision']=1
            (art / config['svg']).write_text(text,encoding='utf-8')
        package=folder/'package';suffix=1
        while package.exists():
            suffix+=1;package=folder/f'package-{suffix}'
        revision = package_symbol(symbol, exact_source, package, art, {'by':'Workflow validation','summary':'Existing drawing, unchanged geometry; isolated identity.'}, batch=batch)
        client.upload(package); manifest[short] = {'symbol':identity, 'revision':revision['id'],'batch':batch}
    write_json(root / 'fixtures.json', manifest)
    print(json.dumps({'fixtures':len(manifest), 'published':0}))


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-config',required=True);p.add_argument('--config',required=True);p.add_argument('--output',required=True);p.add_argument('--prefix',default='review-flow-');a=p.parse_args()
    assert a.prefix.startswith('review-flow-')
    prepare(a.source_config,a.config,a.output,a.prefix)
