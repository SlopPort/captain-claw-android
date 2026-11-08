"""Verify an in-place debug upgrade preserves existing game files/preferences.

OpenAI Codex (LLM). Requires an idle, explicitly allocated Android device with
the debuggable main app. Never uninstalls, downgrades or restores stale data.
The test stops the game, takes fresh private backups, installs with -r, and
checks before launching the upgraded app. Runtime checks are a separate step.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from android_package import installed_apk_sha256

PORT=Path(__file__).resolve().parents[1]
PACKAGE='pl.pazur.port'
REMOTE='/sdcard/Android/data/'+PACKAGE+'/files/'
FILES=('CLAW.REZ','ASSETS.ZIP','config.xml','SAVES.XML','clacon.ttf','console02.tga','ui-language.txt')


def adb(*args):
    return subprocess.check_output(['adb',*args],stderr=subprocess.PIPE,timeout=90)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,required=True)
    parser.add_argument('--aapt',type=Path,required=True)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select one allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    report.mkdir(parents=True,exist_ok=False)
    backup=report/'backup';backup.mkdir()
    badging=subprocess.check_output([str(args.aapt),'dump','badging',str(args.apk)],text=True)
    target=re.search(r"^package: name='([^']+)' versionCode='(\d+)'",badging)
    if not target or target[1]!=PACKAGE:raise RuntimeError('Wrong target package; no installation attempted')
    old=re.search(rb'\bversionCode=(\d+)',adb('shell','dumpsys','package',PACKAGE))
    if not old or int(target[2])<=int(old[1]):raise RuntimeError('This must be a real upgrade; no downgrade/same-version trial')
    # run-as is deliberately limited to this user's debuggable test channel.
    # A production install is not removed or replaced to make this check work.
    adb('shell','run-as',PACKAGE,'pwd')
    result=dict(passed=False,old_version_code=int(old[1]),new_version_code=int(target[2]),
                old_apk_sha256=installed_apk_sha256(),new_apk_sha256=hashlib.sha256(args.apk.read_bytes()).hexdigest(),
                uninstalled=False,runtime_tested=False,restored_from_backup=False)

    def snapshot(save=False):
        hashes={}
        for name in FILES:
            exists=adb('shell','if [ -f '+REMOTE+name+' ]; then echo present; fi')
            if b'present' not in exists:continue
            digest=adb('shell','sha256sum',REMOTE+name).split()[0].decode('ascii')
            hashes['external/'+name]=digest
            if save and name in ('config.xml','SAVES.XML','ui-language.txt'):
                content=adb('exec-out','cat',REMOTE+name)
                if hashlib.sha256(content).hexdigest()!=digest:raise RuntimeError('Data changed during backup')
                (backup/name).write_bytes(content)
        names=adb('exec-out','run-as',PACKAGE,'ls','shared_prefs').decode('utf-8').splitlines()
        for name in sorted(names):
            if not name.endswith('.xml'):continue
            if not re.fullmatch(r'[A-Za-z0-9_.-]+\.xml',name):raise RuntimeError('Unexpected preference filename')
            content=adb('exec-out','run-as',PACKAGE,'cat','shared_prefs/'+name)
            hashes['preferences/'+name]=hashlib.sha256(content).hexdigest()
            if save:(backup/('preferences-'+name)).write_bytes(content)
        if 'external/config.xml' not in hashes or 'external/SAVES.XML' not in hashes:
            raise RuntimeError('Expected existing game configuration/progress')
        return hashes

    try:
        adb('shell','am','force-stop',PACKAGE)
        result['before']=snapshot(save=True)
        # Empty preferences do not prove preservation of existing values.
        result['private_preference_files_checked']=sum(name.startswith('preferences/') for name in result['before'])
        result['private_preferences_tested']=result['private_preference_files_checked']>0
        install=subprocess.run(['adb','install','-r',str(args.apk)],capture_output=True,timeout=180)
        (report/'install.txt').write_bytes(install.stdout+install.stderr)
        result['after']=snapshot()
        result['user_files_unchanged']=result['before']==result['after']
        if install.returncode:raise RuntimeError('Upgrade refused; see private install log; no uninstall attempted')
        result['installed_apk_sha256']=installed_apk_sha256()
        if result['installed_apk_sha256']!=result['new_apk_sha256']:raise RuntimeError('Installed APK identity mismatch')
        if not result['user_files_unchanged']:raise RuntimeError('User data changed; backups retained, no automatic overwrite')
        result['passed']=True
    finally:
        (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('before','after')}))


if __name__=='__main__':main()
