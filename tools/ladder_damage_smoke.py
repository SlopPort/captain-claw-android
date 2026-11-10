"""Observe real Soldier damage during isolated production-ladder attachment.

OpenAI Codex (LLM). Setup creates a ladder, removes other enemies and initializes
HP100/ammo99. Offensive AI stays active; no protection/healing or direct damage
calls. Not campaign, physical-input or original-policy evidence. Fresh files
are restored by CampaignSession, including failed/insufficient-evidence trials.
"""
import argparse
import json
import os
import re
import time
from datetime import datetime
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence
from vertical_combat_smoke import state
from gamepad_quit_smoke import PORT

STATUS=r'Pazur ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)'


def sample(session):
    start=len(session.logs());session.command('ladderstatus')
    session.wait('Pazur ladder status:',after=start)
    x,y,bottom,climb,ladder,ground,vy,animation,paused=re.findall(STATUS,session.logs()[start:])[-1]
    return dict(x=float(x),y=float(y),bottom=int(bottom),climb=int(climb),ladder=int(ladder),ground=int(ground),vy=float(vy),animation=animation,animation_paused=int(paused))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--case',choices=('recovery','death','both'),default='both')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    apk=installed_apk_sha256();rows=[]
    prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text())
    index=prototypes.index('ActorPrototype_Level1_Soldier')
    for case in ('recovery','death'):
        if args.case not in (case,'both'):continue
        with CampaignSession(f'{args.report}/{case}',level=1) as session:
            session.command('ladderstage')
            # The following arena reset leaves the existing static ladder in
            # place. Distance gives the player time to attach before contact.
            session.command(f'combatstage {index} 220 0')
            session.command('combatkey up 60');time.sleep(.12)
            session.command('combatkey release 0')
            initial=sample(session);enemy=state(session)
            row=dict(case=case,initial=initial,enemy=enemy)
            (session.report/'observations.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
            assert initial['climb'] and not initial['ground'] and enemy['player_hp']>0,'No valid live mid-ladder setup'
            session.command('laddertrace ladder-damage 10000');start=len(session.logs())
            session.wait('Pazur combat: actor=Claw health=',after=start,seconds=12)
            hits=re.findall(r'actor=Claw health=(\d+)->(-?\d+) source=(\d+)',session.logs()[start:])
            assert any(int(h[2])==enemy['enemy_actor_id'] and int(h[0])>int(h[1]) for h in hits),'No staged Soldier damage'
            if case=='recovery':
                session.command('combatkey up 500');time.sleep(.8)
                session.command('combatkey release 0');recovered=sample(session)
                row['recovered']=recovered
                (session.report/'observations.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
                assert recovered['y']<initial['y']-10 and recovered['climb'] and not recovered['ground'],'Could not resume climbing after actual damage'
                jump_start=len(session.logs())
                session.command('combatjumpattack 250 0 right 250');time.sleep(1.2)
                escaped=sample(session);row['escaped']=escaped
                row['jump_trace_observed']=bool(re.search(r'ladder trace: label=ladder-damage .*animation=jump .*jumping=1',session.logs()[jump_start:]))
                assert row['jump_trace_observed'],'No actual jump observed after recovery'
                assert not escaped['climb'] and escaped['x']>recovered['x']+10,'Ladder retained control after jump-away'
            else:
                deadline=time.monotonic()+40;refresh=time.monotonic()+7;fatal=None;reattached=False
                while time.monotonic()<deadline:
                    log=session.logs()[start:]
                    deaths=[m for m in re.finditer(r'^.*actor=Claw health=(\d+)->(-?\d+) source='+str(enemy['enemy_actor_id'])+r'.*$',log,re.M) if int(m[1])>0 and int(m[2])<=0]
                    fatal=deaths[0] if deaths else None
                    if fatal:break
                    hits=re.findall(r'actor=Claw health=(\d+)->(-?\d+) source='+str(enemy['enemy_actor_id']),log)
                    if not reattached and hits and int(hits[-1][1])==5:
                        # Earlier damage may drop the hero to the floor. After
                        # natural health loss, reattach before the next shot;
                        # never manufacture low HP or a fatal damage callback.
                        time.sleep(.4)
                        session.command('combatkey up 60')
                        row['reattached_after_natural_health_5']=True;reattached=True
                    if time.monotonic()>=refresh:
                        session.command('laddertrace ladder-damage 10000');refresh=time.monotonic()+7
                    time.sleep(.2)
                assert fatal,'No actual fatal Soldier hit'
                previous=[line for line in log[:fatal.start()].splitlines() if 'Pazur ladder trace: label=ladder-damage ' in line]
                assert previous,'No pre-fatal ladder observation'
                last=previous[-1]
                # An explicit leap year avoids Python's ambiguous yearless
                # date parsing; only this short log interval is compared.
                stamp=lambda line:datetime.strptime('2000-'+line[:18],'%Y-%m-%d %H:%M:%S.%f')
                age=(stamp(fatal[0])-stamp(last)).total_seconds()*1000
                row.update(pre_fatal_trace=last,trace_age_ms=age,fatal_health=[int(fatal[1]),int(fatal[2])])
                (session.report/'observations.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
                assert 0<=age<=200 and 'ground=0 ladder=1 climb=1' in last,'Fatal hit was not sufficiently observed during attachment'
                session.wait('Pazur pad context: mode=2',after=start,seconds=15)
                fade=session.logs().index('Pazur pad context: mode=2',start)
                session.wait('Pazur pad context: mode=1',after=fade,seconds=20)
                respawn=sample(session);row['respawn']=respawn
                assert not respawn['climb'] and abs(respawn['x'])<10000,'Stale ladder attachment after real respawn'
                session.command('combatkey right 100');time.sleep(.3)
                moved=sample(session);row['moved_after_respawn']=moved
                assert moved['x']>respawn['x']+10,'Respawn movement blocked'
            crashes=crash_evidence(session.logs())
            assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
            row['crash_evidence']=crashes
        row['fresh_config_and_progress_restored']=True;rows.append(row)
        (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)
    assert installed_apk_sha256()==apk,'APK changed during observation'
    (report/'results.json').write_text(json.dumps(dict(passed=True,apk_sha256=apk,cases=rows,
        natural_playthrough=False,physical_input_tested=False,original_parity_verified=False),indent=2),encoding='utf-8')


if __name__=='__main__':main()
