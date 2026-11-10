"""Real checkpoint collision, process restart and menu reload; app-local input.

OpenAI Codex. Isolated save and setup teleport are explicit fixtures. No global
Android keys or injected checkpoint/save events. Original files are restored.
"""
import argparse
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence
from vertical_combat_smoke import state
from gamepad_quit_smoke import adb,REMOTE
from gamepad_quit_smoke import PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--walk-after-reload',action='store_true',help='Observe short right/left/right movement after reload/optional respawn; no jump')
    parser.add_argument('--ordinary-death',action='store_true',help='After reload, let an active arena Soldier kill Claw, then check checkpoint respawn; setup removes other enemies and initializes HP/ammo')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    if args.ordinary_death and not args.walk_after_reload:parser.error('Ordinary death also requires --walk-after-reload')
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
        respawn=None
        if args.ordinary_death:
            lives=[int(c.findtext('Lives','0')) for c in saved.findall('Level/Checkpoint') if c.findtext('CheckpointNumber')=='1']
            assert lives and min(lives)>0,'Ordinary respawn requires remaining lives'
            prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text(encoding='utf-8'))
            start=len(session.logs())
            session.command(f'combatstage {prototypes.index("ActorPrototype_Level1_Soldier")} 80 0')
            arena=state(session)
            assert arena['enemy']=='Soldier' and arena['enemy_actor_id']>0,arena
            deadline=time.monotonic()+45
            while time.monotonic()<deadline:
                if re.search(r'Pazur combat: actor=Claw health=\d+->0\b',session.logs()[start:]):break
                time.sleep(.2)
            else:raise AssertionError('No ordinary enemy-caused death observed; retain fixture logs')
            death=re.search(r'Pazur combat: actor=Claw health=\d+->0 source=(\d+)',session.logs()[start:])
            assert death and int(death[1])==arena['enemy_actor_id'],'Fatal hit not attributed to the fixture Soldier'
            # Fatal health is followed by the death animation, then the
            # separate fade process. A fixed five-second sleep sampled that
            # legitimate paused interval rather than a failed respawn.
            session.wait('Pazur pad context: mode=2',after=start,seconds=15)
            fade_start=session.logs().index('Pazur pad context: mode=2',start)
            session.wait('Pazur pad context: mode=1',after=fade_start,seconds=20)
            respawn=state(session)
            assert respawn['player_hp']>0 and abs(respawn['position'][0]-x)<100 and abs(respawn['position'][1]-y)<100,respawn
            session.capture('checkpoint-respawned')
        walking=None
        if args.walk_after_reload:
            walking={'before':state(session)}
            for label,key,duration in [('right','right',80),('left','left',160),('returned','right',160)]:
                session.command(f'combatkey {key} {duration}');time.sleep(.4)
                walking[label]=state(session)
            session.command('combatkey release 0')
            # Retain the measured states even if an assertion below fails.
            (session.report/'reload-walk.json').write_text(json.dumps(walking,indent=2),encoding='utf-8')
            assert walking['right']['position'][0]-walking['before']['position'][0]>10,'Blocked right after checkpoint reload'
            assert walking['right']['position'][0]-walking['left']['position'][0]>20,'Blocked reversing left after checkpoint reload'
            assert walking['returned']['position'][0]-walking['left']['position'][0]>20,'Blocked returning right after checkpoint reload'
            assert all(row['player_hp']>0 for row in walking.values()),'Death invalidates movement observation'
            session.capture('checkpoint-walked')
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
        assert installed_apk_sha256()==apk_sha256,'Package changed during test'
        result=dict(passed=True,real_checkpoint_collision=True,process_restarted=True,
                    apk_sha256=apk_sha256,
                    reloaded_through_menu=True,position=[x,y],natural_playthrough=False,
                    walk_after_reload=walking,crash_evidence=crashes,
                    ordinary_death_requested=args.ordinary_death,checkpoint_respawn=respawn,
                    input='app-local SDL keyboard events',controller_input=False,global_input=False,
                    fixtures=['isolated save','teleport to existing checkpoint']+
                             (['arena setup removes other enemies, initializes hero HP100/ammo99 and spawns active Soldier; no healing during observed damage'] if args.ordinary_death else []))
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
