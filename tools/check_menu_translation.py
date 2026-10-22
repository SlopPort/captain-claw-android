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
    expected={item.findtext('Name') for item in menu.findall('MenuPage/MenuItem') if item.findtext('Type')!='Slider'}
    assert None not in expected,'Unnamed source item'
    log=(args.report/'menu-native.log').read_text(encoding='utf-8',errors='replace')
    observed={name for language,name in re.findall(r'Pazur menu label: language=(en|pl) item=(\S+)',log) if language==outcome['language']}
    missing=sorted(expected-observed)
    result=dict(passed=not missing,language=outcome['language'],apk_sha256=sha,
                support_sha256=hashlib.sha256(support).hexdigest(),expected_items=len(expected),
                missing=missing,scope='main-menu definitions including help, credits, audio and checkpoint pages; not original background/voice translation')
    (args.report/'translation-coverage.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result));assert not missing,missing


if __name__=='__main__':main()
