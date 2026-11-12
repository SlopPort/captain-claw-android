"""Build the private full-audit ledger from actual REA function Evidence.

OpenAI Codex (LLM). Enumeration/decompilation never marks semantic review done.
An independent PE header inventory accounts for executable ranges separately
from Ghidra's detected functions, including executable zero-fill sections.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

PORT = Path(__file__).resolve().parents[1]


def evidence(path):
    response = json.loads(path.read_text(encoding='utf-8'))
    if 'evidence_id' in response and 'normalized_result' in response:
        return response # Exact complete record exported by REA after a transport budget failure.
    if response.get('error') or response.get('worker_error'):
        raise ValueError('Failed REA response')
    result = response['result']
    if result.get('isError'): raise ValueError('REA tool returned an error')
    value = result.get('structuredContent')
    if value is None:
        value = json.loads(next(x['text'] for x in result['content'] if x['type'] == 'text'))
    return value


def pe_inventory(data):
    if data[:2] != b'MZ': raise ValueError('Not a DOS/PE image')
    offset = struct.unpack_from('<I', data, 60)[0]
    if data[offset:offset+4] != b'PE\0\0': raise ValueError('Not PE')
    machine, count = struct.unpack_from('<HH', data, offset+4)
    optional_size = struct.unpack_from('<H', data, offset+20)[0]
    optional = offset+24
    if machine != 0x14c or struct.unpack_from('<H', data, optional)[0] != 0x10b:
        raise ValueError('Expected x86 PE32')
    base = struct.unpack_from('<I', data, optional+28)[0]
    rows = []
    for index in range(count):
        start = optional+optional_size+40*index
        name = data[start:start+8].rstrip(b'\0').decode('ascii')
        virtual_size, rva, raw_size, raw_offset = struct.unpack_from('<IIII', data, start+8)
        flags = struct.unpack_from('<I', data, start+36)[0]
        if raw_size and raw_offset+raw_size > len(data): raise ValueError('Section outside file')
        rows.append(dict(name=name, va=hex(base+rva), virtual_size=virtual_size,
            raw_offset=raw_offset, raw_size=raw_size, flags=hex(flags),
            executable=bool(flags & 0x20000000), writable=bool(flags & 0x80000000),
            executable_zero_fill_bytes=max(0, virtual_size-raw_size) if flags & 0x20000000 else 0))
    raw_end = max(s['raw_offset']+s['raw_size'] for s in rows if s['raw_size'])
    return dict(source='Independent PE header parsing, not REA Evidence',
        format='PE32', architecture='x86', image_base=hex(base),
        entry=hex(base+struct.unpack_from('<I', data, optional+16)[0]), sections=rows,
        trailing_file_offset=raw_end, trailing_file_bytes=len(data)-raw_end)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--procedures', default='002-procedures.response.json')
    args = parser.parse_args()
    root = (PORT/'reports'/args.report).resolve()
    if not root.is_relative_to((PORT/'reports').resolve()): parser.error('Private reports only')
    binary = (PORT.parent/'CLAW.EXE').read_bytes()
    digest = hashlib.sha256(binary).hexdigest()
    listing = evidence(root/args.procedures)
    if listing['operation'] != 'list_procedures' or listing['subject']['digest']['sha256'] != digest:
        raise ValueError('Wrong operation or different target identity')
    procedures = listing['normalized_result']
    addresses = [p['address'] for p in procedures]
    if len(set(addresses)) != len(addresses): raise ValueError('Duplicate function entries')
    # Review decisions are separately maintained, never inferred from tool success.
    reviews_path = root/'reviews.json'
    reviews = json.loads(reviews_path.read_text(encoding='utf-8')) if reviews_path.exists() else {}
    unknown_reviews = set(reviews)-set(addresses)
    if unknown_reviews: raise ValueError('Review outside inventoried function set')
    rows = []
    dossiers = {}
    failed_responses = []
    for path in list(root.glob('*.response.json'))+list(root.glob('*.retained-evidence.json')):
        try: value = evidence(path)
        except (ValueError, KeyError, StopIteration):
            failed_responses.append(path.name); continue
        if value.get('operation') != 'analyze_function': continue
        if value['subject']['digest']['sha256'] != digest: raise ValueError('Different dossier target')
        address = value['normalized_result']['procedure']['address']
        if address not in addresses: raise ValueError('Dossier outside inventory')
        dossiers[address] = dict(path=path.name, evidence_id=value['evidence_id'],
            body=value['normalized_result']['procedure']['body'],
            facets=value['normalized_result']['facet_availability'],
            unresolved_calls=len(value['normalized_result']['unresolved_calls']))
    for procedure in procedures:
        metadata = procedure.get('procedure', {})
        address = procedure['address']
        review = reviews.get(address, {})
        if review.get('semantic_status', 'unreviewed') not in ('unreviewed', 'partial', 'reviewed', 'blocked'):
            raise ValueError('Unknown review status')
        if review.get('semantic_status', 'unreviewed') != 'unreviewed':
            if not all(review.get(key) for key in ('findings', 'evidence', 'limitations', 'port_comparison')):
                raise ValueError('Review requires findings, evidence, limits and port comparison')
        rows.append(dict(address=address, provider_name=procedure['value'],
            external=metadata.get('external'), thunk=metadata.get('thunk'),
            thunk_target=metadata.get('thunk_target'),
            semantic_status=review.get('semantic_status', 'unreviewed'), review=review,
            dossier=dossiers.get(address)))
    layout = pe_inventory(binary)
    body_map = []
    for section in layout['sections']:
        if not section['executable'] or not section['raw_size']: continue
        start = int(section['va'], 16)
        end = start+section['raw_size']
        intervals = []
        for dossier in dossiers.values():
            body = dossier['body']
            if not body.get('available'): continue
            for span in body['ranges']:
                lo, hi = int(span['start'], 16), int(span['end'], 16)+1
                if hi <= lo: raise ValueError('Invalid inclusive function range')
                if max(start, lo) < min(end, hi): intervals.append((max(start, lo), min(end, hi)))
        merged = []
        for lo, hi in sorted(intervals):
            if merged and lo <= merged[-1][1]: merged[-1][1] = max(hi, merged[-1][1])
            else: merged.append([lo, hi])
        gaps = []; cursor = start
        for lo, hi in merged:
            if cursor < lo: gaps.append([cursor, lo])
            cursor = hi
        if cursor < end: gaps.append([cursor, end])
        covered = sum(hi-lo for lo, hi in merged)
        if covered+sum(hi-lo for lo, hi in gaps) != section['raw_size']:
            raise ValueError('Executable range accounting mismatch')
        body_map.append(dict(section=section['name'], acquired_body_union_bytes=covered,
            ranges_outside_acquired_bodies=[dict(start=hex(lo), end_inclusive=hex(hi-1),
                bytes=hi-lo, file_offset=section['raw_offset']+lo-start,
                classification='unclassified; includes not-yet-acquired functions') for lo, hi in gaps]))
    summary = dict(target_sha256=digest, target_bytes=len(binary),
        rea_inventory_evidence=listing['evidence_id'], provider=listing['provider'],
        analysis_profile=listing['analysis_profile'],
        enumerated_functions=len(rows), external_functions=sum(p['external'] is True for p in rows),
        internal_functions=sum(p['external'] is False for p in rows),
        thunks=sum(p['thunk'] is True for p in rows),
        semantically_reviewed=sum(p['semantic_status'] == 'reviewed' for p in rows),
        partially_reviewed=sum(p['semantic_status'] == 'partial' for p in rows),
        acquired_dossiers=len(dossiers), failed_responses=failed_responses,
        executable_file_bytes=sum(s['raw_size'] for s in layout['sections'] if s['executable']),
        executable_zero_fill_bytes=sum(s['executable_zero_fill_bytes'] for s in layout['sections']),
        trailing_file_bytes=layout['trailing_file_bytes'],
        acquired_function_body_executable_bytes=sum(s['acquired_body_union_bytes'] for s in body_map),
        instruction_byte_coverage=None,
        limitations=['Function discovery is not an exhaustive classification of executable bytes.',
            'External functions are imports, not implementations recovered from this file.',
            'Automated extraction does not prove semantic understanding or port equivalence.',
            'Executable zero-fill, indirect calls, dynamically loaded code and unresolved paths need separate accounting.',
            'Supplied CrazyHook-distributed executable is not certified pristine 1997.'])
    for name, value in [('pe-layout.json', layout), ('function-ledger.json', rows),
                        ('function-body-map.json', body_map), ('inventory-summary.json', summary)]:
        temporary = root/(name+'.tmp')
        temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
        temporary.replace(root/name)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
