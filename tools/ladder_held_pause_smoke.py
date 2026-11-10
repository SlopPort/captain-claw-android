"""Release held climbing input during pause, then resume without stale motion.

OpenAI Codex (LLM). Isolated production ladder, enemies removed and setup HP.
App-local SDL input, not a physical controller/touch test or campaign traversal.
Fresh configuration/progress are restored even when an assertion fails.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence
from gamepad_quit_smoke import PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    apk=installed_apk_sha256()
    rows=[]
    # Separate actors/processes prevent one trial's ladder position from
    # approaching a cap and masking a stale held-direction failure.
    for direction in ('up','down'):
        with CampaignSession(f'{args.report}/{direction}',level=1) as session:
            def sample():
                start=len(session.logs());session.command('ladderstatus')
                session.wait('Pazur ladder status:',after=start)
                matches=re.findall(r'Pazur ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)',session.logs()[start:])
                x,y,bottom,climb,ladder,ground,vy,animation,paused=matches[-1]
                return dict(x=float(x),y=float(y),bottom=int(bottom),climb=int(climb),ladder=int(ladder),ground=int(ground),vy=float(vy),animation=animation,animation_paused=int(paused))

            session.command('padvirtual attach');time.sleep(.3)
            session.command('ladderstage')
            session.command('combatkey up 450');time.sleep(.7)
            session.command('combatkey release 0')
            initial=sample()
            assert initial['climb'] and not initial['ground'],initial
            button='dpup' if direction=='up' else 'dpdown'
            session.command(f'padvirtual button {button} 1')
            start=len(session.logs());session.command('menukey escape')
            session.wait('Pazur pad context: mode=2',after=start)
            # The mailbox rejects physics queries and combatkey while paused.
            # Use allowed virtual input release; measure only after resuming.
            session.command(f'padvirtual button {button} 0')
            time.sleep(.3)
            start=len(session.logs());session.command('menukey escape')
            session.wait('Pazur pad context: mode=1',after=start)
            resumed=sample()
            samples=[]
            for _ in range(5):
                time.sleep(.12);samples.append(sample())
            row=dict(direction=direction,initial=initial,resume_baseline=resumed,resumed=samples)
            rows.append(row)
            # Preserve the actual measurements even if a release assertion fails.
            (session.report/'observations.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
            delta=resumed['y']-initial['y']
            assert (delta < -5 if direction=='up' else delta > 5), 'Held input did not move in the requested direction'
            assert all(s['climb'] and not s['ground'] and abs(s['vy'])<.1 for s in samples),row
            assert all(abs(s['x']-resumed['x'])<1 and abs(s['y']-resumed['y'])<1 for s in samples),row
            session.command('combatkey up 100');time.sleep(.3)
            session.command('combatkey release 0');moved=sample()
            assert moved['y']<samples[-1]['y']-10,'Fresh press failed to resume climbing'
            row['fresh_press']=moved
            crashes=crash_evidence(session.logs())
            assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
            row['crash_evidence']=crashes
        row['fresh_config_and_progress_restored']=True
    result=dict(passed=True,apk_sha256=apk,rows=rows,natural_playthrough=False,physical_input_tested=False)
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
