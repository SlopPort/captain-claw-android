"""Read-only inventory of the Windows installation; no third-party dependencies."""
import argparse
import collections
import hashlib
import json
import struct
from pathlib import Path


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pe_header(path):
    with path.open('rb') as stream:
        dos = stream.read(64)
        if len(dos) < 64 or dos[:2] != b'MZ':
            return {'error': 'not a DOS/PE executable'}
        offset = struct.unpack_from('<I', dos, 60)[0]
        stream.seek(offset)
        header = stream.read(24)
        if len(header) != 24 or header[:4] != b'PE\0\0':
            return {'error': 'missing PE header'}
        machine, sections = struct.unpack_from('<HH', header, 4)
        return {'machine': hex(machine), 'architecture': {
            0x14c: 'x86', 0x8664: 'x86_64', 0xaa64: 'arm64'
        }.get(machine, 'unknown'), 'sections': sections}


def audit(root):
    assets = root / 'Assets'
    files = sorted(p for p in assets.rglob('*') if p.is_file())
    counts = collections.Counter()
    sizes = collections.Counter()
    names = collections.defaultdict(list)
    levels = []
    for path in files:
        relative = path.relative_to(assets).as_posix()
        ext = path.suffix.upper() or '<none>'
        counts[ext] += 1
        sizes[ext] += path.stat().st_size
        names[relative.casefold()].append(relative)
        if ext == '.WWD':
            levels.append(relative)
    binaries = {}
    for name in ('CLAW.EXE', 'CrazyHook.dll', 'CLAW.REZ', 'CLAW.FEC'):
        path = root / name
        if path.is_file():
            entry = {'bytes': path.stat().st_size, 'sha256': digest(path)}
            if path.suffix.lower() in ('.exe', '.dll'):
                entry['pe'] = pe_header(path)
            with path.open('rb') as stream:
                entry['first_32_bytes_hex'] = stream.read(32).hex()
            binaries[name] = entry
    return {
        'schema_version': 1,
        'asset_count': len(files),
        'asset_bytes': sum(sizes.values()),
        'by_extension': {ext: {'count': counts[ext], 'bytes': sizes[ext]}
                         for ext in sorted(counts)},
        'levels': levels,
        'case_collisions': [value for value in names.values() if len(value) > 1],
        'binaries': binaries,
        'limitations': [
            'Inventory does not establish compatibility with OpenClaw.',
            'FEC format and CrazyHook behaviors are not decoded.',
            'Android memory use and performance require device measurements.'
        ]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(audit(args.root), indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
    else:
        print(result)
