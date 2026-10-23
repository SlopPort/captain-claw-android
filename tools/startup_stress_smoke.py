"""Repeat ordinary isolated level starts, not a route/campaign traversal.

OpenAI Codex (LLM). A startup timeout remains a failed observation even if a later
fresh process succeeds. Own log clients may reconnect with their history retained;
never restart the ADB server. Original config/save hashes checked after each loop.
"""
import argparse
import hashlib
import json
import os
import subprocess
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT,REMOTE

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report',required=True)
parser.add_argument('--level',type=int,choices=range(1,15),default=8)
parser.add_argument('--count',type=int,choices=range(1,21),default=10)
args=parser.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select one allocated device')
folder=PORT/'reports'/args.report;folder.mkdir(parents=True,exist_ok=False)
def snapshot():return {name:hashlib.sha256(subprocess.check_output(['adb','exec-out','cat',REMOTE+name])).hexdigest() for name in ('config.xml','SAVES.XML')}
before=snapshot();apk=installed_apk_sha256();rows=[]
result=dict(apk_sha256=apk,level=args.level,requested_starts=args.count,passed=False,diagnostics_enabled=False,natural_playthrough=False,rows=rows)
try:
 for index in range(args.count):
  with CampaignSession(args.report+'/start-'+str(index),level=args.level,diagnostics=False) as session:
   session.wait('Level name: Claw - Level '+str(args.level))
   session.wait('Pazur frame sample:',seconds=30)
   assert session.pid in session.process_ids(),'Game process ended'
   reconnects=session.report/'log-reconnections.jsonl'
   rows.append(dict(index=index,loaded=True,render_sample_observed=True,log_client_reconnections=len(reconnects.read_text().splitlines()) if reconnects.exists() else 0))
  assert snapshot()==before,'Original files changed'
  assert installed_apk_sha256()==apk,'Installed package changed'
  (folder/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(rows[-1]),flush=True)
 result['passed']=True
finally:
 result['original_files_restored']=snapshot()==before
 (folder/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
