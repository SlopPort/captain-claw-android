"""Walk across 1/2 px solid-floor joins without jumping; report snagging.

OpenAI Codex (LLM). Each case has fresh real physics and an isolated raised
floor segment; no enemy, teleported campaign progression or persistent edits.
"""
import argparse,json,os,time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from vertical_combat_smoke import state
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--report',required=True)
p.add_argument('--expect-fixed',action='store_true')
a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256();rows=[]
for side in (-1,1):
 for rise in (1,2):
  with CampaignSession(a.report+'-'+str(side)+'-'+str(rise),level=1) as s:
   s.command(f'combatstairs -1 {side*80} {rise} passive');time.sleep(.3)
   before=state(s)
   s.command('combatkey '+('right' if side>0 else 'left')+' 1200');time.sleep(1.4)
   after=state(s);advanced=side*(after['position'][0]-before['position'][0])
   row=dict(side=side,rise=rise,before=before,after=after,advanced_px=advanced,crossed=advanced>100)
   rows.append(row)
   if a.expect_fixed:assert row['crossed'],('Snagged at floor join',row)
result=dict(apk_sha256=apk,cases=rows,all_crossed=all(r['crossed'] for r in rows),natural_playthrough=False,original_config_and_progress_restored=True)
(s.report.parent/(a.report+'-results.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
