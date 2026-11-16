"""Read back Batch 03 source and all hosted SVG/fragment hashes. Never writes to Review."""
from support import APP
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from review_client import Client, digest, write_json


def verify(config, workers=6):
    batch = APP / 'batches/batch-03'
    rows = json.loads((batch / 'manifest.json').read_text(encoding='utf-8'))['targets']
    client = Client(config)
    state = client.state()
    hashes, total = set(), 0
    for row in rows:
        assert row['status'] == 'submitted', row['id']
        revision = client.revision(row['revision_id'])
        folder = batch / 'symbols' / row['id']
        assert revision['source']['definition'] == json.loads((folder / 'definition.json').read_text(encoding='utf-8'))
        assert revision['source']['recipe'] == (folder / 'custom.tex').read_text(encoding='utf-8')
        assert revision['fingerprint'] == row['fingerprint']
        assert row['revision_id'] in state['symbols'][row['id']]['revisions']
        assert revision['readiness']['visual']['summary']
        configs = revision['symbol']['configurations']
        assert len(configs) == row['configurations']
        total += len(configs)
        hashes.update(c[key] for c in configs for key in ('sha256', 'fragment'))
    def check(h):
        assert digest(client.request('/review/assets/' + h)) == h, h
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(check, hashes))
    return {'designs': len(rows), 'configurations': total, 'hosted_asset_hashes': len(hashes),
            'exact_source_and_history_references': 'passed', 'service_writes': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, help='Private existing Review connection file')
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--output', type=Path, help='Optional local receipt outside the repository')
    args = parser.parse_args()
    result = verify(args.config, args.workers)
    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, indent=2))
