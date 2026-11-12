"""Queue missing native dossiers against a hash-validated private REA inventory.

OpenAI Codex (LLM). Acquisition only, never an automatic semantic pass.
Existing requests/responses are retained, including failed attempts.
"""
import argparse
import hashlib
import json
from pathlib import Path
from rea_audit_inventory import PORT, evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--limit', type=int, default=64)
    args = parser.parse_args()
    if args.limit < 1: parser.error('Positive batch size required')
    root = (PORT/'reports'/args.report).resolve()
    if not root.is_relative_to((PORT/'reports').resolve()): parser.error('Private reports only')
    listing = evidence(root/'002-procedures.response.json')
    digest = hashlib.sha256((PORT.parent/'CLAW.EXE').read_bytes()).hexdigest()
    if listing['subject']['digest']['sha256'] != digest: raise ValueError('Different target')
    existing = set()
    for path in root.glob('*.request.json'):
        request = json.loads(path.read_text(encoding='utf-8'))
        if request['name'] == 'analyze_function': existing.add(request['arguments']['procedure'])
    candidates = [p['address'] for p in listing['normalized_result']
        if p.get('procedure', {}).get('external') is False and p['address'] not in existing]
    queued = []
    for address in sorted(candidates, key=lambda a: int(a, 16))[:args.limit]:
        path = root/('10000-fn-'+address+'.request.json')
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(dict(name='analyze_function', arguments=dict(procedure=address))), encoding='utf-8')
        temporary.replace(path)
        queued.append(address)
    print(json.dumps(dict(queued=len(queued), remaining_unqueued=len(candidates)-len(queued),
                         semantic_review_implied=False)))


if __name__ == '__main__':
    main()
