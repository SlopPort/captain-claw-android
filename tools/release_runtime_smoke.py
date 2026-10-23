"""Isolated signed release-variant startup; never replace the debug installation.

OpenAI Codex (LLM). Requires separately built runtimePackage=pl.pazur.port.releasecheck.
Only this task's new app is installed/uninstalled. Copies the allocated device's
own data locally; original package/files remain unchanged. No campaign traversal,
input, shell permission adoption, USB changes or claim of exact production APK QA.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, PORT, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--aapt',type=Path,required=True)
    parser.add_argument('--abi',choices=('arm64-v8a','armeabi-v7a'),default='arm64-v8a')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select one allocated phone')
    package='pl.pazur.port.releasecheck';root='/sdcard/Android/data/'+package+'/files/'
    if adb('shell','pm','path',package,check=False).strip():raise RuntimeError('Existing releasecheck installation; do not replace it')
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    config=adb('exec-out','cat',REMOTE+'config.xml')
    saves=adb('exec-out','cat',REMOTE+'SAVES.XML')
    original_rez=adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]
    badging=subprocess.check_output([str(args.aapt),'dump','badging',str(args.apk)],text=True)
    assert "package: name='"+package+"'" in badging,'Wrong APK identity; refusing installation'
    before={n:adb('shell','sha256sum',REMOTE+n).split()[0] for n in ('CLAW.REZ','config.xml','SAVES.XML')}
    installed=False;rows=[]
    try:
        adb('install','--abi',args.abi,str(args.apk));installed=True
        package_info=adb('shell','dumpsys','package',package)
        (report/'package.txt').write_text(package_info,encoding='utf-8')
        assert 'primaryCpuAbi='+args.abi in package_info,'Unexpected installed ABI'
        adb('shell','am','start','-W','-n',package+'/pl.pazur.port.LauncherActivity')
        until=time.monotonic()+20
        while time.monotonic()<until:
            if subprocess.run(['adb','shell','test','-d',root],capture_output=True).returncode==0:break
            time.sleep(.2)
        else:raise RuntimeError('Isolated app directory did not initialize')
        adb('shell','am','force-stop',package)
        for name in ('CLAW.REZ','ASSETS.ZIP','console02.tga','clacon.ttf','SAVES.XML'):
            adb('shell','cp',REMOTE+name,root+name)
        for level in (None,1,14):
            adb('shell','am','force-stop',package)
            tree=ET.fromstring(config)
            tree.find('DebugOptions/SkipMenu').text='false' if level is None else 'true'
            tree.find('DebugOptions/SkipMenuToLevel').text=str(level or 1)
            preview=tree.find('DebugOptions/PreviewIncompleteLevel14')
            if preview is not None:preview.text='false'
            for field,value in [('MusicOn','true'),('SoundOn','true'),('Frequency','22050')]:tree.find('Audio/'+field).text=value
            path=report/'config.xml';ET.ElementTree(tree).write(path,encoding='utf-8',xml_declaration=True)
            adb('push',str(path),root+'config.xml')
            if level==14:
                progress=ET.fromstring(saves)
                if not any(n.findtext('LevelNumber')=='14' for n in progress.findall('Level')):
                    import copy
                    entry=copy.deepcopy(progress.find('Level'));entry.find('LevelNumber').text='14';progress.append(entry)
                path=report/'saves-fixture.xml';ET.ElementTree(progress).write(path,encoding='utf-8',xml_declaration=True)
                adb('push',str(path),root+'SAVES.XML')
            adb('shell','am','start','-W','-n',package+'/pl.pazur.port.LauncherActivity')
            pid=adb('shell','pidof',package).strip();assert pid.isdigit(),'Isolated game not running'
            start=time.monotonic();evidence=''
            marker='Changing to: 3' if level is None else 'Level name: Claw - Level '+str(level)
            while time.monotonic()-start<60:
                evidence=adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
                if marker in evidence and (level is None or re.search(r'Pazur audio PCM: peak=[1-9]\d*',evidence)):break
                time.sleep(.5)
            label='menu' if level is None else 'level'+str(level)
            (report/(label+'.log')).write_text(evidence,encoding='utf-8')
            assert marker in evidence and (level is None or re.search(r'Pazur audio PCM: peak=[1-9]\d*',evidence)),'Startup/music evidence missing: '+label
            assert 'Fatal signal' not in evidence and 'FATAL EXCEPTION' not in evidence,evidence[-2000:]
            assert adb('shell','pidof',package).strip()==pid,'Process changed'
            rows.append(dict(case=label,passed=True,music_pcm=level is not None))
    finally:
        if installed:
            adb('shell','am','force-stop',package)
            adb('uninstall',package)
        assert adb('exec-out','cat',REMOTE+'config.xml')==config,'Original config changed'
        assert adb('exec-out','cat',REMOTE+'SAVES.XML')==saves,'Original save changed'
        assert adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]==original_rez,'Original REZ changed'
        for name,digest in before.items():assert adb('shell','sha256sum',REMOTE+name).split()[0]==digest,'Original bytes changed: '+name
    result=dict(passed=True,apk_sha256=hashlib.sha256(args.apk.read_bytes()).hexdigest(),cases=rows,
        separate_package=True,requested_abi=args.abi,package_primary_abi_verified=True,process_maps_checked=False,production_identity_tested=False,natural_playthrough=False,original_files_unchanged=True)
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
