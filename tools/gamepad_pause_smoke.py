"""Verify SDL virtual-pad pause/resume and release gating on a real level.

Only app-local commands are used; no global Android input injection.
"""
from pathlib import Path
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT

REPORT=PORT/'reports/gamepad-pause-0.4.4'


def main():
    REPORT.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'): adb('pull',REMOTE+name,str(REPORT/name))
    config=ET.parse(REPORT/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text='1'
    debug=config.find('DebugOptions')
    flag=debug.find('PreviewIncompleteLevel14')
    if flag is None: flag=ET.SubElement(debug,'PreviewIncompleteLevel14')
    flag.text='true'
    config.write(REPORT/'config-test.xml',encoding='utf-8',xml_declaration=True)
    ticket=0
    pid=''

    def logs(): return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')

    def command(value):
        nonlocal ticket
        ticket+=1
        tag='pause-smoke-'+str(ticket)
        temporary=REPORT/'command.tmp'
        temporary.write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(temporary),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False): return
            time.sleep(.1)
        raise RuntimeError('No acknowledgement: '+value)

    results=[]
    try:
        adb('push',str(REPORT/'config-test.xml'),REMOTE+'config.xml')
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity')
        time.sleep(2)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
        deadline=time.monotonic()+45
        while 'Level loaded !' not in logs() and time.monotonic()<deadline: time.sleep(.5)
        assert 'Level loaded !' in logs(),'Level failed to load'
        time.sleep(1)
        command('padvirtual attach')
        # Virtual signed trigger axes start at their midpoint; set an actual released value.
        command('padvirtual axis triggerright -32768')
        command('padvirtual button dpright 1')
        command('padvirtual button dpright 0')
        for attempt in range(3):
            before=logs()
            command('padvirtual button start 1')
            time.sleep(.3)
            paused=logs()[len(before):]
            assert 'Pazur pad context: mode=2' in paused,paused
            # Held Start must not bounce repeatedly between play and menu.
            assert 'Pazur pad context: mode=1' not in paused,paused
            command('padvirtual button start 0')
            command('padvirtual button dpdown 1')
            command('padvirtual button dpdown 0')
            menu_log=logs()[len(before):]
            assert 'up=0 down=1' in menu_log,menu_log
            before_resume=logs()
            command('padvirtual button start 1')
            command('padvirtual button start 0')
            time.sleep(.3)
            resumed=logs()[len(before_resume):]
            assert 'Pazur pad context: mode=1' in resumed,resumed
            results.append({'cycle':attempt+1,'paused':True,'menu_direction':True,'resumed':True,'held_start_no_bounce':True})
        command('padvirtual detach')
        log=logs()
        assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,log
        assert pid in adb('shell','pidof','pl.pazur.port').split()
    finally:
        if pid: (REPORT/'native.log').write_text(logs(),encoding='utf-8')
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'): adb('push',str(REPORT/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'): adb('shell','rm','-f',REMOTE+name)
        (REPORT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
