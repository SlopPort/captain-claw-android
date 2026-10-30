"""Attach through a real level-three rope trigger, observe motion, and jump off.

OpenAI Codex (LLM). Setup teleports/removes enemies and protects Claw; this is
not natural route evidence. No direct attach callback or boss/progress edit.
"""
import argparse,json,re,time,math
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);a=p.parse_args()
 source=(PORT/'upstream/OpenClaw/OpenClaw/Engine/Actor/Components/RopeComponent.cpp').read_text(encoding='utf-8')
 offsets={int(i):(float(x),float(y)) for i,x,y in re.findall(r'\{\s*(\d+), Point\((-?\d+), (-?\d+)\)',source)}
 assert len(offsets)==120
 pattern=r'Pazur rope status: id=\d+ x=6466\.0 y=6060\.0 frame=(\d+) phase=([\d.]+) attached=(\d) hero=([-\d.]+),([-\d.]+)'
 with CampaignSession(a.report,level=3) as s:
  s.command('combatstage -1 80 0');s.command('invincible 1');rows=[]
  def status():
   start=len(s.logs());s.command('ropestatus');m=re.findall(pattern,s.logs()[start:]);assert m,'Missing first rope';f,t,attached,x,y=m[-1]
   row=dict(frame=int(f),phase=float(t),attached=int(attached),x=float(x),y=float(y));return row
  for attempt in range(24):
   s.command('campaignposition 6293 6082');time.sleep(.12)
   row=status()
   if row['attached']:break
  else:raise AssertionError('Real rope trigger did not attach during timed placements')
  for _ in range(18):
   row=status();rows.append(row);assert row['attached'],'Rope dropped Claw without input'
   f=row['frame'];t=row['phase'];v=offsets[f];n=offsets[(f+1)%120]
   expected=(6468+v[0]+(n[0]-v[0])*t,5909+v[1]+(n[1]-v[1])*t)
   row['handle_error_px']=math.hypot(row['x']-expected[0],row['y']-expected[1])
   assert row['handle_error_px']<25,row
   time.sleep(.08)
  s.command('combatkey jump 100');time.sleep(.22);detached=status();assert not detached['attached'],detached
  result=dict(passed=True,apk_sha256=installed_apk_sha256(),natural_playthrough=False,attachment='real trigger after teleport setup',samples=rows,detach=detached,visual_smoothness_verified=False)
  (s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(dict(passed=True,samples=len(rows),max_handle_error=max(v['handle_error_px'] for v in rows))))
if __name__=='__main__':main()
