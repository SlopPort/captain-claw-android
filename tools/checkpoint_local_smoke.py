"""Real checkpoint collision, process restart and menu reload; app-local input.

OpenAI Codex. Isolated save and setup teleport are explicit fixtures. No global
Android keys or injected checkpoint/save events. Original files are restored.
"""
import argparse
import json
import re
import time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import adb,REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    apk_sha256=installed_apk_sha256()
    with CampaignSession(args.report,level=1) as session:
        session.command('campaignposition 6857 4930');time.sleep(2)
        adb('pull',REMOTE+'SAVES.XML',str(session.report/'checkpoint-save.xml'))
        saved=ET.parse(session.report/'checkpoint-save.xml')
        assert any(v.findtext('CheckpointNumber')=='1' for v in saved.findall('Level/Checkpoint')),'Checkpoint collision not saved'
        assert 'Pazur progress atomically saved' in session.logs(),'Atomic save path not observed'
        config=ET.parse(session.report/'config.test.xml');config.find('DebugOptions/SkipMenu').text='false'
        config.write(session.report/'reload-config.xml',encoding='utf-8',xml_declaration=True)
        adb('push',str(session.report/'reload-config.xml'),REMOTE+'config.xml')
        session.restart();time.sleep(.3)
        def press(button):
            session.command('menukey '+button);time.sleep(.3)
        start=len(session.logs())
        for button in ('enter','down','enter','enter','down','enter'):press(button)
        session.wait('Level loaded !',after=start)
        time.sleep(1);start=len(session.logs());session.command('combatstatus')
        positions=re.findall(r'probe status: claw=\d+ duck=\d+ x=([-\d.]+) y=([-\d.]+)',session.logs()[start:])
        assert positions,'No restored player position'
        x,y=map(float,positions[-1]);assert abs(x-6857)<250 and abs(y-4972)<250,(x,y)
        session.capture('checkpoint-restored')
        assert installed_apk_sha256()==apk_sha256,'Package changed during test'
        result=dict(passed=True,real_checkpoint_collision=True,process_restarted=True,
                    apk_sha256=apk_sha256,
                    reloaded_through_menu=True,position=[x,y],natural_playthrough=False,
                    input='app-local SDL keyboard events',controller_input=False,global_input=False,
                    fixtures=['isolated save','teleport to existing checkpoint'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
