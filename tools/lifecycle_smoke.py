"""Own-app focus transition and held-controller release regression by Codex.

Uses an isolated level and virtual pad, not a physical Bluetooth transport test.
No global Android keys or network/settings changes. User files are restored.
"""
import argparse
import json
import re
import subprocess
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import adb


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    apk_sha256=installed_apk_sha256()
    with CampaignSession(args.report,level=1) as session:
        with (session.report/'lifecycle-native.log').open('wb') as out:
            reader=subprocess.Popen(['adb','logcat','-T','1','-s','SDL/APP','libc','AndroidRuntime'],stdout=out,stderr=subprocess.DEVNULL)
            try:output=adb('shell','am','instrument','-w','-r','pl.pazur.port.test/pl.pazur.port.LifecycleTest')
            finally:reader.terminate();reader.wait(timeout=5)
        (session.report/'instrumentation.txt').write_text(output,encoding='utf-8')
        assert 'INSTRUMENTATION_CODE: 0' in output,output
        log=(session.report/'lifecycle-native.log').read_text(errors='replace')
        assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,'Crash'
        def positions(label):
            return [float(x) for x in re.findall(r'ladder trace: label='+label+r' .*? x=([-\d.]+)',log)]
        held=positions('lifecycle-held-resume');repress=positions('lifecycle-repress')
        assert len(held)>=5 and max(held)-min(held)<2,held
        assert len(repress)>=3 and max(repress)-min(repress)>20,repress
        assert installed_apk_sha256()==apk_sha256,'Package changed during lifecycle test'
        result=dict(passed=True,apk_sha256=apk_sha256,held_axis_after_resume_drift=max(held)-min(held),
                    repress_movement=max(repress)-min(repress),physical_controller=False,
                    fixtures=['isolated level start','virtual SDL controller'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
