"""Independent x86-32 traversal of exact bytes acquired through REA.

OpenAI Codex (LLM). Decoder output is not REA instruction Evidence, recovered
source, a discovered function, or a semantic pass. Commercial output stays in
reports. Calls assume a possible fallthrough but retain returnability gaps.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

import capstone
from capstone import x86_const as x86
from rea_audit_inventory import PORT, evidence


def decode(data, base, seeds, maximum=4096):
    engine = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    engine.detail = True
    pending = deque(seeds)
    result, gaps, byte_owners = {}, [], {}
    end = base + len(data)
    if maximum < 1 or not seeds or any(not base <= seed < end for seed in seeds):
        raise ValueError('Invalid traversal limits/seeds')
    while pending and len(result) < maximum:
        address = pending.popleft()
        if hex(address) in result:
            continue
        if not base <= address < end:
            gaps.append(dict(address=hex(address), reason='edge-outside-selected-region'))
            continue
        instruction = next(engine.disasm(data[address-base:address-base+15], address, count=1), None)
        if instruction is None:
            result[hex(address)] = dict(address=hex(address), status='undecodable',
                                        bytes='', length=0)
            gaps.append(dict(address=hex(address), reason='instruction-not-decoded'))
            continue
        targets = []
        flow = dict(kind='fallthrough', conditional=False, computed=False, direct_destinations=[])
        next_address = address + instruction.size
        if instruction.group(capstone.CS_GRP_RET) or instruction.group(capstone.CS_GRP_IRET):
            flow['kind'] = 'return'
        elif (instruction.group(capstone.CS_GRP_INT) or instruction.group(capstone.CS_GRP_PRIVILEGE)
              or instruction.mnemonic in ('ud2', 'hlt', 'syscall', 'sysenter', 'sysexit', 'sysret', 'rsm')):
            flow['kind'] = 'unavailable'
            gaps.append(dict(address=hex(address), reason='exception-or-privileged-flow-unresolved'))
        elif instruction.id in (x86.X86_INS_LJMP, x86.X86_INS_LCALL):
            flow['kind'] = 'unavailable'
            gaps.append(dict(address=hex(address), reason='far-transfer-unresolved'))
        elif instruction.group(capstone.CS_GRP_CALL):
            flow['kind'] = 'call'
            targets.append(next_address)
            gaps.append(dict(address=hex(address), reason='call-target-and-returnability-not-reviewed'))
        elif instruction.group(capstone.CS_GRP_JUMP) or instruction.mnemonic in ('loop', 'loope', 'loopne', 'jcxz', 'jecxz'):
            flow.update(kind='jump', conditional=instruction.id != x86.X86_INS_JMP)
            if flow['conditional']:
                targets.append(next_address)
        elif instruction.group(capstone.CS_GRP_BRANCH_RELATIVE):
            flow['kind'] = 'unavailable'
            gaps.append(dict(address=hex(address), reason='unsupported-relative-control-flow'))
        else:
            targets.append(next_address)
        if flow['kind'] in ('jump', 'call'):
            if len(instruction.operands) == 1 and instruction.operands[0].type == x86.X86_OP_IMM:
                target = instruction.operands[0].imm & 0xffffffff
                flow['direct_destinations'] = [hex(target)]
                if flow['kind'] == 'jump':
                    targets.append(target)
            else:
                flow['computed'] = True
                if flow['kind'] == 'jump':
                    gaps.append(dict(address=hex(address), reason='jump-destination-unresolved'))
        overlaps = set()
        for byte in range(address, next_address):
            overlaps.update(byte_owners.get(byte, set()))
            byte_owners.setdefault(byte, set()).add(address)
        if overlaps:
            gaps.append(dict(address=hex(address), reason='overlapping-instruction-boundaries',
                             other_starts=[hex(value) for value in sorted(overlaps)]))
        result[hex(address)] = dict(address=hex(address), status='decoded', bytes=instruction.bytes.hex(),
            length=instruction.size, raw_disassembly=instruction.mnemonic+' '+instruction.op_str, flow=flow)
        for target in targets:
            if base <= target < end:
                if hex(target) not in result and target not in pending:
                    pending.append(target)
            else:
                gaps.append(dict(address=hex(address), reason='edge-outside-selected-region', target=hex(target)))
    return dict(instructions=result, pending=[hex(value) for value in pending], gaps=gaps,
                completed_bounded_worklist=not pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--bytes-response', required=True)
    parser.add_argument('--seed', required=True)
    parser.add_argument('--maximum', type=int, default=4096)
    args = parser.parse_args()
    root = (PORT/'reports'/args.report).resolve()
    if not root.is_relative_to((PORT/'reports').resolve()):
        parser.error('Private reports only')
    source = (root/args.bytes_response).resolve()
    if source.parent != root:
        parser.error('Use a response in this audit report')
    record = evidence(source)
    digest = hashlib.sha256((PORT.parent/'CLAW.EXE').read_bytes()).hexdigest()
    if record['operation'] != 'read_bytes' or record['subject']['digest']['sha256'] != digest:
        raise ValueError('Wrong byte operation/target')
    value = record['normalized_result']
    data = bytes.fromhex(value['bytes_hex'])
    if not value['complete'] or len(data) != value['requested_bytes'] or len(data) != value['returned_bytes']:
        raise ValueError('Incomplete byte source')
    base, seed = int(value['address'],16), int(args.seed,16)
    output = root/('region-capstone-'+hex(seed)+'.json')
    if output.exists():
        raise ValueError('Preserve existing traversal; use an explicit reviewed follow-up')
    state = decode(data, base, [seed], args.maximum)
    state.update(target_sha256=digest, seed=hex(seed), start=hex(base), end=hex(base+len(data)-1),
                 decoder='capstone-independent', decoder_version=capstone.__version__,
                 byte_source=dict(path=source.name, evidence_id=record['evidence_id'],
                                  sha256=hashlib.sha256(data).hexdigest()), semantic_status='unreviewed')
    state['instructions'] = {address:dict(byte_evidence_id=record['evidence_id'], instruction=instruction)
                             for address,instruction in state['instructions'].items()}
    output.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(path=output.name, decoder=state['decoder'], instructions=len(state['instructions']),
                         pending=len(state['pending']), gaps=len(state['gaps']), semantic_status='unreviewed')))


if __name__ == '__main__':
    main()
