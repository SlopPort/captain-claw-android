"""Bounded, resumable ordinary-enemy fixture coverage. OpenAI Codex (LLM).

Each prototype gets both sides and both vertical relations through the existing
fresh-process test. Completion is evidence collection, not a fairness verdict.
No controller input or protection. Setup initializes HP=100/ammo=99; health is
not edited during observed actions. Passive AI is opt-in and must
remain labeled. Original config/progress hashes must match after every child.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT,REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--count',type=int,default=45)
    parser.add_argument('--height',type=int,choices=(16,32,48,64),default=48)
    parser.add_argument('--passive',action='store_true')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Set ANDROID_SERIAL explicitly')
    prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text())
    if args.start<0 or args.count<1 or args.start+args.count>len(prototypes):raise ValueError('Invalid prototype range')
    folder=(PORT/'reports'/args.report).resolve()
    if not folder.is_relative_to((PORT/'reports').resolve()):raise ValueError('Report must stay under reports')
    folder.mkdir(parents=True,exist_ok=False)
    def snapshot():
        return {name:hashlib.sha256(subprocess.check_output(['adb','exec-out','cat',REMOTE+name])).hexdigest()
                for name in ('config.xml','SAVES.XML')}
    before=snapshot();apk=installed_apk_sha256();rows=[];started=time.monotonic()
    summary=dict(apk_sha256=apk,expected_prototypes=prototypes[args.start:args.start+args.count],
                 height=args.height,offensive_ai_disabled=args.passive,all_requested_fixtures_completed=False,
                 natural_playthrough=False,controller_input=False,global_input=False,
                 fixture_initializes_hero_hp_to_100=True,fixture_sets_pistol_ammo_to_99=True,
                 health_edited_during_action=False,
                 original_file_hashes=before,rows=rows)
    try:
        for index in range(args.start,args.start+args.count):
            report=args.report+'/case-'+str(index)
            command=[sys.executable,str(PORT/'tools/vertical_combat_smoke.py'),'--report',report,
                     '--prototype',prototypes[index],'--height',str(args.height),'--actions','standing']
            if args.passive:command.append('--passive')
            with (folder/('case-'+str(index)+'-run.txt')).open('wb') as output:
                result=subprocess.run(command,stdout=output,stderr=subprocess.STDOUT,check=False)
            restored=snapshot()==before
            row=dict(index=index,prototype=prototypes[index],exit_code=result.returncode,files_restored=restored)
            if result.returncode==0:
                outcomes=json.loads((PORT/'reports'/(report+'-summary.json')).read_text())
                assert len(outcomes)==4 and all(v['apk_sha256']==apk for v in outcomes),'Wrong child coverage/build'
                row.update(cases=4,damage_observed=sum(v['enemy_damage_observed'] for v in outcomes),
                           hero_damage=sum(v['player_damage'] for v in outcomes),
                           all_cases_created_attack_area=None if any(v.get('deferred_request_trace_observed') for v in outcomes) else all(v['area_created'] for v in outcomes),
                           deferred_area_request_trace=any(v.get('deferred_request_trace_observed') for v in outcomes))
            rows.append(row)
            (folder/'results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
            print(json.dumps(row),flush=True)
            assert restored,'Original files were not restored; stop without overwriting evidence'
            assert installed_apk_sha256()==apk,'Installed APK changed; stop comparison'
            assert result.returncode==0,'Fixture failed; inspect the retained child report before continuing'
        summary['all_requested_fixtures_completed']=True
    finally:
        summary['elapsed_seconds']=time.monotonic()-started
        (folder/'results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')


if __name__=='__main__':main()
