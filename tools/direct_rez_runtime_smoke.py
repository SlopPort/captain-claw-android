"""Boot the user's complete REZ with exact APK support; restore all user data.

Checks the direct-import runtime format, not a human system-picker interaction.
Reports contain proprietary local data and must never enter source archives.
"""
import subprocess
import sys
import zipfile
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    report=PORT/'reports/direct-rez-0.4.8';report.mkdir(parents=True,exist_ok=True)
    names=('CLAW.REZ','ASSETS.ZIP','config.xml','clacon.ttf','console02.tga','SAVES.XML')
    adb('shell','am','force-stop','pl.pazur.port')
    for name in names:adb('pull',REMOTE+name,str(report/name))
    stage=report/'input';stage.mkdir(exist_ok=True)
    with zipfile.ZipFile(PORT/'app/build/outputs/apk/debug/app-debug.apk') as apk:
        for name in ('ASSETS.ZIP','config.xml','console02.tga'):
            (stage/name).write_bytes(apk.read('assets/import-support/'+name))
    adb('pull','/system/fonts/Roboto-Regular.ttf',str(stage/'clacon.ttf'))
    try:
        # This CrazyHook PC installation has a 168-byte stub CLAW.REZ and loose
        # Assets/. Use the complete archive already supplied by the user instead.
        adb('push',str(report/'CLAW.REZ'),REMOTE+'CLAW.REZ')
        for name in ('ASSETS.ZIP','config.xml','console02.tga','clacon.ttf'):adb('push',str(stage/name),REMOTE+name)
        subprocess.run([sys.executable,str(PORT/'tools/level_boot_smoke.py'),'--levels','1','14','--frequency','22050','--effects-on','--hold-seconds','12','--report','direct-rez-boot-0.4.8'],check=True)
        print('Direct complete REZ + APK support runtime: PASS')
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in names:adb('push',str(report/name),REMOTE+name)
        print('Original complete data/config/saves restored')


if __name__=='__main__':main()
