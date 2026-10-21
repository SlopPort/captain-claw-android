"""Measure actual mixed output for player sword/gun and a live enemy attack.

No audio recording or microphone access. Music is muted in the temporary
session; counts and peak amplitude only are collected from SDL's post-mix.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    args=parser.parse_args();rows=[]
    with CampaignSession(args.report) as session:
        session.command('audiooptions 1 0 100 100')
        session.command('audiotrace 1')
        session.command('combatstage -1 80 0');time.sleep(1)
        for label,key,expected in [('idle',None,None),('sword','sword','/claw/sounds/swordswish.wav'),
                                   ('pistol','pistol','/claw/sounds/gunshot.wav'),
                                   ('officer',None,'/level1/sounds/officer/ofcswstb8-22.wav'),
                                   ('chameleon13',None,'/level13/sounds/chameleon/tonguestrike.wav'),
                                   ('chameleon14',None,'/level14/sounds/chameleon/tonguestrike.wav')]:
            if label in ('officer','chameleon13','chameleon14'):
                names=re.findall(r'^\s*ActorPrototype_(\w+),',(PORT/'native/CombatPrototypes.h').read_text(),re.M)
                prototype={'officer':'Level1_Officer','chameleon13':'Level13_Chameleon','chameleon14':'Level14_Chameleon'}[label]
                session.command('combatstage '+str(names.index(prototype))+' 65 0')
                session.command('invincible 1');time.sleep(.5)
            session.command('audioquiet');time.sleep(.2)
            if label=='sword':
                # Standing melee randomly selects a kick/uppercut in OpenClaw.
                # Crouching selects duckswipe, so this specifically tests a sword.
                session.command('combatkey down 4000');time.sleep(.2)
            start=len(session.logs());session.command('audiomeasure '+label)
            if key:session.command('combatkey '+key+' 100')
            time.sleep(5 if label.startswith('chameleon') else 2 if label=='officer' else 1.2)
            session.command('audioreport')
            log=session.logs()[start:]
            match=re.search(r'audio mix: label='+label+r' buffers=(\d+) audible=(\d+) nonzero=(\d+) peak=(\d+)',log)
            assert match,'Missing mixer measurement'
            buffers,audible,nonzero,peak=map(int,match.groups())
            sound=expected is None or any('accepted=1' in line and expected in line.lower() for line in log.splitlines())
            passed=buffers>0 and (nonzero==0 if label=='idle' else nonzero>0 and peak>0 and sound)
            row=dict(label=label,buffers=buffers,audible_buffers=audible,nonzero_samples=nonzero,peak=peak,
                     expected_sound=expected,sound_request_seen=sound,passed=passed)
            rows.append(row);print(json.dumps(row),flush=True)
            if label=='sword':session.command('combatkey release 0')
        session.command('audiotrace 0')
        (session.report/'results.json').write_text(json.dumps(dict(rows=rows,passed=all(row['passed'] for row in rows)),indent=2),encoding='utf-8')
        assert all(row['passed'] for row in rows),'See actual mixer and resource logs'


if __name__=='__main__':main()
