"""Verify binding capture UI -> saved file -> Java/JNI -> native sword damage.

Preserves config, saves and any custom controller bindings. Controlled arena,
not a natural gameplay or physical controller test.
"""
from pathlib import Path
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT

REPORT=PORT/'reports/controller-bindings-0.4.5'


def main():
    REPORT.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing diagnostic mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    files=['config.xml','SAVES.XML','controller-bindings.txt']
    present={name:subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0 for name in files}
    for name in files:
        if present[name]: adb('pull',REMOTE+name,str(REPORT/name))
    config=ET.parse(REPORT/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text='1'
    debug=config.find('DebugOptions');flag=debug.find('PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(debug,'PreviewIncompleteLevel14')
    flag.text='true'
    config.write(REPORT/'config-test.xml',encoding='utf-8',xml_declaration=True)
    try:
        adb('push',str(REPORT/'config-test.xml'),REMOTE+'config.xml')
        adb('logcat','-c')
        output=adb('shell','am','instrument','-w','-r','pl.pazur.port.test/pl.pazur.port.ControllerBindingsTest',check=False)
        (REPORT/'instrumentation.log').write_text(output,encoding='utf-8')
        log=adb('logcat','-d','-s','SDL/APP','libc','AndroidRuntime')
        (REPORT/'native.log').write_text(log,encoding='utf-8')
        assert 'INSTRUMENTATION_CODE: 0' in output,output
        assert 'Pazur Android pad: key=102 down=1' in log,log
        assert re.search(r'Pazur pad state: .*attack=1 fire=0',log),log
        health=[int(n) for n in re.findall(r'Pazur probe status: .*target_hp=(-?\d+)',log)]
        assert len(health)>=2 and (0<=health[-1]<health[-2] or 'Pazur enemy defeated: Soldier' in log),health
        result={'capture_ui':True,'saved_attack_key':102,'jni_dispatch':True,'native_sword_input':True,
                'controlled_sword_damage':True,'target_health':health,'physical_test':False}
        (REPORT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result,indent=2))
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in files:
            if present[name]:adb('push',str(REPORT/name),REMOTE+name)
            else:adb('shell','rm','-f',REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp','controller-bindings.tmp'):
            adb('shell','rm','-f',REMOTE+name)


if __name__=='__main__':main()
