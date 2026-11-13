"""Bundle the complete local first batch, omitting caches and installed tools."""
import hashlib
import json
from pathlib import Path
import zipfile
from core import ROOT
from exports import catalog, export


def package():
    keys = [c['key'] for s in catalog()['symbols'] for c in s['configurations']]
    (ROOT/'review/all-symbols.zip').write_bytes(export('zip', keys)[2])
    allowed = {'definitions','tex','viewer','library','tests','references','review'}
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file()
        and (len(p.relative_to(ROOT).parts) == 1 or p.relative_to(ROOT).parts[0] in allowed)
        and '__pycache__' not in p.parts and p.suffix != '.pyc'
        and p.name not in ('first-batch.zip','package-manifest.json'))
    manifest = {str(p.relative_to(ROOT)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}
    manifest_path = ROOT/'review/package-manifest.json'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    archive_path = ROOT/'review/first-batch.zip'
    with zipfile.ZipFile(archive_path,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in paths+[manifest_path]:
            archive.write(path, 'schematica-first-batch/'+path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        for name, entry in manifest.items():
            assert hashlib.sha256(archive.read('schematica-first-batch/'+name)).hexdigest() == entry['sha256']
    print(json.dumps({'files':len(paths)+1,'archive_bytes':archive_path.stat().st_size,'sha256':hashlib.sha256(archive_path.read_bytes()).hexdigest()},indent=2))


if __name__ == '__main__':
    package()
