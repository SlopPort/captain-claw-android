"""Save Activity lifetime regression with an isolated, gated provider.

OpenAI Codex (LLM). Select an allocated device explicitly. Does not replace game
files or user progress. Old-APK expected-crash mode requires a real BadTokenException
AND a completed exact export; a generic process crash is never a passing baseline.
"""
import argparse
import json
import hashlib
import re
import os
import secrets
import subprocess
from gamepad_quit_smoke import PORT,REMOTE,adb
from android_package import installed_apk_sha256

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report',required=True)
parser.add_argument('--expect-crash',action='store_true')
args=parser.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select one allocated device')
report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
provider='/sdcard/Android/data/pl.pazur.port.test/files/'
for name in ('import-stream-token','save-stream-output.xml'):
 if 'pazur-fixture-present' in adb('shell','if [ -e '+provider+name+' ]; then echo pazur-fixture-present; fi',check=False):raise RuntimeError('Existing provider fixture')
before={name:subprocess.check_output(['adb','exec-out','cat',REMOTE+name]) for name in ('config.xml','SAVES.XML')}
apk=installed_apk_sha256();token=secrets.token_hex(16);(report/'token').write_text(token+'\n',encoding='ascii')
reader=None
try:
 adb('shell','am','force-stop','pl.pazur.port');adb('shell','mkdir','-p',provider)
 adb('push',str(report/'token'),provider+'import-stream-token')
 with (report/'runtime.log').open('wb') as stream:
  reader=subprocess.Popen(['adb','logcat','-T','1','-v','threadtime','-s','AndroidRuntime'],stdout=stream,stderr=subprocess.DEVNULL)
  output=subprocess.run(['adb','shell','am','instrument','-w','-r','-e','uri',
   'content://pl.pazur.port.test.importstream/'+token+'/export','-e','token',token,
   'pl.pazur.port.test/pl.pazur.port.LateSaveActivityTest'],check=True,capture_output=True,text=True,timeout=40).stdout
  reader.terminate();reader.wait(timeout=5);reader=None
 (report/'instrumentation.txt').write_text(output,encoding='utf-8')
 runtime=(report/'runtime.log').read_text(errors='replace')
 exported=subprocess.check_output(['adb','exec-out','cat',provider+'save-stream-output.xml'])
 (report/'exported.xml').write_bytes(exported)
 expected=re.search(r'expected_export_sha256=([0-9a-f]{64})',output)
 assert expected and hashlib.sha256(exported).hexdigest()==expected[1],'Canonical export not completed before lifecycle outcome'
 real_crash='WindowManager$BadTokenException' in runtime and 'Process: pl.pazur.port,' in runtime
 if args.expect_crash:assert real_crash and 'PASS: export' not in output,'Expected exact old-APK late-dialog crash missing'
 else:assert not real_crash and 'INSTRUMENTATION_CODE: 0' in output and 'PASS: export' in output,output
 result=dict(passed=True,apk_sha256=apk,expected_old_crash=args.expect_crash,bad_token_crash_observed=real_crash,
  exact_export_completed=True,ordinary_app_permissions=True,picker_ui_tested=False)

finally:
 if reader is not None:reader.terminate();reader.wait(timeout=5)
 adb('shell','am','force-stop','pl.pazur.port')
 for name,original in before.items():assert subprocess.check_output(['adb','exec-out','cat',REMOTE+name])==original,'User file changed: '+name
 adb('shell','rm','-f',provider+'import-stream-token',provider+'save-stream-output.xml')
 print('Original config/progress unchanged; provider fixtures removed',flush=True)

result['original_config_and_progress_unchanged']=True
result['provider_fixtures_removed']=True
(report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
