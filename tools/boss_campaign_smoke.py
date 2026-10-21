"""Controlled melee boss encounter and real gem/score/save transition tests.

Setup uses isolated level starts, teleports and player invincibility. Attacks
are normal app-local sword input. Boss HP and damage callbacks are not edited.
This is not natural campaign traversal or proof of original-game parity.
"""
import argparse
import json
import re
import time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb, REMOTE

STAGERS={2:(23642,3994),4:(18429,1730),6:(34645,4476),10:(40497,7249),13:(37176,2061)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',type=int,choices=STAGERS,required=True)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    with CampaignSession(args.report,level=args.level) as session:
        session.command('invincible 1')
        x,y=STAGERS[args.level];session.command(f'teleport {x} {y-40}')
        time.sleep(23)
        effects={4:'/LEVEL4/SOUNDS/KATHERINE/WHIP1.WAV',6:'/LEVEL6/SOUNDS/WOLVINGTON/UPPERCUT.WAV',10:'/LEVEL10/SOUNDS/MARROW/STAB2.WAV'}
        if args.level in effects:
            session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
        boss_name=None;attempts=0
        for attempts in range(120):
            start=len(session.logs());session.command('campaignmap')
            bosses=re.findall(r'kind=boss .*name=(\S+) x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',session.logs()[start:])
            if boss_name and 'Pazur enemy defeated: '+boss_name in session.logs():break
            assert bosses,'No live boss found'
            name,x,y,hp=bosses[-1];boss_name=name
            if int(hp)<=0:break
            session.command(f'teleport {float(x)-75:.1f} {float(y)-5:.1f}')
            session.command('combatkey right 30');time.sleep(.1)
            if attempts==0 and args.level in effects:
                session.command('audioquiet');session.command('audiomeasure boss-effect');time.sleep(3)
                session.command('audioreport')
            session.command('combatkey sword 100');time.sleep(.65)
        else:raise AssertionError('Boss did not fall to controlled ordinary sword attacks')
        session.wait('Pazur enemy defeated: '+boss_name)
        if args.level in effects:
            assert any('accepted=1' in row and effects[args.level] in row for row in session.logs().splitlines()),'Missing boss attack effect'
            session.command('audiotrace 0')
        time.sleep(2);session.capture('boss-defeated')
        start=len(session.logs());session.command('campaignfinish')
        session.wait('Score screen initialized OK',after=start)
        score=len(session.logs())
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if 'Level name:' in session.logs()[score:]:break
        session.wait('Level name:',after=score)
        session.wait('Level loaded !',after=score)
        start=len(session.logs());session.command('campaignmap')
        assert f'campaign state: level={args.level+1} ' in session.logs()[start:]
        adb('pull',REMOTE+'SAVES.XML',str(session.report/'progress.xml'))
        assert any(v.findtext('LevelNumber')==str(args.level+1) for v in ET.parse(session.report/'progress.xml').findall('Level'))
        result=dict(passed=True,level=args.level,boss=boss_name,attack_attempts=attempts+1,
                    next_level=args.level+1,natural_playthrough=False,boss_health_edited=False,
                    fixtures=['level start','teleports','player invincibility'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
