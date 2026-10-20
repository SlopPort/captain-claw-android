"""Independently walk REZ directory records and compare every payload with Assets."""
import hashlib
from pathlib import Path
import struct

PORT = Path(__file__).resolve().parents[1]


def verify(archive_path, source):
    expected = {p.relative_to(source).as_posix().upper(): p for p in source.rglob('*')
                if p.is_file() and 0 < len(p.suffix[1:]) <= 3}
    seen = set()
    with archive_path.open('rb') as archive:
        archive.seek(127)
        version, root_offset, root_size = struct.unpack('<III', archive.read(12))
        total = archive_path.stat().st_size
        assert version == 1 and root_offset + root_size == total

        def walk(offset, size, prefix):
            assert 168 <= offset <= total and offset + size <= total
            archive.seek(offset)
            records = archive.read(size)
            pos = 0
            while pos < len(records):
                flag, start, length, _ = struct.unpack_from('<IIII', records, pos)
                name_start = pos + (16 if flag else 28)
                name_end = records.index(0, name_start)
                name = records[name_start:name_end].decode('ascii')
                if flag:
                    walk(start, length, prefix + name + '/')
                    pos = name_end + 1
                else:
                    ext = records[pos+20:pos+24].rstrip(b'\0')[::-1].decode('ascii')
                    key = prefix + name + '.' + ext
                    assert key not in seen and key in expected, key
                    assert start >= 168 and start + length <= offset, key
                    archive.seek(start)
                    actual = hashlib.sha256(archive.read(length)).digest()
                    with expected[key].open('rb') as original:
                        wanted = hashlib.file_digest(original, 'sha256').digest()
                    assert actual == wanted, key
                    seen.add(key)
                    pos = name_end + 2
            assert pos == size

        walk(root_offset, root_size, '')
    assert seen == set(expected)
    print(f'PASS: {len(seen)} REZ entries match original files byte for byte')


if __name__ == '__main__':
    verify(PORT / 'build/game-data/CLAW.REZ', PORT.parent / 'Assets')
