"""Real Level 3 ladder fixture and read-only rope clock observations.

Written by OpenAI Codex (LLM). Teleported placement and removed enemies are not
natural campaign evidence. CampaignSession restores the original user files.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import PORT
from android_package import installed_apk_sha256

STATUS = r'Pazur ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    result = dict(natural_playthrough=False, apk_sha256=installed_apk_sha256(), cases=[])
    failures=[]
    # A fresh process for each cap avoids carrying an attachment/gravity state
    # across diagnostic teleports between unrelated ladders.
    for tile,x,surface in ((668,5984,6341),(667,7200,6016)):
        with CampaignSession(f'{args.report}/cap-{tile}', level=3) as session:
            session.command('combatstage -1 80 0')
            def sample(label):
                start=len(session.logs())
                session.command('ladderstatus')
                session.wait('Pazur ladder status:', after=start)
                groups=re.findall(STATUS,session.logs()[start:])[-1]
                row=dict(label=label,x=float(groups[0]),y=float(groups[1]),bottom=int(groups[2]),
                         climb=int(groups[3]),ladder=int(groups[4]),ground=int(groups[5]),vy=float(groups[6]),animation=groups[7])
                result['cases'].append(row)
                return row
            session.command(f'campaignposition {x} {surface-55}')
            time.sleep(.12)
            initial=sample(f'{tile}_calibration')
            # Start with the physical sole eight pixels below the actual cap.
            target=initial['y']+surface+8-initial['bottom']
            session.command(f'campaignposition {x} {target}')
            # A late 20 ms press exposes the release bug; 80 ms can lift Claw
            # ~40 pixels and hide the defective nine-pixel summit transition.
            session.command('combatkey up 20')
            time.sleep(.04)
            session.command('combatkey release 0')
            time.sleep(.65)
            mounted=sample(f'{tile}_neutral_mount')
            mount_pass=bool(mounted['ground'] and not mounted['climb'] and abs(mounted['bottom']-surface)<=4)
            if not mount_pass: failures.append(mounted)
            if mount_pass:
                session.command('combatkey down 200')
                time.sleep(.2)
                session.command('combatkey release 0')
                time.sleep(.15)
                down=sample(f'{tile}_descent')
                if not (down['climb'] and down['bottom']>surface+12): failures.append(down)
            # Pause at an ordinary segment below the cap: no phantom floor.
            session.command(f'campaignposition {x} {surface+70}')
            session.command('combatkey up 80')
            time.sleep(.1)
            session.command('combatkey release 0')
            time.sleep(.2)
            seam=sample(f'{tile}_middle_pause')
            if not (seam['climb'] and not seam['ground']): failures.append(seam)
            if tile==667:
                start=len(session.logs())
                for _ in range(35):
                    session.command('ropestatus')
                    time.sleep(.06)
                result['rope_samples']=re.findall(r'Pazur rope status:[^\r\n]*',session.logs()[start:])
                if not result['rope_samples']: failures.append('No rope clock evidence')
    # Clock sampling alone is not a visual smoothness or attached-motion pass.
    result['rope_attached_motion_verified']=False
    result['rope_visual_smoothness_verified']=False
    result['failures']=failures
    result['passed']=not failures
    (PORT/'reports'/args.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!="rope_samples"},ensure_ascii=True),flush=True)
    if failures: raise SystemExit(1)

if __name__=='__main__':
    main()
