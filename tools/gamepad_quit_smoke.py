"""Exercise real SDL virtual-controller menu exit; preserve config and save files.

No global Android key injection. Uses only the game's opt-in command mailbox.
"""
from pathlib import Path
import json
import subprocess
import time
import xml.etree.ElementTree as ET

PORT=Path(__file__).resolve().parents[1]
REPORT=PORT/'reports/gamepad-quit-0.4.4'
REMOTE='/sdcard/Android/data/pl.pazur.port/files/'


def adb(*args, check=True):
    return subprocess.run(['adb',*args],capture_output=True,text=True,check=check,stdin=subprocess.DEVNULL).stdout


def main():
    REPORT.mkdir(parents=True,exist_ok=True)
    # Refuse to overwrite another diagnostic session's command.
    for name in ('combat-command.txt','combat-response.txt'):
        if 'No such file' not in adb('shell','ls',REMOTE+name,check=False):
            probe=subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True)
            if probe.returncode==0: raise RuntimeError('Existing mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'): adb('pull',REMOTE+name,str(REPORT/name))
    config=ET.parse(REPORT/'config.xml')
    config.find('DebugOptions/SkipMenu').text='false'
    debug=config.find('DebugOptions')
    flag=debug.find('PreviewIncompleteLevel14')
    if flag is None: flag=ET.SubElement(debug,'PreviewIncompleteLevel14')
    flag.text='true'
    config.write(REPORT/'config-test.xml',encoding='utf-8',xml_declaration=True)
    ticket=0

    def command(value):
        nonlocal ticket
        ticket+=1
        tag='quit-smoke-'+str(ticket)
        temporary=REPORT/'command.tmp'
        temporary.write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(temporary),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+8
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False): return
            time.sleep(.1)
        raise RuntimeError('No acknowledgement: '+value)

    results=[]
    try:
        adb('push',str(REPORT/'config-test.xml'),REMOTE+'config.xml')
        for attempt in range(3):
            adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity')
            time.sleep(5)
            pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
            before=adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
            command('padvirtual attach')
            command('padvirtual button b 1')
            command('padvirtual button b 0')
            command('padvirtual button a 1')
            time.sleep(3)
            log=adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
            # Logs can retain the same process across SDLActivity relaunches.
            delta=log[len(before):] if log.startswith(before) else log
            (REPORT/f'attempt-{attempt+1}.log').write_text(delta,encoding='utf-8')
            assert 'Terminating...' in delta,delta
            assert 'Fatal signal' not in delta and 'FORTIFY:' not in delta and 'FATAL EXCEPTION' not in delta,delta
            activity=adb('shell','dumpsys','activity','activities')
            resumed=[line for line in activity.splitlines() if 'mResumedActivity:' in line]
            assert not any('pl.pazur.port' in line for line in resumed),resumed
            results.append({'attempt':attempt+1,'terminated':True,'no_fatal_log':True,'activity_finished':True})
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'): adb('push',str(REPORT/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):
            adb('shell','rm','-f',REMOTE+name)
        (REPORT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
