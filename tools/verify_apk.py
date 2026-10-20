"""Check ABI coverage and ELF LOAD alignment of every ARM64 library."""
import argparse
import json
from pathlib import Path
import struct
import zipfile


def inspect(apk):
    result = []
    with zipfile.ZipFile(apk) as package:
        libs = [name for name in package.namelist() if name.startswith('lib/') and name.endswith('.so')]
        assert {name.split('/')[1] for name in libs} == {'arm64-v8a', 'armeabi-v7a'}
        for name in libs:
            data = package.read(name)
            assert data[:4] == b'\x7fELF' and data[5] == 1, name
            if data[4] == 2:
                phoff = struct.unpack_from('<Q', data, 32)[0]
                entrysize, count = struct.unpack_from('<HH', data, 54)
                segments = []
                for i in range(count):
                    entry = struct.unpack_from('<IIQQQQQQ', data, phoff + i * entrysize)
                    if entry[0] == 1:
                        assert entry[7] >= 16384, name
                        assert entry[2] % 16384 == entry[3] % 16384, name
                        segments.append(entry[7])
                assert segments, name
                result.append({'library': name, 'load_alignments': segments})
            else:
                assert data[4] == 1, name
                result.append({'library': name, 'elf_class': 32})
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.apk), indent=2))
