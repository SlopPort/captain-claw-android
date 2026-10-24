"""Walk both directions after activating the real level-one checkpoint.

OpenAI Codex (LLM). Teleport setup and removed enemies are explicit fixtures,
not natural traversal. Checkpoint collision and save handling are production
paths; the user's original config and progress are restored on exit.
"""
import argparse,json,os,time,xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from vertical_combat_smoke import state
from android_package import installed_apk_sha256
from gamepad_quit_smoke import adb,REMOTE
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256()
with CampaignSession(a.report,level=1) as s:
 s.command('combatstage -1 80 0');s.command('campaignposition 6873 4970');time.sleep(1)
 before=state(s);s.capture('checkpoint-before')
 progress=ET.fromstring(adb('exec-out','cat',REMOTE+'SAVES.XML'))
 saved=any(c.findtext('CheckpointNumber')=='1' for level in progress.findall('Level') if level.findtext('LevelNumber')=='1' for c in level.findall('Checkpoint'))
 assert saved,'Real checkpoint collision did not write checkpoint 1'
 s.command('combatkey right 80');time.sleep(.4);right=state(s)
 s.command('combatkey left 160');time.sleep(.6);left=state(s);s.command('combatkey right 160');time.sleep(.5);returned=state(s);s.capture('checkpoint-after')
 assert right['position'][0]-before['position'][0]>15,('Blocked walking right',before,right)
 assert right['position'][0]-left['position'][0]>30,('Blocked walking back left',right,left)
 assert returned['position'][0]-left['position'][0]>30,('Blocked returning across checkpoint',left,returned)
 assert abs(right['position'][1]-before['position'][1])<4 and abs(left['position'][1]-before['position'][1])<4,'Unexpected floor height/fall; inspect setup'
 result=dict(passed=True,apk_sha256=apk,checkpoint_saved=True,before=before,right=right,left=left,returned=returned,natural_playthrough=False)
result['original_config_and_progress_restored']=True
(s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
