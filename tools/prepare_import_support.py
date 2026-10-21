"""Package XML support only; original game art/fonts never enter this APK asset.

Direct REZ import follows the UX of arthurboss/claw-web (GPLv3).
Android implementation by Codex; no upstream game bitmaps are copied here.
"""
from pathlib import Path
import struct
import zlib
import zipfile

PORT=Path(__file__).resolve().parents[1]


def png():
    # Original neutral placeholder for legacy touchscreen help images. The actual
    # Android controls are drawn natively. Do not redistribute upstream screenshots.
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,32,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+bytes([24,30,40,180])*64)*32))+chunk(b'IEND',b'')


def main():
    dest=PORT/'app/src/main/assets/import-support'
    dest.mkdir(parents=True,exist_ok=True)
    files={}
    for root in (PORT/'upstream/OpenClaw/Build_Release/ASSETS',PORT/'asset-overrides'):
        for p in sorted(root.rglob('*')):
            if p.is_file() and p.suffix.lower()=='.xml':files[p.relative_to(root).as_posix().upper()]=p
    assert 'LEVEL_METADATA/LEVEL14.XML' in files
    with zipfile.ZipFile(dest/'ASSETS.ZIP','w',zipfile.ZIP_DEFLATED) as archive:
        for name,p in sorted(files.items()):archive.writestr(name,p.read_bytes())
        for name in ('CONTROLS/touchscreen_title.png','CONTROLS/touchscreen_img.png'):
            archive.writestr(name,png())
    (dest/'config.xml').write_bytes((PORT/'profiles/low-end.xml').read_bytes())
    # Original generated flat console backdrop, 2x2 uncompressed true-colour TGA.
    (dest/'console02.tga').write_bytes(struct.pack('<BBBHHBHHHHBB',0,0,2,0,0,0,0,0,2,2,24,32)+bytes([30,24,18])*4)


if __name__=='__main__':main()
