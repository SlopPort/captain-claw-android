"""Real menu navigation with focused Android window taps and local Escape keys.

OpenAI Codex. No controller emulation or global input. Source pages are not
declared visited merely because menu initialization generated their textures.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from campaign_session import CampaignSession
from android_log_evidence import crash_evidence
from gamepad_quit_smoke import adb, PORT, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    parser.add_argument('--stress-cycles',type=int,choices=range(0,101),default=0,metavar='0..100')
    parser.add_argument('--audio-sliders',action='store_true')
    parser.add_argument('--languages',nargs='+',choices=('en','pl'),default=['en','pl']);args=parser.parse_args()
    names=('main','help-index','help','single','levels','options','audio','credits','quit','returned','keyboard-return')
    if args.audio_sliders:names+=('audio-zero','audio-max','audio-cancel','audio-toggle')
    expected=['MenuPage_Help','MenuPage_Help_TouchScreen','MenuPage_Main',
              'MenuPage_SinglePlayer','MenuPage_SinglePlayer_NewGame','MenuPage_SinglePlayer','MenuPage_Main',
              'MenuPage_Options','MenuPage_Options_Audio','MenuPage_Options','MenuPage_Main',
              'MenuPage_Credits','MenuPage_Main','MenuPage_QuitGame','MenuPage_Main','MenuPage_QuitGame','MenuPage_Main']
    if args.stress_cycles:
        names=('main','stress-single')
        expected=['MenuPage_SinglePlayer','MenuPage_SinglePlayer_NewGame','MenuPage_SinglePlayer','MenuPage_Main']*args.stress_cycles
    base=next(x.removeprefix('package:') for x in adb('shell','pm','path','pl.pazur.port').splitlines() if x.endswith('/base.apk'))
    digest=hashlib.sha256()
    with subprocess.Popen(['adb','exec-out','cat',base],stdout=subprocess.PIPE) as process:
        while block:=process.stdout.read(1024*1024):digest.update(block)
        assert process.wait()==0,'APK hash failed'
    for language in args.languages:
        for name in names:
            assert 'occupied' not in adb('shell','if [ -e '+REMOTE+'menu-'+language+'-'+name+'.png ]; then echo occupied; fi'),'Existing screenshot'
        with CampaignSession(args.report+'-'+language,start_menu=True) as session:
            with (session.report/'menu-native.log').open('wb') as out:
                reader=subprocess.Popen(['adb','logcat','-T','1','-v','threadtime','-s','SDL/APP','libc','AndroidRuntime'],stdout=out,stderr=subprocess.DEVNULL)
                try:
                    intro='true' if os.environ.get('ANDROID_SERIAL','').startswith('emulator-') else 'false'
                    output=adb('shell','am','instrument','-w','-r','-e','language',language,'-e','cycles',str(args.stress_cycles),'-e','audio_sliders','true' if args.audio_sliders else 'false','-e','dismiss_intro',intro,'pl.pazur.port.test/pl.pazur.port.MenuTouchTest')
                finally:reader.terminate();reader.wait(timeout=5)
            (session.report/'instrumentation.txt').write_text(output,encoding='utf-8')
            for name in names:
                remote=REMOTE+'menu-'+language+'-'+name+'.png'
                adb('pull',remote,str(session.report/(name+'.png')),check=False);adb('shell','rm','-f',remote)
            log=(session.report/'menu-native.log').read_text(encoding='utf-8',errors='replace')
            pages=re.findall(r'Pazur menu page: (\S+)',log)
            result=dict(passed=False,language=language,apk_sha256=digest.hexdigest(),pages=pages,
                        audio_sliders_tested=args.audio_sliders,
                        expected_pages=expected,stress_cycles=args.stress_cycles,input='focused game-window touch and Escape',global_input=False,controller_input=False,
                        crash_evidence=crash_evidence(log))
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            assert 'INSTRUMENTATION_CODE: 0' in output,output
            crashes=result['crash_evidence']
            assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],'Game crash or unattributed fatal line: '+str(crashes)
            assert pages==expected,('Wrong page sequence',pages)
            if args.audio_sliders:
                adb('pull',REMOTE+'config.xml',str(session.report/'audio-after.xml'))
                volumes=re.findall(r'Pazur menu volume: channel=(\d) sound=(\d+) music=(\d+) soundOn=(\d) musicOn=(\d)',log)
                result['volume_commits']=volumes
                (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
                assert len(volumes)==6 and [v[0] for v in volumes]==['1','1','2','2','1','1'],volumes
                assert volumes[-1][1:3]==('50','20'),volumes
            shared=re.findall(r'Pazur menu hit test: item=((?:VOICE|AMBIENT)_\w+_BUTTON) box=[^\r\n]* state=(\d+) focusable=(\d+)',log)
            result['non_disabled_shared_sound_states']=sorted(set(row for row in shared if row[1:]!=('1','0')))
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            assert shared and not result['non_disabled_shared_sound_states'],'Mute/unmute re-enabled independent shared-sound controls'
            assert 'Pazur menu label fallback:' not in log,'System font unavailable'
            assert 'Could not switch to page:' not in log,'A disabled destination accepted input'
            assert 'Pazur unavailable menu page: item=MULTIPLAYER_BUTTON' in log,'Unavailable multiplayer not disabled'
            assert 'Pazur menu shared sound: item=VOICE_ON_BUTTON' in log and 'Pazur menu shared sound: item=AMBIENT_ON_BUTTON' in log,'Nonfunctional independent sound options not disabled'
            labels=re.findall(r'Pazur menu label: language=(en|pl) item=(\S+) box=(\d+)x(\d+) text=(\d+)x(\d+)',log)
            assert len(labels)>100 and all(row[0]==language for row in labels),'Wrong/missing native locale'
            assert all(int(tw)<=int(w) and int(th)<=int(h) for _,_,w,h,tw,th in labels),'Text exceeds item'
            result.update(passed=True,translated_image_states=len(labels),visual_review_required=True)
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            print(json.dumps(result),flush=True)


if __name__=='__main__':main()
