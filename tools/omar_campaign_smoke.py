"""Controlled final encounter with continuous logs and isolated/restored saves.

Codex implementation. Teleports, elemental powerups, infinite ammo and protection
are explicit fixtures. Damage is caused by ordinary attacks, not health edits.
"""
import argparse
import json
import time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb,REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    with CampaignSession(args.report,level=14) as session:
        session.command('invincible 1');session.command('teleport 41820 1940')
        session.wait('Pazur Omar fight started')
        session.command('teleport 42300 2350');session.command('infiniteammo 1')
        session.command('combatkey left 80')
        for power,health in [('frostsword',175),('firesword',150),('frostsword',125),('firesword',100)]:
            session.command(power);start=len(session.logs());deadline=time.monotonic()+28
            marker='->'+str(health)+' bullets=0'
            while marker not in session.logs()[start:] and time.monotonic()<deadline:
                session.command('combatkey sword 100');time.sleep(.2)
            session.wait(marker,seconds=1,after=start);time.sleep(1)
        time.sleep(31) # Let the last temporary sword powerup expire.
        for phase in range(4):
            session.command(f'teleport {42320 if phase%2==0 else 42090} 1900')
            session.command('combatkey '+('right' if phase%2==0 else 'left')+' 70')
            start=len(session.logs());deadline=time.monotonic()+35
            marker='->'+str(75-phase*25)+' bullets=0'
            while marker not in session.logs()[start:] and time.monotonic()<deadline:
                current=session.logs()[start:]
                if 'bullets=3' not in current or current.rfind('opening closed')>current.rfind('bullets=3'):
                    session.command('combatkey pistol 100');time.sleep(.3)
                else:
                    session.command('combatkey down 1500');time.sleep(.2)
                    session.command('combatkey sword 100');time.sleep(.3)
            session.wait(marker,seconds=1,after=start)
        session.wait('Pazur finale complete',seconds=30)
        session.wait('Score screen initialized OK');session.capture('final-score')
        start=len(session.logs())
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.4)
            if 'Changing to: 3' in session.logs()[start:]:break
        session.wait('Changing to: 3',after=start)
        adb('pull',REMOTE+'SAVES.XML',str(session.report/'progress.xml'))
        assert all(int(v.findtext('LevelNumber'))<=14 for v in ET.parse(session.report/'progress.xml').findall('Level'))
        result=dict(passed=True,finale=True,returned_to_menu=True,no_level15=True,
                    boss_health_edited=False,natural_playthrough=False,
                    fixtures=['isolated save','teleports','elemental powerups','infinite ammo','protection'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
