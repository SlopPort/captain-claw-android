"""Controlled input-routing and balance fixture; never a natural campaign run."""
from campaign_session import CampaignSession
import argparse,json
from android_package import installed_apk_sha256
p=argparse.ArgumentParser();p.add_argument('--report',required=True);args=p.parse_args()
with CampaignSession(args.report) as session:
    start=len(session.logs());session.command('gameplayoptionscheck')
    session.wait('Pazur gameplay options fixture:',after=start)
    log=session.logs()[start:]
    passed='Pazur gameplay options fixture: passed=1' in log
    result={'passed':passed,'fixture':True,'natural_campaign':False,'apk_sha256':installed_apk_sha256(),
            'checks':['four layouts x three movement modes','direction drag-out and re-entry','release clears movement','custom button bounds',
                      'player damage 5/10/15 for base 10','healing 15/10/5 for base 10']}
    (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert passed,log
    print(json.dumps(result))
