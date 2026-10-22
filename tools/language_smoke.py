"""PL/EN Android screens and an isolated English native preview, by Codex.

The instrumentation restores preferences/bindings; CampaignSession restores
configuration and progress. No system-wide input or network changes.
"""
import argparse
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb, REMOTE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    with CampaignSession(args.report,level=1) as session:
        output=adb('shell','am','instrument','-w','-r','-e','preview_native','true',
                   'pl.pazur.port.test/pl.pazur.port.LanguageTest')
        (session.report/'instrumentation.txt').write_text(output,encoding='utf-8')
        assert 'INSTRUMENTATION_CODE: 0' in output,output
        assert 'English native screenshot captured' in output,output
        filename=REMOTE+'language-english-native.png'
        adb('pull',filename,str(session.report/'english-native.png'))
        adb('shell','rm','-f',filename)
        print(output,flush=True)


if __name__=='__main__':main()
