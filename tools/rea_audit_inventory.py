"""Build the private full-audit ledger from actual REA function Evidence.

OpenAI Codex (LLM). Enumeration/decompilation never marks semantic review done.
An independent PE header inventory accounts for executable ranges separately
from Ghidra's detected functions, including executable zero-fill sections.
"""
import argparse
import bisect
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


def validate_independent_region(region, source):
    """Validate the REA byte carrier without relabelling its local decoder."""
    if (source.get('operation') != 'read_bytes'
            or source['subject']['digest']['sha256'] != region['target_sha256']
            or source['evidence_id'] != region['byte_source']['evidence_id']):
        raise ValueError('Different independent-decoder byte source')
    value = source['normalized_result']
    data = bytes.fromhex(value['bytes_hex'])
    if (not value['complete'] or len(data) != value['requested_bytes']
            or len(data) != value['returned_bytes']
            or hashlib.sha256(data).hexdigest() != region['byte_source']['sha256']):
        raise ValueError('Incomplete/changed independent-decoder bytes')
    base = int(value['address'], 16)
    if int(region['start'], 16) != base or int(region['end'], 16) != base+len(data)-1:
        raise ValueError('Different independent-decoder interval')
    for item in region['instructions'].values():
        instruction = item['instruction']
        if item['byte_evidence_id'] != source['evidence_id']:
            raise ValueError('Different instruction byte carrier')
        if instruction['status'] != 'decoded':
            continue
        offset = int(instruction['address'], 16)-base
        size = instruction['length']
        if (not 1 <= size <= 15 or offset < 0 or offset+size > len(data)
                or bytes.fromhex(instruction['bytes']) != data[offset:offset+size]):
            raise ValueError('Instruction not backed by exact REA bytes')


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
    alternatives = {}
    instruction_bodies = {}
    failed_responses = []
    error_evidence = {}
    for path in list(root.glob('*.response.json'))+list(root.glob('*.retained-evidence.json')):
        try: value = evidence(path)
        except (ValueError, KeyError, StopIteration):
            failed_responses.append(path.name)
            response = json.loads(path.read_text(encoding='utf-8'))
            for item in response.get('result', {}).get('content', []):
                if item.get('type') != 'text': continue
                try: error = json.loads(item['text']).get('error', {})
                except (ValueError, AttributeError): continue
                retained = error.get('details', {}).get('reported_limits', {}).get('evidence_id')
                if retained: error_evidence[path.name] = retained
            continue
        operation = value.get('operation')
        if operation in ('procedure_info', 'read_function_instructions', 'procedure_references'):
            if value['subject']['digest']['sha256'] != digest: raise ValueError('Different alternate-evidence target')
            normalized = value['normalized_result']
            procedure = normalized if operation == 'procedure_info' else normalized['procedure']
            address = procedure.get('address', procedure.get('entrypoint'))
            if address not in addresses: raise ValueError('Alternate evidence outside inventory')
            alternatives.setdefault(address, []).append(dict(path=path.name,
                evidence_id=value['evidence_id'], operation=operation))
            if operation == 'read_function_instructions':
                instruction_bodies[address] = dict(body=procedure['body'])
            continue
        if operation != 'analyze_function': continue
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
            dossier=dossiers.get(address), alternative_evidence=alternatives.get(address, [])))
    layout = pe_inventory(binary)
    internal_addresses = {p['address'] for p in rows if p['external'] is False}
    acquired_bodies = dict(instruction_bodies)
    acquired_bodies.update(dossiers)
    missing_bodies = sorted(internal_addresses-set(acquired_bodies))
    acquired_ids = {dossier['evidence_id'] for dossier in dossiers.values()}
    recovered_errors = [name for name, retained in error_evidence.items() if retained in acquired_ids]
    body_map = []
    for section in layout['sections']:
        if not section['executable'] or not section['raw_size']: continue
        start = int(section['va'], 16)
        end = start+section['raw_size']
        intervals = []
        for dossier in acquired_bodies.values():
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
                classification=('unclassified outside acquired bodies; inventory acquisition complete'
                    if not missing_bodies else 'unclassified; includes not-yet-acquired functions')) for lo, hi in gaps]))
    regions = []; decoded_starts = set(); decoded_bytes = set(); decode_sources = {}
    for path in root.glob('region-*.json'):
        region = json.loads(path.read_text(encoding='utf-8'))
        if region['target_sha256'] != digest: raise ValueError('Different code-region target')
        decoder = region.get('decoder', 'ghidra-via-rea')
        if decoder == 'capstone-independent':
            source_path = (root/region['byte_source']['path']).resolve()
            if source_path.parent != root: raise ValueError('Byte source outside report')
            validate_independent_region(region, evidence(source_path))
        elif decoder != 'ghidra-via-rea':
            raise ValueError('Unknown region decoder')
        for item in region['instructions'].values():
            instruction = item['instruction']
            if instruction['status'] != 'decoded': continue
            address = int(instruction['address'], 16)
            if len(bytes.fromhex(instruction['bytes'])) != instruction['length']:
                raise ValueError('Region instruction byte count mismatch')
            decoded_starts.add(address)
            decode_sources.setdefault(decoder, set()).add(address)
            decoded_bytes.update(range(address, address+instruction['length']))
        regions.append(dict(path=path.name, seed=region['seed'],
            decoder=decoder, decoder_version=region.get('decoder_version'),
            semantic_status=region['semantic_status'],
            observed_instructions=len(region['instructions']), pending=len(region['pending']),
            remaining_gaps=len(region['gaps'])))
    gap_ranges = sorted((int(gap['start'], 16), int(gap['end_inclusive'], 16))
        for section in body_map for gap in section['ranges_outside_acquired_bodies'])
    gap_starts = [span[0] for span in gap_ranges]
    outside_body_bytes = 0
    for address in decoded_bytes:
        index = bisect.bisect_right(gap_starts, address)-1
        if index >= 0 and address <= gap_ranges[index][1]: outside_body_bytes += 1
    summary = dict(target_sha256=digest, target_bytes=len(binary),
        rea_inventory_evidence=listing['evidence_id'], provider=listing['provider'],
        analysis_profile=listing['analysis_profile'],
        enumerated_functions=len(rows), external_functions=sum(p['external'] is True for p in rows),
        internal_functions=sum(p['external'] is False for p in rows),
        thunks=sum(p['thunk'] is True for p in rows),
        semantically_reviewed=sum(p['semantic_status'] == 'reviewed' for p in rows),
        partially_reviewed=sum(p['semantic_status'] == 'partial' for p in rows),
        acquired_dossiers=len(dossiers), failed_responses=failed_responses,
        functions_with_instruction_only_evidence=len(set(instruction_bodies)-set(dossiers)),
        known_internal_entries_without_body_evidence=missing_bodies,
        body_acquisition_complete_for_current_inventory=not missing_bodies,
        recovered_transport_responses=recovered_errors,
        unrecovered_response_errors=[name for name in failed_responses if name not in recovered_errors],
        executable_file_bytes=sum(s['raw_size'] for s in layout['sections'] if s['executable']),
        executable_zero_fill_bytes=sum(s['executable_zero_fill_bytes'] for s in layout['sections']),
        trailing_file_bytes=layout['trailing_file_bytes'],
        acquired_function_body_executable_bytes=sum(s['acquired_body_union_bytes'] for s in body_map),
        instruction_byte_coverage=None,
        supplemental_code_regions=regions,
        region_unique_decoded_instruction_starts=len(decoded_starts),
        region_decode_sources={name:len(starts) for name,starts in sorted(decode_sources.items())},
        region_decoded_bytes_outside_acquired_bodies=outside_body_bytes,
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
