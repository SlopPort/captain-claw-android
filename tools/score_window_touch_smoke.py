"""Verify Android window touch -> SDL -> real score screen -> next level.

The only gameplay fixture is teleporting to the existing level-one end pickup.
No input is sent to another app. Original config/saves are always restored.
"""
import argparse
import json
import subprocess
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT
from android_package import installed_apk_sha256


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    apk_sha256=installed_apk_sha256()
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    owned=('combat-command.txt','combat-response.txt','combat-command.tmp','score-window-before.png','score-window-after.png')
    for name in owned:
        if subprocess.run(['adb','shell','test','-e',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing test file: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    try:
        config=ET.parse(report/'config.xml')
        for path,value in [('DebugOptions/SkipMenu','true'),('DebugOptions/SkipMenuToLevel','1')]:config.find(path).text=value
        debug=config.find('DebugOptions');flag=debug.find('PreviewIncompleteLevel14')
        if flag is None:flag=ET.SubElement(debug,'PreviewIncompleteLevel14')
        flag.text='true';config.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
        adb('push',str(report/'test.xml'),REMOTE+'config.xml')
        adb('logcat','-c')
        with (report/'native.log').open('wb') as log:
            reader=subprocess.Popen(['adb','logcat','-s','SDL/APP','libc','AndroidRuntime'],stdout=log,stderr=subprocess.DEVNULL)
            try:
                output=adb('shell','am','instrument','-w','-r','-e','scenario','score','pl.pazur.port.test/pl.pazur.port.JumpTouchTest')
            finally:
                reader.terminate();reader.wait(timeout=5)
        (report/'instrumentation.log').write_text(output,encoding='utf-8')
        for name in owned[-2:]:adb('pull',REMOTE+name,str(report/name))
        log=(report/'native.log').read_text(encoding='utf-8',errors='replace')
        assert 'INSTRUMENTATION_CODE: 0' in output,output
        assert 'Score screen initialized OK' in log and 'Level name: Claw - Level 2' in log
        assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
        (report/'results.json').write_text(json.dumps(dict(passed=True,apk_sha256=apk_sha256,input='Android window MotionEvent',natural_playthrough=False)),encoding='utf-8')
        print('Android window score confirmation and level 2: PASS',flush=True)
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in owned:adb('shell','rm','-f',REMOTE+name)
        print('Original configuration and saves restored',flush=True)


if __name__=='__main__':main()
