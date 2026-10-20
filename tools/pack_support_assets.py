"""Pack engine XML assets with explicit local overrides, without duplicate ZIP names."""
from pathlib import Path
import zipfile

PORT = Path(__file__).resolve().parents[1]


def pack_support_assets(destination):
    files = {}
    for root in (PORT / 'upstream/OpenClaw/Build_Release/ASSETS', PORT / 'asset-overrides'):
        for path in sorted(root.rglob('*')):
            if path.is_file():
                name = path.relative_to(root).as_posix()
                files[name.upper()] = (name, path)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for _, (name, path) in sorted(files.items()):
            archive.write(path, name)


if __name__ == '__main__':
    pack_support_assets(PORT / 'build/game-data/ASSETS.ZIP')
