"""Measure real sword contacts/health changes with and without Catnip.

OpenAI Codex (LLM). Passive ordinary Soldier fixtures isolate outgoing damage.
The normal 10 HP target may die; negative HP in its damage log still records
actual requested damage. No game data or persistent progress is changed.
This is not an original-game runtime experiment or natural campaign test.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report',required=True)
parser.add_argument('--expect-legacy',action='store_true')
args=parser.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
index=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text()).index('ActorPrototype_Level1_Soldier')
apk=installed_apk_sha256();rows=[]
for powerup,duck in [(False,False),(False,True),(True,False),(True,True)]:
    with CampaignSession(args.report+'-'+str(int(powerup))+'-'+str(int(duck)),level=1) as session:
        # Fix facing before spawning the target; a reversed swipe is a valid miss.
        session.command('combatkey right 100');time.sleep(.2)
        session.command(f'combatdummy {index} 65 0');time.sleep(.5)
        if powerup:session.command('catnip')
        if duck:
            session.command('combatkey down 2000');time.sleep(.2)
        expected=100 if powerup and args.expect_legacy else (5 if duck else 10)*(2 if powerup else 1)
        start=len(session.logs());session.command('combatkey sword 100');time.sleep(1)
        log=session.logs()[start:]
        contacts=re.findall(r'Pazur area contact: source=\d+ target=Soldier damage=(\d+)',log)
        health=re.findall(r'Pazur combat: actor=Soldier health=(-?\d+)->(-?\d+)',log)
        assert contacts and set(map(int,contacts))=={expected},('Wrong sword contact damage',expected,contacts)
        assert health and int(health[0][0])-int(health[0][1])==expected,('Wrong HP delta',expected,health)
        session.command('combatkey release 0');time.sleep(.25)
        rows.append(dict(catnip=powerup,crouched=duck,damage=expected,health_before=int(health[0][0]),health_after=int(health[0][1])))
result=dict(passed=True,apk_sha256=apk,legacy_100_expected=args.expect_legacy,cases=rows,natural_playthrough=False)
result['original_config_and_progress_restored']=True
(session.report.parent/(args.report+'-results.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
