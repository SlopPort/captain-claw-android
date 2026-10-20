"""Verify real background saving and restart loading without changing other options."""
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    report=PORT/'reports/audio-options-0.4.7';report.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    config=ET.parse(report/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text='1'
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true'
    config.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
    ticket=0

    def launch():
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity')
        pid=''
        deadline=time.monotonic()+50
        while time.monotonic()<deadline:
            pid=adb('shell','pidof','pl.pazur.port',check=False).strip().split()
            if pid and 'Level loaded !' in adb('logcat','-d','--pid='+pid[0],'-s','SDL/APP'):return pid[0]
            time.sleep(.5)
        raise RuntimeError('Level did not load')

    def command(value):
        nonlocal ticket
        ticket+=1;tag='audio-'+str(ticket)
        (report/'command.tmp').write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(report/'command.tmp'),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No response: '+value)

    def fields(root):
        def walk(node,path):
            result={path:(node.text if node.text and node.text.strip() else None),path+'@':sorted(node.attrib.items())}
            for child in node:result.update(walk(child,path+'/'+child.tag))
            return result
        return {k:v for p in root for c in p for k,v in walk(c,p.tag+'/'+c.tag).items()}

    try:
        adb('push',str(report/'test.xml'),REMOTE+'config.xml')
        launch();command('audiooptions 0 0 37 12')
        # Opening settings backgrounds SDL without injecting any system keys.
        adb('shell','am','start','-a','android.settings.SETTINGS');time.sleep(1)
        adb('pull',REMOTE+'config.xml',str(report/'saved.xml'))
        saved=ET.parse(report/'saved.xml')
        expected={'Audio/SoundOn':'false','Audio/MusicOn':'false','Audio/SoundVolume':'37','Audio/MusicVolume':'12'}
        before,after=fields(config.getroot()),fields(saved.getroot())
        assert all(after[k]==v for k,v in expected.items()),after
        assert {k:v for k,v in before.items() if k not in expected}=={k:v for k,v in after.items() if k not in expected}
        adb('shell','am','force-stop','pl.pazur.port')
        pid=launch();command('audiooptions')
        log=adb('logcat','-d','--pid='+pid,'-s','SDL/APP')
        (report/'native.log').write_text(log,encoding='utf-8')
        assert 'sound=0 music=0 soundVolume=37 musicVolume=12' in log,log[-2000:]
        (report/'results.json').write_text(json.dumps({'background_saved':True,'restart_loaded':True,'other_fields_preserved':True,'passed':True},indent=2))
        print('Audio background save and restart: PASS')
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):adb('shell','rm','-f',REMOTE+name)


if __name__=='__main__':main()
