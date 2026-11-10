"""Observe jump/sword input started on the game thread after a real hit.

OpenAI Codex (LLM). Opt-in debug42 diagnostic; active Soldier on an isolated
32 px step, setup HP100/ammo99, no protection/healing during observation.
Protocol success is not balance/original-fidelity acceptance. Never a campaign
clear or physical touchscreen/controller latency measurement.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence
from vertical_combat_smoke import state
from gamepad_quit_smoke import PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    apk=installed_apk_sha256()
    prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text(encoding='utf-8'))
    index=prototypes.index('ActorPrototype_Level1_Soldier')
    rows=[]
    for hold in (250,700):
        for delay in (0,80):
            label=f'{args.report}/hold-{hold}-sword-{delay}'
            with CampaignSession(label,level=1) as session:
                session.command('combatkey right 100');time.sleep(.25)
                session.command(f'combatstairs {index} 80 32')
                initial=state(session)
                assert initial['enemy']=='Soldier' and initial['enemy_hp']>0,initial
                assert initial['enemy_box'][1]+initial['enemy_box'][3]<initial['player_box'][1]+initial['player_box'][3],initial
                session.command('laddertrace after-hit-order 4200')
                start=len(session.logs())
                session.command(f'combatjumpafterhit {hold} {delay} right')
                session.wait('Pazur jump after hit: armed ',after=start)
                session.wait('Pazur jump after hit: sent ',after=start,seconds=8)
                session.wait('Pazur jump trace: label=afterhit ',after=start,seconds=6)
                log=session.logs()[start:]
                sent=re.findall(r'Pazur jump after hit: sent hp=(\d+) tick=(\d+)',log)
                measurements=re.findall(r'Pazur jump trace: label=afterhit queue_ms=(\d+) takeoff_ms=(-?\d+) rise=([\d.]+) hold_ms=(\d+) jumps=(\d+)',log)
                assert len(sent)==len(measurements)==1,'Expected one armed input and one measurement'
                hp,tick=map(int,sent[0]);q,t,h,d,j=measurements[0]
                assert tick>0 and hold<=int(d)<=hold+500, 'Incomplete or invalid input-duration measurement'
                assert any(int(source)==initial['enemy_actor_id'] and int(after)==hp
                           for after,source in re.findall(r'Pazur combat: actor=Claw health=\d+->(\d+) source=(\d+)',log)), 'Trigger health does not match an actual Soldier hit'
                final=state(session)
                crashes=crash_evidence(session.logs())
                assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
                row=dict(protocol_passed=True,apk_sha256=apk,requested_hold_ms=hold,requested_sword_delay_ms=delay,
                         trigger_hp=hp,input_tick=tick,queue_ms=int(q),first_upward_motion_ms=int(t),rise=float(h),
                         recorded_hold_ms=int(d),displacement_cycles=int(j),initial=initial,final=final,
                         upward_motion_observed=float(h)>2,crash_evidence=crashes,natural_playthrough=False,
                         physical_input_latency_tested=False,original_parity_verified=False)
            row['fresh_config_and_progress_restored']=True
            (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
            rows.append(row)
            print(json.dumps({k:row[k] for k in ('requested_hold_ms','requested_sword_delay_ms','first_upward_motion_ms','rise','recorded_hold_ms')}),flush=True)
    (PORT/'reports'/args.report/'results.json').write_text(json.dumps(dict(protocol_passed=True,cases=rows),indent=2),encoding='utf-8')


if __name__=='__main__':main()
