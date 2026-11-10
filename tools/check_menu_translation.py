"""Check every named text/action in the actual APK menu against runtime labels.

OpenAI Codex. This supplements visual review and real navigation; creating a
texture does not prove that its page was visited. Slider art is nonlinguistic.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


def menu_policy(menu):
    """Mirror native construction against the packaged XML, not a stale row list.

    Native Android Controls/Difficulty launch settings outside the XML. All
    other SwitchPage actions need a destination. Multiplayer is unavailable
    regardless of whether a data package happens to define its page.
    """
    pages={page.findtext('PageName') for page in menu.findall('MenuPage')}
    expected=set()
    omitted=set()
    for item in menu.findall('MenuPage/MenuItem'):
        name=item.findtext('Name')
        assert name is not None,'Unnamed source item'
        shortcut=name in ('CONTROLS_BUTTON','DIFFICULTY_BUTTON')
        missing=any(event.findtext('Type')=='SwitchPage' and
                    event.findtext('PageName') not in pages
                    for event in item.findall('GeneratedEvent'))
        if name=='MULTIPLAYER_BUTTON' or (missing and not shortcut):
            omitted.add(name)
        elif item.findtext('Type')!='Slider':
            expected.add(name)
    return expected,omitted


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    with args.apk.open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
    outcome=json.loads((args.report/'results.json').read_text(encoding='utf-8'))
    assert outcome['passed'] and outcome['apk_sha256']==sha,'Failed navigation or different APK'
    with zipfile.ZipFile(args.apk) as apk:support=apk.read('assets/import-support/ASSETS.ZIP')
    with zipfile.ZipFile(io.BytesIO(support)) as archive:
        menu=ET.fromstring(archive.read('MENU.XML'))
    expected,omitted=menu_policy(menu)
    log=(args.report/'menu-native.log').read_text(encoding='utf-8',errors='replace')
    observed={name for language,name in re.findall(r'Pazur menu label: language=(en|pl) item=(\S+)',log) if language==outcome['language']}
    missing=sorted(expected-observed)
    # Require runtime evidence for exclusions; source policy alone must not turn
    # an untranslated or accidentally missing row into a passing coverage claim.
    removed=set(re.findall(r'Pazur menu removed: (\S+) \(unsupported action\)',log))
    unconfirmed=sorted(omitted-removed)
    unexpected=sorted(removed & expected)
    result=dict(passed=not (missing or unconfirmed or unexpected),language=outcome['language'],apk_sha256=sha,
                support_sha256=hashlib.sha256(support).hexdigest(),expected_items=len(expected),
                missing=missing,omitted_items=sorted(omitted),unconfirmed_removals=unconfirmed,
                unexpected_removals=unexpected,scope='main-menu definitions including help, credits, audio and checkpoint pages; not original background/voice translation')
    (args.report/'translation-coverage.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result));assert result['passed'],result


if __name__=='__main__':main()
