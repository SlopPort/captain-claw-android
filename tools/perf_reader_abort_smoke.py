"""Verify a dead owned logcat client cannot pass sustained FPS evidence.

OpenAI Codex (LLM). Windows host only; select one phone with ANDROID_SERIAL.
Runs an isolated level-one observation, then terminates only the ADB logcat
child whose PID and parent match this test's own worker. Never kills the ADB
server, changes USB/network settings or edits player resources during play.
The performance worker restores its config/save in finally; verify exact bytes.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from gamepad_quit_smoke import PORT, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if os.name!='nt' or not os.environ.get('ANDROID_SERIAL'):
        raise RuntimeError('Requires Windows and an explicitly selected ANDROID_SERIAL')
    report=(PORT/'reports'/args.report).resolve()
    if report.parent!=(PORT/'reports').resolve() or report.exists():
        raise RuntimeError('Use a new direct report name')
    report.mkdir()
    worker_name=args.report+'-worker'
    worker_report=PORT/'reports'/worker_name
    if worker_report.exists():raise RuntimeError('Worker report already exists')
    output_path=report/'worker.txt'
    with output_path.open('wb') as output:
        worker=subprocess.Popen([sys.executable,str(PORT/'tools/gameplay_perf_smoke.py'),
            '--level','1','--seconds','20','--report',worker_name,'--observe','--quiet-diagnostics'],stdout=output,stderr=subprocess.STDOUT)
        until=time.monotonic()+90
        while time.monotonic()<until:
            if worker.poll() is not None:raise RuntimeError('Worker ended before interruption; see report')
            native=worker_report/'native.log'
            if native.exists() and 'Pazur benchmark quiet:' in native.read_text(errors='replace'):break
            time.sleep(.1)
        else:raise RuntimeError('Observation not ready; worker retains its bounded cleanup')
        reader=json.loads((worker_report/'log-reader.json').read_text())
        host_pid=int(reader['host_pid']);game_pid=int(reader['game_pid'])
        # Numeric interpolation only. Check direct parent AND executable/command
        # before terminating the exact client we intentionally own.
        command=(f"$client=Get-CimInstance Win32_Process -Filter 'ProcessId = {host_pid}'; "
            f"if ($null -eq $client -or $client.ParentProcessId -ne {worker.pid} "
            f"-or $client.Name -ine 'adb.exe' -or $client.CommandLine -notmatch '\\blogcat\\b' "
            f"-or $client.CommandLine -notmatch '--pid={game_pid}(?:\\s|$)') {{ throw 'Client ownership mismatch' }}; "
            f"Stop-Process -Id {host_pid}")
        subprocess.run(['powershell','-NoProfile','-Command',command],check=True,capture_output=True,text=True)
        code=worker.wait(timeout=50)
    text=output_path.read_text(errors='replace')
    if code==0 or 'Owned logcat reader stopped; sustained evidence is incomplete' not in text:
        raise RuntimeError('Expected explicit incomplete-evidence rejection; see worker output')
    if (worker_report/'results.json').exists():raise RuntimeError('Interrupted observation emitted a success result')
    for remote,original in [('config.xml','config.xml'),('SAVES.XML','SAVES.XML')]:
        actual=subprocess.run(['adb','exec-out','cat',REMOTE+remote],check=True,capture_output=True).stdout
        if actual!=(worker_report/original).read_bytes():raise RuntimeError('Restoration mismatch: '+remote)
    result={'passed':True,'owned_client_terminated':True,'incomplete_evidence_rejected':True,
            'config_and_save_restored':True,'adb_server_restarted':False}
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
