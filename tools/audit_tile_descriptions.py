"""Read-only supplied WWD tile survey; OpenAI Codex (LLM).

Independent parser based on checked libwap/WwdFile.cpp and WwdProperties.
No target execution. Descriptions and identities stay in ignored reports.
This does not establish the installed phone dataset or actual tile placement.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

PORT = Path(__file__).resolve().parents[1]
LIMIT = 128 * 1024 * 1024


def survey(path, level):
    raw = path.read_bytes()
    if len(raw) > LIMIT or len(raw) < 1524 or struct.unpack_from('<I', raw)[0] != 1524:
        raise ValueError('Unsupported WWD header/size')
    planes, descriptions, expected = struct.unpack_from('<III', raw, 736)
    if not 1524 <= planes <= len(raw) or not 0 < expected <= LIMIT:
        raise ValueError('Invalid payload bounds')
    decoder = zlib.decompressobj()
    block = decoder.decompress(raw[planes:], expected + 1)
    if len(block) != expected or not decoder.eof or decoder.unconsumed_tail or decoder.unused_data:
        raise ValueError('Payload length/stream mismatch')
    data = raw[:planes] + block
    if not planes <= descriptions <= len(data) - 32:
        raise ValueError('Description header outside payload')
    header = struct.unpack_from('<8I', data, descriptions)
    if header[0] != 32:
        raise ValueError('Unsupported description header')
    count = header[2]
    if count > (len(data) - descriptions - 32) // 20:
        raise ValueError('Description count exceeds minimum storage')
    at = descriptions + 32
    types, records = {}, []
    for index in range(count):
        if at + 20 > len(data):
            raise ValueError('Truncated description')
        kind, unused, width, height = struct.unpack_from('<4I', data, at)
        at += 16
        types[str(kind)] = types.get(str(kind), 0) + 1
        if kind == 1:
            at += 4  # No outside/rectangle fields exist for SINGLE.
            continue
        if kind != 2 or at + 24 > len(data):
            raise ValueError('Unsupported type or truncated DOUBLE; do not guess its layout')
        outside, inside, left, top, right, bottom = struct.unpack_from('<6i', data, at)
        at += 24
        records.append(dict(index=index, width=width, height=height, outside=outside,
                            inside=inside, rect=[left, top, right, bottom]))
    return dict(level=level, sha256=hashlib.sha256(raw).hexdigest(), count=count,
                types=types, descriptions=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    output = (PORT / 'reports' / args.report).resolve()
    if not output.is_relative_to((PORT / 'reports').resolve()):
        parser.error('Private reports only')
    output.mkdir(parents=True, exist_ok=False)
    rows = [survey(args.assets / f'LEVEL{level}/WORLDS/WORLD.WWD', level)
            for level in range(1, 15)]
    (output / 'survey.json').write_text(json.dumps(dict(
        scope='Local descriptions only; no tile-placement, runtime or installed-data claim',
        levels=rows), indent=2), encoding='utf-8')
    print(json.dumps([dict(level=row['level'], count=row['count'], types=row['types'])
                      for row in rows], indent=2))


if __name__ == '__main__':
    main()
