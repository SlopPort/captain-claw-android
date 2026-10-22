"""App-local touch regression after live viewport changes, by OpenAI Codex.

No global input, display overrides or log clearing. Existing JumpTouchTest sends
MotionEvents directly to the focused game window. Isolated saves are restored.
"""
import argparse
import json
import re
import subprocess
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--scenario',choices=('jump','score','game-over'),default='jump')
    parser.add_argument('--expect-logical-size',type=int,nargs=2,default=[853,480],metavar=('W','H'))
    args=parser.parse_args()
    images={'jump':['jump-multitouch.png','jump-layout.png','jump-focus.png','jump-pause.png'],
            'score':['score-window-before.png','score-window-after.png'],
            'game-over':['game-over-before.png','game-over-after.png']}[args.scenario]
    for name in images:
        assert 'pazur-present' not in adb('shell','if [ -e '+REMOTE+name+' ]; then echo pazur-present; fi'),'Existing image: '+name
    with CampaignSession(args.report,level=1) as session:
        with (session.report/'window-native.log').open('wb') as output:
            reader=subprocess.Popen(['adb','logcat','-T','1','-s','SDL/APP','libc','AndroidRuntime'],stdout=output,stderr=subprocess.DEVNULL)
            try:
                result=adb('shell','am','instrument','-w','-r','-e','layout','final','-e','scenario',args.scenario,
                           'pl.pazur.port.test/pl.pazur.port.JumpTouchTest')
            finally:reader.terminate();reader.wait(timeout=5)
        (session.report/'instrumentation.txt').write_text(result,encoding='utf-8')
        for name in images:
            adb('pull',REMOTE+name,str(session.report/name),check=False)
            adb('shell','rm','-f',REMOTE+name)
        log=(session.report/'window-native.log').read_text(errors='replace')
        assert 'INSTRUMENTATION_CODE: 0' in result,result
        assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,'Crash'
        viewports=re.findall(r'Pazur viewport: physical=(\d+)x(\d+) logical=(\d+)x(\d+)',log)
        assert viewports and list(map(int,viewports[-1][2:]))==args.expect_logical_size,viewports
        evidence=dict(scenario=args.scenario,passed=False,viewport_events=viewports,input='focused game-window MotionEvents',
                      natural_playthrough=False,global_input=False,display_settings_changed=False)
        if args.scenario=='jump':
            rows=[dict(label=n,queue_ms=int(q),takeoff_ms=int(t),rise=float(h),hold_ms=int(d),jumps=int(j))
                  for n,q,t,h,d,j in re.findall(r'Pazur jump trace: label=(\S+) queue_ms=(\d+) takeoff_ms=(-?\d+) rise=([\d.]+) hold_ms=(\d+) jumps=(\d+)',log)]
            evidence['jump_cases']=rows
            (session.report/'results.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
            assert len(rows)==6,rows
            cases={row['label']:row for row in rows}
            assert all(cases[n]['rise']>=50 and cases[n]['jumps']==1 for n in ('hold10','hold100','drift100')),rows
            assert cases['hold700']['rise']>150 and cases['hold1800']['jumps']==1,rows
            assert all(0<=row['takeoff_ms']<=65 for row in rows),rows
            drift=log.split('Pazur console command: combatjumpmeasure drift100',1)[1].split('Pazur jump trace: label=drift100',1)[0]
            assert 'attack=1' not in drift and 'fire=1' not in drift,'Jump finger drift activated another action'
            states=[tuple(map(int,v)) for v in re.findall(r'Pazur controls: left=(\d) right=(\d) jump=(\d) attack=(\d) fire=(\d) up=(\d) down=(\d)',log)]
            for state in ((0,1,1,0,0,0,0),(0,0,1,0,0,0,0),(0,0,0,1,0,0,0),(0,0,0,0,1,0,0)):
                assert state in states,(state,states)
            assert states[-1]==(0,0,0,0,0,0,0),states[-4:]
        elif args.scenario=='score':
            assert 'Score screen initialized OK' in log and 'Level name: Claw - Level 2' in log,'Score transition missing'
        else:
            assert 'Pazur game over menu opened' in log and 'Changing to: 3' in log.split('Pazur game over menu opened',1)[1],'Game Over/menu transition missing'
        evidence['passed']=True
        (session.report/'results.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
        print(json.dumps(evidence),flush=True)


if __name__=='__main__':main()
