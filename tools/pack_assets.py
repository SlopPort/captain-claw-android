"""Repack local loose game assets into the REZ layout consumed by libwap.

Writes a separate test-data directory; never changes the original installation.
"""
from pathlib import Path
import argparse
import json
import shutil
import struct
import xml.etree.ElementTree as ET
import zipfile
from pack_support_assets import pack_support_assets

PORT = Path(__file__).resolve().parents[1]
ROOT = PORT.parent


def build_rez(source, destination, header_path=None):
    skipped = []
    count = 0
    with destination.open('wb') as out:
        out.write(bytes(168))

        def directory(path):
            nonlocal count
            entries = []
            for child in sorted(path.iterdir(), key=lambda p: p.name.casefold()):
                if child.is_dir():
                    offset, size = directory(child)
                    entries.append(struct.pack('<IIII', 1, offset, size, 0)
                                   + child.name.upper().encode('ascii') + b'\0')
                elif child.is_file():
                    extension = child.suffix[1:].upper()
                    if not extension or len(extension) > 3:
                        skipped.append(child.relative_to(source).as_posix())
                        continue
                    offset = out.tell()
                    with child.open('rb') as inp:
                        shutil.copyfileobj(inp, out, 1024 * 1024)
                    size = out.tell() - offset
                    count += 1
                    entries.append(struct.pack('<IIIII', 0, offset, size, 0, count)
                                   + extension[::-1].encode('ascii').ljust(4, b'\0')
                                   + struct.pack('<I', 0)
                                   + child.stem.upper().encode('ascii') + b'\0\0')
            offset = out.tell()
            for entry in entries:
                out.write(entry)
            return offset, out.tell() - offset

        offset, size = directory(source)
        if out.tell() >= 2**31:
            raise ValueError('Archive exceeds signed offsets supported by upstream')
        out.seek(0)
        header = (header_path or ROOT / 'CLAW.REZ').read_bytes()[:127]
        out.write(header)
        out.write(struct.pack('<III', 1, offset, size))
    return {'packed': count, 'skipped': skipped, 'bytes': destination.stat().st_size}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root',type=Path,default=ROOT,help='Own game installation with CLAW.REZ and optional loose Assets/')
    args=parser.parse_args()
    dest = PORT / 'build/game-data'
    dest.mkdir(parents=True, exist_ok=True)
    game_root=args.game_root.resolve()
    if not (game_root/'CLAW.REZ').is_file(): parser.error('Own CLAW.REZ not found in --game-root')
    if (game_root/'Assets').is_dir():
        report = build_rez(game_root / 'Assets', dest / 'CLAW.REZ',game_root/'CLAW.REZ')
    else:
        shutil.copyfile(game_root/'CLAW.REZ',dest/'CLAW.REZ')
        report={'mode':'copy_original_rez','bytes':(dest/'CLAW.REZ').stat().st_size,'skipped':[]}
    upstream = PORT / 'upstream/OpenClaw/Build_Release'
    pack_support_assets(dest / 'ASSETS.ZIP')
    for name in ('clacon.ttf', 'console02.tga'):
        shutil.copyfile(upstream / name, dest / name)
    tree = ET.parse(PORT / 'profiles/low-end.xml')
    tree.find('Audio/MusicOn').text = 'true'
    tree.find('Assets/AssetsFolder').text = './'
    tree.write(dest / 'config.xml', encoding='utf-8', xml_declaration=True)
    with zipfile.ZipFile(dest.parent / 'game-data.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in ('CLAW.REZ', 'ASSETS.ZIP', 'config.xml', 'clacon.ttf', 'console02.tga'):
            archive.write(dest / name, name)
    (PORT / 'reports').mkdir(parents=True,exist_ok=True)
    (PORT / 'reports/asset-pack.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
