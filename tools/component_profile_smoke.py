"""Opt-in component timing; instrumentation affects frame timings."""
import argparse
import json
import copy
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',type=int,choices=range(1,15),default=13)
    parser.add_argument('--report',default='component-profile-0.4.8')
    args=parser.parse_args()
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:raise RuntimeError('Existing mailbox')
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    tree=ET.parse(report/'config.xml');tree.find('DebugOptions/SkipMenu').text='true';tree.find('DebugOptions/SkipMenuToLevel').text=str(args.level)
    flag=tree.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(tree.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true';tree.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
    saves=ET.parse(report/'SAVES.XML')
    if not any(level.findtext('LevelNumber')==str(args.level) for level in saves.findall('Level')):
        level=copy.deepcopy(saves.find('Level'));level.find('LevelNumber').text=str(args.level);saves.getroot().append(level)
    saves.write(report/'saves-test.xml',encoding='utf-8',xml_declaration=True)
    pid=''
    try:
        adb('push',str(report/'test.xml'),REMOTE+'config.xml');adb('push',str(report/'saves-test.xml'),REMOTE+'SAVES.XML');adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity');time.sleep(2)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
        def logs():return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
        deadline=time.monotonic()+45
        while 'Level loaded !' not in logs() and time.monotonic()<deadline:time.sleep(.5)
        assert 'Level loaded !' in logs();time.sleep(10)
        (report/'command.tmp').write_text('profile|componentprofile\n',encoding='ascii')
        adb('push',str(report/'command.tmp'),REMOTE+'combat-command.tmp');adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        time.sleep(7);log=logs();(report/'native.log').write_text(log,encoding='utf-8')
        rows=[{'component':n,'total_ms_in_5_seconds':float(ms)} for n,ms in re.findall(r'Pazur component sample: (\S+) total=([\d.]+)',log)]
        assert rows and 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
        (report/'results.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
    finally:
        if pid:(report/'native.log').write_text(adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime'),encoding='utf-8')
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):adb('shell','rm','-f',REMOTE+name)


if __name__=='__main__':main()
