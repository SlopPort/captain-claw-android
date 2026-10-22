"""Real parrot contacts, retracting bridge and jumping sword phases.

Isolated level/teleports/player protection are fixtures. No boss or parrot HP
edits, spawned projectiles or synthetic phase/completion events are used.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession


def boss(session):
    start=len(session.logs());session.command('campaignmap')
    values=re.findall(r'name=Level10_Marrow x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',session.logs()[start:])
    if not values and re.search(r'Pazur enemy defeated: Level10_Marrow\s*$',session.logs(),re.M):
        return 0.,0.,0
    assert values,'Marrow missing';x,y,hp=values[-1]
    return float(x),float(y),int(hp)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    parser.add_argument('--observe',action='store_true');args=parser.parse_args()
    with CampaignSession(args.report,level=10) as session:
        session.command('invincible 1');session.command('teleport 32432 7769')
        session.wait('Pazur Marrow fight started')
        session.capture('arena-start')
        if args.observe:
            time.sleep(5);session.command('campaignmap');session.capture('parrot-flight');return
        for phase in range(3):
            bx,by,hp=boss(session);right=bx>40812
            session.command('combatkey '+('right' if right else 'left')+' 30');time.sleep(.1)
            session.command('teleport '+('40562' if right else '41063')+' 7200');time.sleep(.7)
            start=len(session.logs())
            for _ in range(70):
                session.command('combatkey sword 100');time.sleep(.3)
                if 'Pazur Marrow bridge opened' in session.logs()[start:]:break
            else:raise AssertionError('Three real parrot hits did not open bridge')
            time.sleep(1);session.capture('bridge-'+str(phase+1))
            start=len(session.logs())
            for attempt in range(48):
                bx,by,hp=boss(session)
                if hp<=0 or 'Pazur Marrow carry started' in session.logs()[start:]:break
                side=-1 if bx>40812 else 1
                session.command('combatkey '+('right' if side<0 else 'left')+' 30');time.sleep(.1)
                session.command(f'teleport {bx+side*75:.1f} 7300');time.sleep(.55)
                if attempt < 4:
                    session.command(f'laddertrace marrow-jump-{phase}-{attempt} 1800')
                # Schedule ordinary button events on the game thread. Separate
                # ADB round trips either missed a short jump or attacked above
                # the boss during a full-height jump (preserved trace reports).
                session.command('combatjumpattack 100 150 '+('right' if side<0 else 'left'));time.sleep(1.1)
                if attempt < 4:
                    session.command('combatstatus')
            else:raise AssertionError('Jumping sword phase did not advance')
            if phase<2:
                session.wait('Pazur Marrow parrot phase resumed',seconds=8,after=start)
                assert boss(session)[2]==100-phase*50,'Unexpected phase health'
            else:session.wait('Pazur enemy defeated: Level10_Marrow')
        time.sleep(2);session.command('campaignfinish');session.wait('Score screen initialized OK')
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if 'Level name: Claw - Level 11' in session.logs():break
        session.wait('Level name: Claw - Level 11')
        result=dict(passed=True,natural_playthrough=False,boss_health_edited=False,
                    phases=3,input='ordinary sword and jump',fixtures=['level start','teleports','player protection'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
