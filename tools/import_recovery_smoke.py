"""Actual app-process deaths during import publication AND recovery.

OpenAI Codex. Tiny isolated fixtures only; no USB/network changes, controller
events, global input or replacement of real game data. Intentional process deaths
are required test evidence, not accidental native crashes or complete import UX.
"""
import argparse
import hashlib
import json
import re
import subprocess
from gamepad_quit_smoke import adb, PORT, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    report=PORT/'reports'/args.report
    report.mkdir(parents=True,exist_ok=False)
    assert 'occupied' not in adb('shell','if [ -e '+REMOTE+'import-transaction-test ]; then echo occupied; fi'),'Existing test fixture'
    package=adb('shell','pm','path','pl.pazur.port').strip()
    base=next(line.removeprefix('package:') for line in package.splitlines() if line.endswith('/base.apk'))
    digest=hashlib.sha256()
    with subprocess.Popen(['adb','exec-out','cat',base],stdout=subprocess.PIPE) as process:
        while block:=process.stdout.read(1024*1024):digest.update(block)
        assert process.wait()==0,'Cannot hash installed APK'
    version=re.search(r'versionName=(\S+)',adb('shell','dumpsys','package','pl.pazur.port'))[1]
    results=[]
    adb('shell','am','force-stop','pl.pazur.port')
    for mode in ('empty','partial','full'):
        for phase in ('kill-publish','kill-recover','verify'):
            output=adb('shell','am','instrument','-w','-r','-e','phase',phase,'-e','mode',mode,
                       'pl.pazur.port.test/pl.pazur.port.ImportRecoveryTest',check=False)
            (report/(mode+'-'+phase+'.txt')).write_text(output,encoding='utf-8')
            if phase=='verify':assert 'INSTRUMENTATION_CODE: 0' in output and 'PASS:' in output,output
            else:assert 'Process crashed' in output or 'Process killed' in output,output
        results.append(dict(mode=mode,publication_process_death=True,recovery_process_death=True,
                            rollback_verified=True,save_sentinel_preserved=True))
    (report/'results.json').write_text(json.dumps(dict(passed=True,version=version,apk_sha256=digest.hexdigest(),
        scope='isolated small fixtures; actual process death; not low-storage/power-loss or picker UX',
        modes=results),indent=2),encoding='utf-8')
    print('PASS: actual publication and recovery process deaths, empty/partial/full original sets; real game data untouched',flush=True)


if __name__=='__main__':main()
