"""Isolated signed release-variant startup; never replace the debug installation.

OpenAI Codex (LLM). Requires separately built runtimePackage=pl.pazur.port.releasecheck.
Only this task's new app is installed/uninstalled. Copies the allocated device's
own data locally; original package/files remain unchanged. No campaign traversal,
input, shell permission adoption, USB changes or claim of exact production APK QA.
"""
import argparse
import copy
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, PORT, REMOTE
from android_package import installed_apk_sha256


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--aapt',type=Path,required=True)
    parser.add_argument('--abi',choices=('arm64-v8a','armeabi-v7a'),default='arm64-v8a')
    parser.add_argument('--controls',action='store_true',help='Explicit diagnostic jump/exit/score/save fixture in isolated package; not a natural clear')
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
    local_hash=hashlib.sha256(args.apk.read_bytes()).hexdigest()
    installed=False;rows=[];installed_hash=None;ticket=0
    def command(value):
        nonlocal ticket
        ticket+=1;tag='release-'+str(ticket)
        (report/'command.tmp').write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(report/'command.tmp'),root+'combat-command.tmp')
        adb('shell','mv',root+'combat-command.tmp',root+'combat-command.txt')
        until=time.monotonic()+12
        while time.monotonic()<until:
            if tag+'|done' in adb('shell','cat',root+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No isolated release response: '+value)
    def logs(pid):return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')

    try:
        adb('install','--abi',args.abi,str(args.apk));installed=True
        installed_hash=installed_apk_sha256(package);assert installed_hash==local_hash,'Installed release differs from requested APK'
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
            if args.controls:tree.find('GlobalOptions/LoadAllLevelSaves').text='false'
            preview=tree.find('DebugOptions/PreviewIncompleteLevel14')
            if preview is None:preview=ET.SubElement(tree.find('DebugOptions'),'PreviewIncompleteLevel14')
            preview.text='true' if args.controls and level==1 else 'false'
            for field,value in [('MusicOn','true'),('SoundOn','true'),('Frequency','22050')]:tree.find('Audio/'+field).text=value
            path=report/'config.xml';ET.ElementTree(tree).write(path,encoding='utf-8',xml_declaration=True)
            adb('push',str(path),root+'config.xml')
            if args.controls:
                # Own-app cloned checkpoint-zero fixture, never the user's save.
                progress=ET.Element('GameSaves');entry=copy.deepcopy(ET.fromstring(saves).find('Level'))
                entry.find('LevelNumber').text='1'
                checkpoint=copy.deepcopy(entry.find('Checkpoint'))
                for node in list(entry.findall('Checkpoint')):entry.remove(node)
                for key,value in [('CheckpointNumber',0),('Score',0),('Health',100),('Lives',3),('BulletCount',10),('MagicCount',5),('DynamiteCount',3)]:checkpoint.find(key).text=str(value)
                entry.append(checkpoint);progress.append(entry)
                fixture=report/'saves-checkpoint-zero.xml';ET.ElementTree(progress).write(fixture,encoding='utf-8',xml_declaration=True)
                adb('push',str(fixture),root+'SAVES.XML')
            if level==14:
                progress=ET.parse(report/'saves-checkpoint-zero.xml').getroot() if args.controls else ET.fromstring(saves)
                if not any(n.findtext('LevelNumber')=='14' for n in progress.findall('Level')):
                    entry=copy.deepcopy(progress.find('Level'));entry.find('LevelNumber').text='14';progress.append(entry)
                path=report/'saves-fixture.xml';ET.ElementTree(progress).write(path,encoding='utf-8',xml_declaration=True)
                adb('push',str(path),root+'SAVES.XML')
            adb('shell','am','start','-W','-n',package+'/pl.pazur.port.LauncherActivity')
            pid=adb('shell','pidof',package).strip();assert pid.isdigit(),'Isolated game not running'
            start=time.monotonic();evidence=''
            marker='Changing to: 3' if level is None else 'Level name: Claw - Level '+str(level)
            while time.monotonic()-start<60:
                evidence=logs(pid)
                if marker in evidence and (level is None or re.search(r'Pazur audio PCM: peak=[1-9]\d*',evidence)):break
                time.sleep(.5)
            label='menu' if level is None else 'level'+str(level)
            (report/(label+'.log')).write_text(evidence,encoding='utf-8')
            assert marker in evidence and (level is None or re.search(r'Pazur audio PCM: peak=[1-9]\d*',evidence)),'Startup/music evidence missing: '+label
            assert 'Fatal signal' not in evidence and 'FATAL EXCEPTION' not in evidence,evidence[-2000:]
            assert adb('shell','pidof',package).strip()==pid,'Process changed'
            controls=None
            if args.controls and level==1:
                before_progress=subprocess.check_output(['adb','exec-out','cat',root+'SAVES.XML'])
                (report/'progress-before-jump.xml').write_bytes(before_progress)
                assert {node.findtext('LevelNumber') for node in ET.fromstring(before_progress).findall('Level')}=={'1'},'Control fixture already contains unlocked levels'
                time.sleep(3);command('combatjumpmeasure release-jump');command('combatkey jump 100')
                until=time.monotonic()+10
                while 'Pazur jump trace: label=release-jump' not in logs(pid) and time.monotonic()<until:time.sleep(.2)
                trace=re.search(r'Pazur jump trace: label=release-jump .*?rise=([\d.]+).*?jumps=(\d+)',logs(pid))
                assert trace and float(trace[1])>40 and trace[2]=='1','Release jump failed'
                placements=0
                for attempt in range(3):
                    command('campaignfinish');placements+=1;until=time.monotonic()+6
                    while 'Score screen initialized OK' not in logs(pid) and time.monotonic()<until:time.sleep(.2)
                    if 'Score screen initialized OK' in logs(pid):break
                else:raise RuntimeError('Release exit fixture not collected')
                for attempt in range(12):
                    command('padvirtual tap 320 240');time.sleep(.35)
                    if 'Level name: Claw - Level 2' in logs(pid):break
                assert 'Level name: Claw - Level 2' in logs(pid),'Release score confirmation failed'
                progress_bytes=subprocess.check_output(['adb','exec-out','cat',root+'SAVES.XML'])
                (report/'progress-after-score.xml').write_bytes(progress_bytes)
                assert any(node.findtext('LevelNumber')=='2' for node in ET.fromstring(progress_bytes).findall('Level')),'Release progress not written'
                evidence=logs(pid);(report/(label+'.log')).write_text(evidence,encoding='utf-8')
                controls=dict(jump_rise=float(trace[1]),jump_requested_hold_ms=100,exit_fixture_placements=placements,next_level_started=True,level2_save_written=True)
            rows.append(dict(case=label,passed=True,music_pcm=level is not None,controls=controls))
        assert installed_apk_sha256(package)==installed_hash,'Release package changed during trial'
    finally:
        if installed:
            adb('shell','am','force-stop',package)
            adb('uninstall',package)
        assert adb('exec-out','cat',REMOTE+'config.xml')==config,'Original config changed'
        assert adb('exec-out','cat',REMOTE+'SAVES.XML')==saves,'Original save changed'
        assert adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]==original_rez,'Original REZ changed'
        for name,digest in before.items():assert adb('shell','sha256sum',REMOTE+name).split()[0]==digest,'Original bytes changed: '+name
    result=dict(passed=True,apk_sha256=installed_hash,cases=rows,
        separate_package=True,requested_abi=args.abi,package_primary_abi_verified=True,process_maps_checked=False,production_identity_tested=False,natural_playthrough=False,original_files_unchanged=True,controls_fixture_requested=args.controls)
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
