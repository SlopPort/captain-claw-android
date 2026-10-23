"""Production launcher cancellation, invalid stream and full user's REZ import.

OpenAI Codex (LLM). Select an allocated phone with ANDROID_SERIAL. Default modes inject the picker result; picker-cancel and picker-rez use the
real system picker. ContentProvider lives in test APK only;
random capability authorizes one read-only fixture. No shell permissions adopted
by the target app. Host restores all replaced support files/config/save, verifies
REZ identity and removes the test provider's private copy/token. No game traversal.
"""
import argparse
import json
import os
import secrets
import zipfile
import shutil
import subprocess
from gamepad_quit_smoke import adb, PORT, REMOTE
from android_package import installed_apk_sha256


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--only',nargs='+',choices=('picker-cancel','cancel','invalid','rez','zip','traversal','bad-config','duplicate','missing','crc','picker-rez'))
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select one allocated device')
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    provider='/sdcard/Android/data/pl.pazur.port.test/files/'
    names=['ASSETS.ZIP','config.xml','clacon.ttf','console02.tga','SAVES.XML']
    for name in ('import-transaction','import-stream-fixture','combat-command.txt','SAVES.pending.xml'):
        if subprocess.run(['adb','shell','test','-e',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing fixture/transaction: '+name)
    for name in ('import-stream-fixture','import-stream-token','import-stream-original.rez'):
        if subprocess.run(['adb','shell','test','-e',provider+name],capture_output=True).returncode==0:raise RuntimeError('Existing provider fixture')
    apk=installed_apk_sha256()
    adb('shell','am','force-stop','pl.pazur.port')
    for name in names:adb('pull',REMOTE+name,str(report/name))
    original_rez=adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]
    token=secrets.token_hex(16);(report/'token').write_text(token+'\n',encoding='ascii')
    (report/'invalid.rez').write_bytes(bytes(168))
    results=[];copy_ready=False;public_folder_created=False
    public_folder='/sdcard/Download/000-pazur-'+token[:12]
    public_fixture=public_folder+'/CLAW.REZ'
    if subprocess.run(['adb','shell','test','-e',public_fixture],capture_output=True).returncode==0:raise RuntimeError('Existing download fixture')
    try:
        adb('shell','mkdir','-p',provider)
        adb('push',str(report/'token'),provider+'import-stream-token')
        adb('shell','cp',REMOTE+'CLAW.REZ',provider+'import-stream-original.rez')
        assert adb('shell','sha256sum',provider+'import-stream-original.rez').split()[0]==original_rez
        copy_ready=True  # Restore only from a verified complete source copy.
        for mode in (args.only or ('picker-cancel','cancel','invalid','rez')):
            adb('shell','am','force-stop','pl.pazur.port')
            for name in ('ASSETS.ZIP','config.xml','clacon.ttf','console02.tga'):
                adb('push',str(report/name),REMOTE+name)
            # Isolate missing-font startup to reach the real first-install UI;
            # local backup is restored even after a test failure.
            adb('shell','rm','-f',REMOTE+'clacon.ttf')
            if mode=='picker-rez':
                adb('shell','mkdir',public_folder);public_folder_created=True
                adb('shell','cp',provider+'import-stream-original.rez',public_fixture)
            if mode=='invalid':adb('push',str(report/'invalid.rez'),provider+'import-stream-fixture')
            if mode=='rez':
                adb('shell','cp',provider+'import-stream-original.rez',provider+'import-stream-fixture')
                assert adb('shell','sha256sum',provider+'import-stream-fixture').split()[0]==original_rez
            if mode in ('zip','traversal','bad-config','duplicate','missing','crc'):
                archive=report/(mode+'.zip')
                with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as packed:
                    if mode=='traversal':packed.writestr('../SAVES.XML','not permitted')
                    elif mode in ('duplicate','missing','crc'):
                        packed.writestr('config.xml',(report/'config.xml').read_bytes(),compress_type=zipfile.ZIP_STORED)
                        if mode=='duplicate':packed.writestr('config.xml',(report/'config.xml').read_bytes(),compress_type=zipfile.ZIP_STORED)
                    else:
                        for name in ('ASSETS.ZIP','config.xml','clacon.ttf','console02.tga'):
                            if name=='config.xml' and mode=='bad-config':packed.writestr(name,'<Configuration>')
                            else:packed.write(report/name,name)
                        with subprocess.Popen(['adb','exec-out','cat',provider+'import-stream-original.rez'],stdout=subprocess.PIPE) as source:
                            with packed.open('CLAW.REZ','w') as out:shutil.copyfileobj(source.stdout,out,65536)
                            assert source.wait()==0,'Cannot read source fixture'
                if mode=='crc':
                    with archive.open('r+b') as corrupt:
                        corrupt.seek(30+len('config.xml')+10);old=corrupt.read(1);corrupt.seek(-1,1);corrupt.write(bytes([old[0]^1]))
                adb('push',str(archive),provider+'import-stream-fixture')
            output=subprocess.run(['adb','shell','am','instrument','-w','-r','-e','mode',mode,'-e','uri',
                'content://pl.pazur.port.test.importstream/'+token+'/fixture','-e','pick_name',public_fixture.rsplit('/',1)[1],'-e','pick_dir','primary:Download/'+public_folder.rsplit('/',1)[1],
                'pl.pazur.port.test/pl.pazur.port.ImportFlowTest'],check=True,capture_output=True,text=True,timeout=180).stdout
            (report/(mode+'.txt')).write_text(output,encoding='utf-8')
            assert 'INSTRUMENTATION_CODE: 0' in output and 'PASS: '+mode in output,output
            assert adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]==original_rez,'REZ changed'
            assert subprocess.check_output(['adb','exec-out','cat',REMOTE+'SAVES.XML'])==(report/'SAVES.XML').read_bytes(),'Save changed'
            if mode not in ('rez','zip','picker-rez'):
                for name in ('ASSETS.ZIP','config.xml','console02.tga'):
                    assert subprocess.check_output(['adb','exec-out','cat',REMOTE+name])==(report/name).read_bytes(),name+' changed after '+mode
            results.append(dict(mode=mode,passed=True,picker_result_injected=mode not in ('picker-cancel','picker-rez')))
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        recovery=adb('shell','am','instrument','-w','-r','-e','mode','recover','pl.pazur.port.test/pl.pazur.port.ImportFlowTest')
        (report/'cleanup-recovery.txt').write_text(recovery,encoding='utf-8')
        if 'PASS: recover' not in recovery or 'INSTRUMENTATION_CODE: 0' not in recovery:
            raise RuntimeError('Cleanup recovery failed; retain backups/provider copy for manual recovery')
        adb('shell','am','force-stop','pl.pazur.port')
        # If success did not preserve source identity, retain the provider copy
        # as a recovery source rather than deleting the only known-good bytes.
        current=adb('shell','sha256sum',REMOTE+'CLAW.REZ',check=False).split()
        if not current or current[0]!=original_rez:
            if not copy_ready:raise RuntimeError('REZ mismatch; provider copy unavailable, retain report')
            adb('shell','cp',provider+'import-stream-original.rez',REMOTE+'CLAW.REZ')
        for name in names:adb('push',str(report/name),REMOTE+name)
        for name in names:
            assert subprocess.check_output(['adb','exec-out','cat',REMOTE+name])==(report/name).read_bytes(),'Restore mismatch: '+name
        assert adb('shell','sha256sum',REMOTE+'CLAW.REZ').split()[0]==original_rez
        if public_folder_created:
            adb('shell','rm','-f',public_fixture)
            adb('shell','rmdir',public_folder)
        adb('shell','rm','-f',provider+'import-stream-fixture',provider+'import-stream-token',provider+'import-stream-original.rez')
        print('Original game/support/config/save bytes restored; provider capability removed',flush=True)
    result=dict(passed=True,apk_sha256=apk,cases=results,ordinary_app_permissions=True,
                picker_result_injected=any(case['picker_result_injected'] for case in results),natural_playthrough=False,restored=True)
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
