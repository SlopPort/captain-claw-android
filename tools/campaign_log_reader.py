"""Read logs for an existing owned campaign; never restart ADB or the game.

OpenAI Codex (LLM). Select a device with ANDROID_SERIAL. The campaign owner must
remain alive; this sidecar does not enter a fixture context or restore files.
Create native-reader.stop in its report directory to stop only this reader.
"""
import argparse
import re
import subprocess
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    session=CampaignSession(args.report)
    for name in ('config.original.xml','saves.original.xml'):
        if not (session.report/name).is_file():
            raise RuntimeError('No owned campaign backup: '+name)
    stop=session.report/'native-reader.stop'
    if stop.exists():
        raise RuntimeError('Reader stop marker already exists')
    session.pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
    path=session.report/'native.log'
    stamps=re.findall(r'(?m)^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) ',session.logs())
    session.output=path.open('ab')
    # The parent already owns these backups; this reader never invokes __exit__.
    session.backed_up=True
    session.stream=subprocess.Popen(session.log_command(stamps[-1] if stamps else None),
                                    stdout=session.output,stderr=subprocess.DEVNULL)
    last_client_pid=None
    try:
        while not stop.exists():
            session.ensure_log_stream()
            if session.stream.pid != last_client_pid:
                (session.report/'native-reader-client.pid').write_text(str(session.stream.pid),encoding='ascii')
                last_client_pid=session.stream.pid
            time.sleep(.3)
    finally:
        if session.stream.poll() is None:
            session.stream.terminate()
            session.stream.wait(timeout=5)
        session.output.close()


if __name__=='__main__':
    main()
