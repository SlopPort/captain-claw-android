"""Observe configured Soldier hurt/death and hero hurt audio after real contacts.

OpenAI Codex (LLM). Isolated arena with supplied Polish assets; setup HP/ammo,
passive Soldier for outgoing hits, active Soldier for incoming damage. No
direct damage calls, healing during actions, campaign or human-listening claim.
--expect-missing-enemy-hurt documents the old missing-request defect only.
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
    parser.add_argument('--expect-missing-enemy-hurt',action='store_true')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text())
    index=prototypes.index('ActorPrototype_Level1_Soldier')
    apk=installed_apk_sha256();rows=[]

    def measurement(session,label,start):
        session.command('audioreport')
        log=session.logs()[start:]
        mixes=re.findall(r'audio mix: label='+label+r' buffers=(\d+) audible=(\d+) nonzero=(\d+) peak=(\d+)',log)
        assert len(mixes)==1,'Missing or ambiguous mixer observation'
        buffers,audible,nonzero,peak=map(int,mixes[0])
        accepted=re.findall(r'audio sound: label='+label+r' accepted=1 path=(\S+)',log)
        assert buffers>0 and nonzero>0 and peak>0,'No actual mixed output'
        return dict(label=label,buffers=buffers,audible_buffers=audible,nonzero_samples=nonzero,peak=peak,
                    accepted_resources=[p.lower() for p in accepted]),log

    with CampaignSession(f'{args.report}/enemy',level=1) as session:
        session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
        session.command('combatkey right 100');time.sleep(.2)
        session.command(f'combatdummy {index} 65 0');time.sleep(.4)
        assert state(session)['enemy_hp']==10,'Expected stock Soldier health'
        for label,old_hp,new_hp,expected in (
                ('enemyhurt',10,5,'/level1/sounds/soldier/00320005.wav'),
                ('enemydeath',5,0,'/level1/sounds/soldier/00320006.wav')):
            session.command('combatkey down 4000');time.sleep(.2)
            session.command('audioquiet');session.command('audiomeasure '+label)
            start=len(session.logs());session.command('combatkey sword 100');time.sleep(1)
            row,log=measurement(session,label,start)
            row.update(health_before=old_hp,health_after=new_hp,expected_resource=expected)
            assert re.search(r'actor=Soldier health='+str(old_hp)+'->'+str(new_hp)+r' source=\d+',log),'Expected actual sword health change'
            requested=expected in row['accepted_resources']
            row['configured_request_observed']=requested
            rows.append(row)
            (session.report/'observations.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
            if label=='enemyhurt' and args.expect_missing_enemy_hurt:
                assert not requested,'Expected old missing hurt request is no longer reproduced'
                assert any(re.fullmatch(r'/game/sounds/hit[1-4]\.wav',p) for p in row['accepted_resources']),'Generic impact sound also absent'
            else:assert row['accepted_resources'].count(expected)==1,'Expected one accepted configured sound: '+expected
        session.command('combatkey release 0')
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes

    with CampaignSession(f'{args.report}/generic-impact',level=1) as session:
        session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
        session.command('combatkey right 100');time.sleep(.2)
        session.command(f'combatdummy {prototypes.index("ActorPrototype_Level1_Officer")} 65 0')
        initial=state(session);old=initial['enemy_hp']
        assert old>5,'Need a nonfatal generic-impact contact'
        session.command('combatkey down 4000');time.sleep(.2)
        session.command('audioquiet');session.command('audiomeasure genericimpact')
        start=len(session.logs());session.command('combatkey sword 100');time.sleep(1)
        row,log=measurement(session,'genericimpact',start)
        assert re.search(r'actor='+re.escape(initial['enemy'])+r' health='+str(old)+'->'+str(old-5)+r' source=\d+',log),'Expected actual nonfatal sword damage'
        assert len([p for p in row['accepted_resources'] if re.fullmatch(r'/game/sounds/hit[1-4]\.wav',p)])==1,'Generic impact absent or duplicated'
        assert '/level1/sounds/hit1.wav' not in log.lower(),'Invalid legacy impact placeholder was requested'
        row.update(health_before=old,health_after=old-5)
        rows.append(row)
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes

    with CampaignSession(f'{args.report}/hero',level=1) as session:
        session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
        session.command('audioquiet');session.command('audiomeasure herohurt')
        start=len(session.logs());session.command(f'combatstage {index} 65 0')
        target=state(session)
        session.wait('Pazur combat: actor=Claw health=100->',after=start,seconds=8)
        time.sleep(.4)
        row,log=measurement(session,'herohurt',start)
        hit=re.search(r'actor=Claw health=100->(\d+) source=(\d+)',log)
        assert hit and 0<int(hit[1])<100,'No nonfatal actual enemy hit'
        assert int(hit[2])==target['enemy_actor_id'],'Damage did not come from the staged Soldier'
        row.update(health_before=100,health_after=int(hit[1]),source_actor=int(hit[2]))
        assert any(re.fullmatch(r'/claw/sounds/11100(?:48|49|50|51)\.wav',p) for p in row['accepted_resources']),'Hero hurt voice absent'
        rows.append(row)
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
    result=dict(passed=True,expected_legacy_missing_hurt=args.expect_missing_enemy_hurt,apk_sha256=apk,
                cases=rows,fresh_config_and_progress_restored=True,natural_playthrough=False,
                human_listening_tested=False,hero_death_tested=False,
                mixed_output_scope='Nonzero mixed signal plus accepted expected resource; not isolated per-voice PCM')
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
