"""Codex (LLM): isolated raw-Start and Catnip music transition regression.

Keeps existing bindings and restores config/progress. Virtual controller/raw
Android codes are app-local; not a physical Bluetooth transport test. Catnip is
applied by the existing console command, not by traversing to an actual pickup.
"""
import argparse,json,os,re,time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--report',required=True)
a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256();rows=[]
with CampaignSession(a.report,level=1) as s:
 s.command('padvirtual attach');time.sleep(.5)
 for cycle in range(3):
  start=len(s.logs())
  s.command('padvirtual raw 108 1');time.sleep(.25)
  s.command('padvirtual raw 108 0');time.sleep(.3)
  assert 'Pazur pad context: mode=2' in s.logs()[start:],'Raw Start did not pause'
  start=len(s.logs())
  s.command('padvirtual raw 108 1');s.command('padvirtual raw 108 0');time.sleep(.3)
  assert 'Pazur pad context: mode=1' in s.logs()[start:],'Raw Start did not resume'
  rows.append(dict(cycle=cycle,raw_start_pause_resume=True))
 s.command('padvirtual detach');time.sleep(1)
 start=len(s.logs());s.command('catnip');time.sleep(32)
 s.command('catnip');time.sleep(3)
 log=s.logs()[start:]
 switches=[int(n) for n in re.findall(r'Pazur MIDI switch: elapsed=(\d+) ms',log)]
 assert len(switches)>=3,'Need acquisition, expiry and acquisition switches'
 assert max(switches)<40,('Music transition too slow',switches)
 assert 'Pazur MIDI prepare:' not in log,'Unexpected music preparation during gameplay'
 assert 'Pazur audio PCM: peak=' in log,'No PCM observation after music switch'
 assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,'Native/Java crash recorded'
 assert s.pid in s.process_ids(),'Game exited during music observation'
 result=dict(passed=True,apk_sha256=apk,pause_cycles=rows,music_switch_ms=switches,
  native_crash=False,natural_playthrough=False,physical_controller_tested=False)
result['original_config_and_progress_restored']=True
(s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
