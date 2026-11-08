"""Check pause/resume while attached to an isolated production ladder.

OpenAI Codex (LLM). Enemies removed, HP/ammo initialized by ladderstage;
no natural campaign, physical controller, hurt/death or process-death claim.
Fresh configuration/progress are restored by CampaignSession.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    apk=installed_apk_sha256()
    rows=[]
    with CampaignSession(args.report,level=1) as session:
        def sample():
            start=len(session.logs());session.command('ladderstatus')
            session.wait('Pazur ladder status:',after=start)
            match=re.findall(r'Pazur ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)',session.logs()[start:])[-1]
            x,y,bottom,climb,ladder,ground,vy,animation,paused=match
            return dict(x=float(x),y=float(y),bottom=int(bottom),climb=int(climb),ladder=int(ladder),ground=int(ground),vy=float(vy),animation=animation,animation_paused=int(paused))

        session.command('ladderstage')
        session.command('combatkey up 300');time.sleep(.6)
        session.command('combatkey release 0');time.sleep(.2)
        initial=sample()
        assert initial['climb'] and not initial['ground'] and abs(initial['vy'])<.1,initial
        for cycle in range(3):
            before=sample();start=len(session.logs())
            session.command('menukey escape')
            session.wait('Pazur pad context: mode=2',after=start)
            if cycle==0:session.capture('paused-on-ladder')
            time.sleep(.6)
            start=len(session.logs());session.command('menukey escape')
            session.wait('Pazur pad context: mode=1',after=start)
            after=sample()
            assert after['climb'] and not after['ground'] and abs(after['vy'])<.1,after
            assert abs(after['x']-before['x'])<1 and abs(after['y']-before['y'])<1,(before,after)
            rows.append(dict(cycle=cycle,before=before,after=after))
        session.command('combatkey up 150');time.sleep(.35)
        session.command('combatkey release 0')
        moved=sample()
        assert moved['y']<rows[-1]['after']['y']-10,'Climbing did not resume'
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
        result=dict(passed=True,apk_sha256=apk,cycles=rows,moved_after_resume=moved,
                    crash_evidence=crashes,natural_playthrough=False,physical_controller_tested=False,
                    input='app-local Escape keys; no controller attached by this helper')
    result['original_config_and_progress_restored']=True
    (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
