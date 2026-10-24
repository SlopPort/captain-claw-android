"""Hold one jump against a segmented tall wall; reject wall-ground/height resets.

OpenAI Codex (LLM). Fresh passive physics fixture for each powerup condition.
No natural campaign traversal. The wall is higher than both configured jumps.
"""
import argparse,json,os,re,time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256();rows=[]
for catnip in (False,True):
 with CampaignSession(a.report+'-'+str(int(catnip)),level=1) as s:
  s.command('wallstage');assert 'Pazur wall fixture:' in s.logs(),'Missing wall fixture support'
  time.sleep(.3)
  if catnip:s.command('catnip')
  config=ET.parse(s.report/'config.original.xml')
  field='PowerupMaxJumpHeight' if catnip else 'MaxJumpHeight'
  cap=float(config.find('.//'+field).text)
  s.command('combatjumpmeasure wall');start=len(s.logs());s.command('walltrial');time.sleep(2.6)
  log=s.logs()[start:]
  match=re.search(r'Pazur jump trace: label=wall .*?rise=([\d.]+).*?jumps=(\d+)',log)
  assert match,('Missing completed jump trace',log[-1000:])
  rise=float(match[1]);jumps=int(match[2])
  supports=[float(y) for y in re.findall(r'Pazur foot support: counted=1 x=[\d.-]+ y=([\d.-]+)',log)]
  assert cap-15<=rise<=cap+2,('Wall changed allowed jump rise',catnip,cap,rise)
  assert jumps==1,('Repeated takeoff from one held input',jumps)
  assert all(y>=1040 for y in supports),('Wall counted as elevated support',supports)
  assert s.pid in s.process_ids(),'Game exited'
  rows.append(dict(catnip=catnip,configured_cap=cap,measured_rise=rise,jumps=jumps,accepted_support_y=supports))
result=dict(passed=True,apk_sha256=apk,cases=rows,original_config_and_progress_restored=True,natural_playthrough=False)
(s.report.parent/(a.report+'-results.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
