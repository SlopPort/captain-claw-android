"""Check held D-pad navigation generates several real menu selection changes."""
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    report=PORT/'reports/gamepad-menu-repeat-0.4.6';report.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    adb('pull',REMOTE+'config.xml',str(report/'config.xml'))
    config=ET.parse(report/'config.xml');config.find('DebugOptions/SkipMenu').text='false'
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true';config.write(report/'config-test.xml',encoding='utf-8',xml_declaration=True)
    ticket=0;pid=''

    def logs():return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')

    def command(value):
        nonlocal ticket
        ticket+=1;tag='menu-repeat-'+str(ticket)
        local=report/'command.tmp';local.write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(local),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+8
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No response: '+value)

    try:
        adb('push',str(report/'config-test.xml'),REMOTE+'config.xml')
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity');time.sleep(5)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
        command('padvirtual attach');time.sleep(.2)
        before=logs();command('padvirtual button dpdown 1');time.sleep(.85)
        command('padvirtual button dpdown 0');time.sleep(.2)
        delta=logs()[len(before):]
        selections=re.findall(r'Pazur menu selection: page=(\d+) item=(\S+) index=(\d+)',delta)
        assert len(selections)>=3,selections
        assert len({p for p,_,_ in selections})==1,selections
        assert 'confirm=1' not in delta and 'Terminating...' not in delta,delta
        command('padvirtual detach')
        (report/'results.json').write_text(json.dumps({'selection_changes':len(selections),'same_page':True,
            'no_confirmation':True,'selections':selections,'passed':True},indent=2),encoding='utf-8')
        print('Held D-pad selection changes:',len(selections))
    finally:
        if pid:(report/'native.log').write_text(logs(),encoding='utf-8')
        adb('shell','am','force-stop','pl.pazur.port')
        adb('push',str(report/'config.xml'),REMOTE+'config.xml')
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):adb('shell','rm','-f',REMOTE+name)


if __name__=='__main__':main()
