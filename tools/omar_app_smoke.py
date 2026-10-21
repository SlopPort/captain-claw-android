"""Controlled Omar contact/finale regression, using app-local input only.

Teleports, elemental powerups, infinite ammo and player protection are explicit
fixtures. Boss HP is never edited. This does NOT prove a natural playthrough.
"""
import copy
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    report=PORT/'reports/omar-app-0.4.8';report.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:raise RuntimeError('Existing mailbox')
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    config=ET.parse(report/'config.xml');config.find('DebugOptions/SkipMenu').text='true';config.find('DebugOptions/SkipMenuToLevel').text='14'
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true';config.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
    saves=ET.parse(report/'SAVES.XML')
    if not any(level.findtext('LevelNumber')=='14' for level in saves.findall('Level')):
        level=copy.deepcopy(saves.find('Level'));level.find('LevelNumber').text='14';saves.getroot().append(level)
    saves.write(report/'saves-test.xml',encoding='utf-8',xml_declaration=True)
    pid='';ticket=0;passed=False
    def logs():return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
    def wait(marker,seconds=40):
        deadline=time.monotonic()+seconds
        while marker not in logs() and time.monotonic()<deadline:time.sleep(.3)
        assert marker in logs(),'Missing '+marker
    def command(value):
        nonlocal ticket
        ticket+=1;tag='omar-'+str(ticket)
        (report/'command.tmp').write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(report/'command.tmp'),REMOTE+'combat-command.tmp');adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No response: '+value)
    try:
        adb('push',str(report/'test.xml'),REMOTE+'config.xml');adb('push',str(report/'saves-test.xml'),REMOTE+'SAVES.XML')
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity');time.sleep(2)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0];wait('Level loaded !')
        command('invincible 1');command('teleport 41820 1940');wait('Pazur Omar fight started')
        command('teleport 42300 2350');command('infiniteammo 1');command('combatkey left 80')
        for power,health in [('frostsword',175),('firesword',150),('frostsword',125),('firesword',100)]:
            command(power);deadline=time.monotonic()+28;marker='->'+str(health)+' bullets=0'
            while marker not in logs() and time.monotonic()<deadline:
                command('combatkey sword 100');time.sleep(.2)
            assert marker in logs(),marker;print('Actual elemental contact: HP',health,flush=True);time.sleep(1)
        # Let the last temporary elemental sword expire before ordinary duck sword.
        time.sleep(31)
        for round in range(4):
            command('teleport '+str(42320 if round%2==0 else 42090)+' 1900')
            command('combatkey '+('right' if round%2==0 else 'left')+' 70');time.sleep(.3)
            base=len(logs());target=75-round*25;marker='->'+str(target)+' bullets=0';deadline=time.monotonic()+30
            while marker not in logs()[base:] and time.monotonic()<deadline:
                current=logs()[base:]
                if 'bullets=3' not in current or current.rfind('opening closed')>current.rfind('bullets=3'):
                    command('combatkey pistol 100');time.sleep(.3)
                else:
                    command('combatkey down 1500');time.sleep(.2);command('combatkey sword 100');time.sleep(.3)
            assert marker in logs()[base:],marker;print('Actual duck contact: HP',target,flush=True)
        wait('Pazur finale complete',30);wait('Score screen initialized OK')
        command('padvirtual attach');time.sleep(.3)
        for _ in range(8):
            command('padvirtual button a 1');time.sleep(.1);command('padvirtual button a 0');time.sleep(.5)
            if 'Changing to: 3' in logs().split('Score screen initialized OK')[-1]:break
        assert 'Changing to: 3' in logs().split('Score screen initialized OK')[-1]
        assert 'Fatal signal' not in logs() and 'FATAL EXCEPTION' not in logs()
        passed=True;print('Controlled contact fight, finale, score and return to menu: PASS')
    finally:
        if pid:(report/'native.log').write_text(logs(),encoding='utf-8')
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):adb('shell','rm','-f',REMOTE+name)
        (report/'results.json').write_text(json.dumps({'passed':passed,'fixture':'teleport/powerups/infinite-ammo/player-protection','boss_health_edited':False,'natural_playthrough':False},indent=2))


if __name__=='__main__':main()
