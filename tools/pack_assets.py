"""Repack local loose game assets into the REZ layout consumed by libwap.

Writes a separate test-data directory; never changes the original installation.
"""
from pathlib import Path
import argparse
import json
import os
import tempfile
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



PACKAGE_FILES = ('CLAW.REZ', 'ASSETS.ZIP', 'config.xml', 'clacon.ttf', 'console02.tga')


class GameDataInputError(ValueError):
    """Stable error category lets the window translate guidance without parsing text."""
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def validate_game_root(game_root):
    """Fail before downloads/copying when the selected installation is incomplete."""
    source = Path(game_root) / 'CLAW.REZ'
    if not source.is_file():
        raise GameDataInputError('missing', 'CLAW.REZ was not found in the selected game folder.')
    if source.stat().st_size < 168:
        raise GameDataInputError('truncated', 'CLAW.REZ is truncated (less than 168 bytes). Select your original game installation.')
    if source.stat().st_size == 168 and not (Path(game_root) / 'Assets').is_dir():
        raise GameDataInputError('placeholder', 'This CLAW.REZ is only a placeholder. Select it beside the original Assets folder.')
    assets = Path(game_root) / 'Assets'
    if source.stat().st_size > 168:
        if assets.is_dir():
            raise GameDataInputError('mixed', 'A full CLAW.REZ and loose Assets were found. This tool does not merge partial overrides. Import the full REZ directly to play its contents, or select a placeholder beside a complete loose-data installation.')
        try:
            validate_rez(source)
        except ValueError as error:
            raise GameDataInputError('invalid', str(error)) from error
    elif not any(path.is_file() for path in assets.rglob('*')):
        raise GameDataInputError('empty', 'The Assets folder is empty. Select a complete loose-data installation.')



def validate_rez(path):
    """Match the Android importer's outer-directory check, not full game coverage."""
    size = path.stat().st_size
    with path.open('rb') as source:
        header = source.read(168)
    if size <= 168 or len(header) < 168:
        raise ValueError('The prepared REZ is empty or incomplete. Check the original Assets folder.')
    version, offset, length = struct.unpack_from('<III', header, 127)
    if version != 1 or offset < 168 or length < 16 or offset + length > size:
        raise ValueError('Invalid REZ directory. Select a complete original CLAW.REZ or its loose Assets installation.')


def write_game_archive(directory, destination):
    """Publish only a closed, CRC-checked ZIP; old output survives write failure.

    The temporary ZIP is on the destination filesystem so os.replace is atomic.
    Abrupt process termination can leave a temporary file, never a partial final
    ZIP. A completed replacement is either the previous valid file or the new one.
    """
    destination = Path(destination)
    with tempfile.NamedTemporaryFile(prefix='game-data-', suffix='.tmp',
                                     dir=destination.parent, delete=False) as temporary:
        pending = Path(temporary.name)
    try:
        with zipfile.ZipFile(pending, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in PACKAGE_FILES:
                archive.write(directory / name, name)
        with zipfile.ZipFile(pending) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise ValueError('ZIP verification failed: ' + bad)
        with pending.open('rb+') as finished:
            os.fsync(finished.fileno())
        os.replace(pending, destination)
    finally:
        pending.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root',type=Path,default=ROOT,help='Own game installation with CLAW.REZ and optional loose Assets/')
    args=parser.parse_args()
    dest = PORT / 'build/game-data'
    dest.mkdir(parents=True, exist_ok=True)
    game_root=args.game_root.resolve()
    validate_game_root(game_root)
    if (game_root/'CLAW.REZ').resolve() == (dest/'CLAW.REZ').resolve():
        parser.error('Select the original game folder, not the generated build/game-data folder.')
    if (game_root/'Assets').is_dir():
        report = build_rez(game_root / 'Assets', dest / 'CLAW.REZ',game_root/'CLAW.REZ')
    else:
        shutil.copyfile(game_root/'CLAW.REZ',dest/'CLAW.REZ')
        report={'mode':'copy_original_rez','bytes':(dest/'CLAW.REZ').stat().st_size,'skipped':[]}
    validate_rez(dest / 'CLAW.REZ')
    upstream = PORT / 'upstream/OpenClaw/Build_Release'
    pack_support_assets(dest / 'ASSETS.ZIP')
    for name in ('clacon.ttf', 'console02.tga'):
        shutil.copyfile(upstream / name, dest / name)
    tree = ET.parse(PORT / 'profiles/low-end.xml')
    tree.find('Audio/MusicOn').text = 'true'
    tree.find('Assets/AssetsFolder').text = './'
    tree.write(dest / 'config.xml', encoding='utf-8', xml_declaration=True)
    write_game_archive(dest, dest.parent / 'game-data.zip')
    # Diagnostics are optional; inability to save a report must not turn a valid
    # published ZIP into an apparent packaging failure in the preparation window.
    try:
        (PORT / 'reports').mkdir(parents=True, exist_ok=True)
        (PORT / 'reports/asset-pack.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    except OSError as error:
        print('Warning: ZIP is ready, but the local diagnostic report could not be saved: ' + str(error))
    print(json.dumps(report))


if __name__ == '__main__':
    main()
