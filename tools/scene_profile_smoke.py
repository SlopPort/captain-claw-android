"""Profile a specific scene; instrumented time is not an FPS benchmark.

OpenAI Codex. Isolated/restored config and saves; optional explicit real-map
placement and protection. No change to simulation cadence or game data.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',type=int,choices=range(1,15),required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--scene',type=int,nargs=2,metavar=('X','Y'),required=True)
    parser.add_argument('--protect-player',action='store_true')
    args=parser.parse_args()
    with CampaignSession(args.report,level=args.level) as session:
        if args.protect_player:session.command('invincible 1')
        session.command('teleport '+' '.join(map(str,args.scene)))
        time.sleep(3)
        start=len(session.logs());session.command('componentprofile')
        session.wait('Pazur component sample:',after=start,seconds=10);time.sleep(.3)
        log=session.logs()[start:]
        rows=[dict(component=name,total_ms_in_5_seconds=float(ms)) for name,ms in
              re.findall(r'Pazur component sample: (\S+) total=([\d.]+)',log)]
        assert rows and 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,log[-1000:]
        result=dict(level=args.level,scene=args.scene,teleported=True,
                    player_invincible_fixture=args.protect_player,instrumented=True,
                    natural_playthrough=False,component_samples=rows)
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        session.capture('scene');print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
