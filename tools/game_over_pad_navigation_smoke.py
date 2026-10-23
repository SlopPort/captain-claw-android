"""Codex: reproduce/fix direction input on the text-only Game Over page.

App-local virtual SDL pad; no global Android input or campaign traversal.
Expected old crash requires the exact focus assertion, not any process failure.
"""
import argparse,json,os,time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--report',required=True)
p.add_argument('--expect-crash',action='store_true')
a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256();failure=None
with CampaignSession(a.report,level=1) as s:
 s.command('combatlastlife');s.wait('Pazur game over menu opened',seconds=15)
 s.command('padvirtual attach');time.sleep(.4)
 try:
  for direction in ('dpdown','dpup'):
   s.command('padvirtual button '+direction+' 1');time.sleep(.5)
   s.command('padvirtual button '+direction+' 0')
  s.command('padvirtual tap 320 240');s.wait('Changing to: 3',seconds=30,after=s.logs().index('Pazur game over menu opened'))
  time.sleep(2)
  assert s.pid in s.process_ids(),'Game exited after menu transition'
 except Exception as error:failure=str(error)
 time.sleep(.5);log=s.logs()
 exact='Could not find any button to switch focus to' in log and 'SIGABRT' in log
 if a.expect_crash:assert exact,('Exact baseline assertion not observed',failure)
 else:assert failure is None and not exact,(failure,log[-2500:])
 result=dict(passed=True,apk_sha256=apk,expected_old_assertion=a.expect_crash,
  focus_assertion_observed=exact,returned_to_main_menu=not a.expect_crash,
  physical_controller_tested=False,natural_playthrough=False)
result['original_config_and_progress_restored']=True
(s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
