"""Recover literal registration seeds from private, hash-matched REA assembly.

OpenAI Codex (LLM). Does not invent function boundaries or semantic passes.
Names and callback bytes remain private; generated requests only inspect the
exact already-referenced address. Unsupported argument patterns stay unresolved.
"""
import argparse
import hashlib
import json
import re
from rea_audit_inventory import PORT, evidence


def registrations(assembly, strings):
    by_source = {s['source_address']: s for s in strings}
    pushes = []
    rows = []
    for line in assembly:
        address, instruction = line.split(': ', 1)
        if instruction.startswith('PUSH '):
            operand = instruction[5:]
            pushes.append((address, int(operand, 16) if re.fullmatch(r'0x[0-9a-f]+', operand) else None))
        if instruction.startswith('CALL '):
            if re.search(r'\+ 0x1c\]$', instruction):
                row = dict(call_address=address, status='unresolved-argument-pattern')
                if len(pushes) >= 3:
                    flag, name, callback = pushes[-3:]
                    text = by_source.get(name[0])
                    if (all(p[1] is not None for p in (flag, name, callback))
                            and (text is None or int(text['address'], 16) == name[1])):
                        row.update(status='literal-callback-observed', name=text['value'] if text else None,
                            name_state='defined-string' if text else 'not-in-defined-string-inventory',
                            name_address=hex(name[1]), callback=hex(callback[1]), flags=flag[1])
                rows.append(row)
            pushes = []
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--queue', action='store_true')
    args = parser.parse_args()
    root = (PORT/'reports'/args.report).resolve()
    if not root.is_relative_to((PORT/'reports').resolve()): parser.error('Private reports only')
    source = evidence(root/'10000-fn-0x401000.response.json')
    digest = hashlib.sha256((PORT.parent/'CLAW.EXE').read_bytes()).hexdigest()
    if source['subject']['digest']['sha256'] != digest: raise ValueError('Different target')
    native = source['normalized_result']
    rows = registrations(native['assembly'], native['referenced_strings'])
    for row in rows:
        if 'callback' not in row or row['name'] is not None: continue
        path = root/('031-registry-name-'+row['name_address']+'.response.json')
        if not path.exists(): continue
        name_evidence = evidence(path)
        if name_evidence['subject']['digest']['sha256'] != digest: raise ValueError('Different name target')
        value = name_evidence['normalized_result']
        if value['address'] != row['name_address'] or not value['complete']: continue
        raw = bytes.fromhex(value['bytes_hex'])
        if b'\0' not in raw: continue
        name = raw.split(b'\0', 1)[0]
        if name and all(32 <= byte < 127 for byte in name):
            row.update(name=name.decode('ascii'), name_state='bounded-read-nul-terminated',
                       name_evidence_id=name_evidence['evidence_id'])
    ledger = json.loads((root/'function-ledger.json').read_text(encoding='utf-8'))
    entries = {p['address'] for p in ledger}
    ranges = []
    for procedure in ledger:
        dossier = procedure.get('dossier')
        if dossier:
            for span in dossier['body']['ranges']:
                ranges.append((int(span['start'], 16), int(span['end'], 16), procedure['address']))
    seeds = set()
    checks = []
    for row in rows:
        if 'callback' not in row: continue
        address = row['callback']; number = int(address, 16)
        owners = [entry for lo, hi, entry in ranges if lo <= number <= hi]
        row.update(inventoried_entry=address in entries, acquired_body_owners=owners,
                   semantic_status='unreviewed', evidence_id=source['evidence_id'])
        if not owners and address not in entries: seeds.add(address)
    for address in sorted(seeds, key=lambda value: int(value, 16)):
        path = root/('030-registry-seed-'+address+'.response.json')
        if not path.exists(): continue
        check = evidence(path)
        if check['subject']['digest']['sha256'] != digest: raise ValueError('Different instruction target')
        value = check['normalized_result']
        if value['address'] != address: raise ValueError('Wrong seed address')
        checks.append(dict(address=address, status=value['status'],
            procedure=value['procedure'], evidence_id=check['evidence_id']))
    queued = 0
    if args.queue:
        for address in sorted(seeds, key=lambda value: int(value, 16)):
            path = root/('030-registry-seed-'+address+'.request.json')
            if path.exists(): continue
            temporary = path.with_suffix('.tmp')
            temporary.write_text(json.dumps(dict(name='inspect_native_instruction',
                arguments=dict(address=address))), encoding='utf-8')
            temporary.replace(path); queued += 1
        for address in sorted({row['name_address'] for row in rows if 'callback' in row and row['name'] is None}):
            path = root/('031-registry-name-'+address+'.request.json')
            if path.exists(): continue
            temporary = path.with_suffix('.tmp')
            temporary.write_text(json.dumps(dict(name='read_bytes',
                arguments=dict(address=address, length=128))), encoding='utf-8')
            temporary.replace(path)
    summary = dict(target_sha256=digest, evidence_id=source['evidence_id'],
        slot_calls=len(rows), resolved_literal_rows=sum('callback' in row for row in rows),
        unresolved_rows=sum('callback' not in row for row in rows),
        named_rows=sum(row.get('name') is not None for row in rows),
        distinct_callbacks=len({row['callback'] for row in rows if 'callback' in row}),
        distinct_callbacks_without_acquired_body=len(seeds), queued=queued,
        seed_instruction_checks=len(checks),
        decoded_unowned_seeds=sum(check['status']=='decoded' and check['procedure'] is None for check in checks),
        undecodable_seeds=[check['address'] for check in checks if check['status'] != 'decoded'],
        limitations=['Literal call-site observations, not complete callback bodies or virtual-slot implementation recovery.',
                     'Exact function entries and acquired-body containment are distinct.',
                     'Registration does not prove stock-map use or original runtime execution.'])
    (root/'registry-callback-ledger.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    (root/'registry-callback-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    (root/'registry-seed-instruction-checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
