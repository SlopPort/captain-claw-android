"""Copy bounded local game-recorder reports without restarting or controlling play.

OpenAI Codex (LLM). Only an explicitly selected ADB device is used. This tool
copies gameplay diagnostics, not private Android logs, save files or media.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        raise RuntimeError('Select an allocated device using ANDROID_SERIAL')
    port=Path(__file__).resolve().parents[1]
    report=(port/'reports'/args.report).resolve()
    if not report.is_relative_to((port/'reports').resolve()):
        raise ValueError('Report must stay inside local reports')
    report.mkdir(parents=True,exist_ok=False)
    rows=[]
    for kind in ('rolling','event'):
        for slot in (0,1):
            name=f'flight-{kind}-{slot}.txt'
            remote='/sdcard/Android/data/pl.pazur.port/files/'+name
            result=subprocess.run(['adb','exec-out','cat',remote],capture_output=True)
            if result.returncode or not result.stdout.startswith(b'Pazur flight recorder 1 '):
                continue
            if not result.stdout.endswith(b'end\n'):
                raise RuntimeError('Incomplete recorder file: '+name)
            (report/name).write_bytes(result.stdout)
            rows.append(dict(file=name,bytes=len(result.stdout),header=result.stdout.splitlines()[0].decode()))
    (report/'collection.json').write_text(json.dumps(dict(files=rows,phone_files_changed=False),indent=2),encoding='utf-8')
    if not rows:
        raise RuntimeError('No reports yet; play an enabled debug 0.4.35+ build for at least five seconds')
    print(json.dumps(dict(files=len(rows),bytes=sum(row['bytes'] for row in rows),phone_files_changed=False)))


if __name__=='__main__':
    main()
