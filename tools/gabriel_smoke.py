"""Controlled Gabriel button/cannon test, using ordinary app-local sword input.

Written by OpenAI Codex. Isolated level, teleports and player protection are
fixtures; boss health and cannon/phase callbacks are never edited or invoked.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--attempts',type=int,default=100)
    parser.add_argument('--button-height',type=float,default=35)
    args=parser.parse_args()
    with CampaignSession(args.report,level=8) as session:
        session.command('invincible 1')
        session.command('teleport 31631 5167')
        time.sleep(24)
        session.command('audiotrace 1')
        start=len(session.logs());session.command('campaignmap')
        button=re.findall(r'name=Level8_GabrielButton x=([-\d.]+) y=([-\d.]+)',session.logs()[start:])
        assert button,'Real button position missing'
        button_x,button_y=map(float,button[-1])
        session.capture('arena')
        health=[]
        for attempt in range(args.attempts):
            start=len(session.logs());session.command('campaignmap')
            values=re.findall(r'name=Level8_Gabriel x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',session.logs()[start:])
            # GabrielPirate shares the prefix; its death is not boss completion.
            if re.search(r'Pazur enemy defeated: Level8_Gabriel\s*$',session.logs(),re.M):break
            assert values,'Gabriel missing'
            hp=int(values[-1][2]);health.append(hp)
            if hp<=0:break
            session.command('combatkey right 30')
            if attempt<2:session.command(f'laddertrace gabriel-button-{attempt} 1500')
            session.command(f'campaignposition {button_x-65:.1f} {button_y-args.button_height:.1f} sword')
            time.sleep(.6)
            if attempt in (0,3,10):session.capture('button-'+str(attempt))
        else:raise AssertionError('Cannon encounter did not finish')
        assert re.search(r'Pazur enemy defeated: Level8_Gabriel\s*$',session.logs(),re.M),'Boss defeat missing'
        assert '/level8/sounds/gabrielcannon/button1.wav' in session.logs().lower(),'Button sound missing'
        assert set(health).issubset({100,75,50,25,0}),health
        time.sleep(2);session.command('campaignfinish')
        session.wait('Score screen initialized OK')
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if 'Level name: Claw - Level 9' in session.logs():break
        session.wait('Level name: Claw - Level 9')
        result=dict(passed=True,health_observed=sorted(set(health),reverse=True),
                    natural_playthrough=False,boss_health_edited=False,
                    fixtures=['isolated save','teleports','player protection'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
