"""Visible PL/EN save failure messages; no progress or provider files replaced.

OpenAI Codex (LLM). Requires an explicitly allocated device and default test APK.
The instrumentation restores language. Host verifies user files and APK identity.
"""
import argparse
import json
import os
import subprocess
from android_package import installed_apk_sha256
from gamepad_quit_smoke import adb, PORT, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    report.mkdir(parents=True,exist_ok=False)
    before={n:subprocess.check_output(['adb','exec-out','cat',REMOTE+n]) for n in ('config.xml','SAVES.XML')}
    apk=installed_apk_sha256()
    result=dict(passed=False,apk_sha256=apk,picker_ui_tested=False,natural_playthrough=False)
    try:
        adb('shell','am','force-stop','pl.pazur.port')
        execution=subprocess.run(['adb','shell','am','instrument','-w','-r','pl.pazur.port.test/pl.pazur.port.SaveErrorMessagesTest'],capture_output=True,text=True,timeout=60)
        output=execution.stdout
        (report/'instrumentation.txt').write_text(output,encoding='utf-8')
        (report/'instrumentation-stderr.txt').write_text(execution.stderr,encoding='utf-8')
        assert execution.returncode==0,execution.stderr
        assert 'INSTRUMENTATION_CODE: 0' in output and 'PASS: four actual provider failures' in output,output
        result['passed']=True
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        result['user_files_unchanged']=all(subprocess.check_output(['adb','exec-out','cat',REMOTE+n])==data for n,data in before.items())
        result['apk_unchanged']=installed_apk_sha256()==apk
        result['passed']=result['passed'] and result['user_files_unchanged'] and result['apk_unchanged']
        (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        assert result['user_files_unchanged'] and result['apk_unchanged'],result
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
