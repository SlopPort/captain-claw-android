"""Conservatively inspect a bounded code region through actual REA instructions.

OpenAI Codex (LLM). No function creation, native execution or semantic passes.
Calls are recorded without following their targets; returnability is unknown.
Direct jumps and conditional fallthrough are explored inside caller-selected
bounds. Undecoded/computed/external edges remain explicit gaps. Results stay
private. Re-running resumes the saved worklist and existing REA responses.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
from rea_audit_inventory import PORT, evidence


def successors(instruction):
    address = int(instruction['address'], 16)
    flow = instruction['flow']; kind = flow['kind']
    if instruction['status'] != 'decoded': return [], ['instruction-not-decoded']
    if not isinstance(instruction['length'], int) or not 1 <= instruction['length'] <= 15:
        raise ValueError('Invalid x86 instruction length')
    next_address = address+instruction['length']
    if kind == 'fallthrough': return [next_address], []
    if kind == 'call': return [next_address], ['call-target-and-returnability-not-reviewed']
    if kind in ('return', 'terminal'): return [], []
    if kind == 'jump':
        destinations = [int(a, 16) for a in flow['direct_destinations'] if a.startswith('0x')]
        gaps = [] if destinations else ['jump-destination-unresolved']
        if flow['conditional']: destinations.append(next_address)
        return destinations, gaps
    return [], ['flow-unavailable']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--seed', required=True)
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True, help='Inclusive address bound')
    parser.add_argument('--max-instructions', type=int, default=1024)
    parser.add_argument('--seconds', type=int, default=50)
    args = parser.parse_args()
    root = (PORT/'reports'/args.report).resolve()
    if not root.is_relative_to((PORT/'reports').resolve()): parser.error('Private reports only')
    seed, start, end = (int(a, 16) for a in (args.seed, args.start, args.end))
    if not start <= seed <= end or args.max_instructions < 1: parser.error('Invalid region bounds')
    digest = hashlib.sha256((PORT.parent/'CLAW.EXE').read_bytes()).hexdigest()
    path = root/('region-'+hex(seed)+'.json')
    state = json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(
        target_sha256=digest, seed=hex(seed), start=hex(start), end=hex(end),
        instructions={}, pending=[hex(seed)], gaps=[], completed_bounded_worklist=False,
        semantic_status='unreviewed')
    if (state['target_sha256'], state['start'], state['end']) != (digest, hex(start), hex(end)):
        raise ValueError('Cannot reuse a different target or region')
    known = {}
    for request_path in root.glob('*.request.json'):
        request = json.loads(request_path.read_text(encoding='utf-8'))
        if request['name'] == 'inspect_native_instruction':
            known[request['arguments']['address']] = request_path
    deadline = time.monotonic()+args.seconds
    try:
        while state['pending'] and len(state['instructions']) < args.max_instructions and time.monotonic() < deadline:
            address = state['pending'][0]
            if address in state['instructions']: state['pending'].pop(0); continue
            request_path = known.get(address, root/('040-region-instruction-'+address+'.request.json'))
            if not request_path.exists():
                temporary = request_path.with_suffix('.tmp')
                temporary.write_text(json.dumps(dict(name='inspect_native_instruction',
                    arguments=dict(address=address))), encoding='utf-8')
                temporary.replace(request_path)
            response_path = request_path.with_name(request_path.name.replace('.request.', '.response.'))
            while not response_path.exists() and time.monotonic() < deadline:
                if (root/'worker.closed.json').exists(): raise RuntimeError('Audit worker ended; region worklist retained')
                time.sleep(.05)
            if not response_path.exists(): break
            record = evidence(response_path)
            if record['subject']['digest']['sha256'] != digest: raise ValueError('Different instruction target')
            instruction = record['normalized_result']
            if instruction['address'] != address: raise ValueError('Wrong instruction address')
            targets, gaps = successors(instruction)
            state['pending'].pop(0)
            state['instructions'][address] = dict(evidence_id=record['evidence_id'], instruction=instruction)
            for gap in gaps: state['gaps'].append(dict(address=address, reason=gap))
            for target in targets:
                if not start <= target <= end:
                    state['gaps'].append(dict(address=address, reason='edge-outside-selected-region', target=hex(target)))
                elif hex(target) not in state['instructions'] and hex(target) not in state['pending']:
                    state['pending'].append(hex(target))
    finally:
        state['completed_bounded_worklist'] = not state['pending']
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(state, indent=2), encoding='utf-8'); temporary.replace(path)
    print(json.dumps(dict(seed=state['seed'], observed_instructions=len(state['instructions']),
        pending=len(state['pending']), gaps=len(state['gaps']),
        completed_bounded_worklist=state['completed_bounded_worklist'], semantic_status=state['semantic_status'])))


if __name__ == '__main__':
    main()
