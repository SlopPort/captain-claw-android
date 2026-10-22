"""Package XML support and original generated help/credits, without game art/fonts.

Direct REZ import follows the UX of arthurboss/claw-web (GPLv3).
Android implementation by Codex; no upstream game bitmaps are copied here.
"""
from pathlib import Path
import re
import struct
import zlib
import zipfile
from credits_png import credit_cards

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
    generated={name:png() for name in ('CONTROLS/touchscreen_title.png','CONTROLS/touchscreen_img.png')}
    generated.update(zip(('CREDITS/credits_ja.png','CREDITS/credits_pavel.png'),credit_cards()))
    # PNG menu resources belong to this support archive, unlike original PCX/PID
    # art supplied in the user's REZ. Missing credit PNGs previously crashed a
    # return to the main menu, because menu initialization loads every page.
    referenced={match.decode('ascii').lstrip('/').lower()
                for path in files.values()
                for match in re.findall(rb'/[^<>"\r\n]+\.png',path.read_bytes(),re.I)}
    missing=referenced-{name.lower() for name in generated}
    if missing:raise RuntimeError('Missing redistributable support PNGs: '+', '.join(sorted(missing)))
    with zipfile.ZipFile(dest/'ASSETS.ZIP','w',zipfile.ZIP_DEFLATED) as archive:
        def write(name,data):
            # Stable metadata avoids rewriting the atomic engine bundle when
            # an unrelated APK rebuild has not changed any support content.
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
            info.create_system=3
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,data)
        for name,p in sorted(files.items()):write(name,p.read_bytes())
        for name,data in sorted(generated.items()):write(name,data)
    (dest/'config.xml').write_bytes((PORT/'profiles/low-end.xml').read_bytes())
    # Original generated flat console backdrop, 2x2 uncompressed true-colour TGA.
    (dest/'console02.tga').write_bytes(struct.pack('<BBBHHBHHHHBB',0,0,2,0,0,0,0,0,2,2,24,32)+bytes([30,24,18])*4)


if __name__=='__main__':main()
