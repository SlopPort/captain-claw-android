"""Check an APK's contents for known private strings and credential markers.

OpenAI Codex (LLM). Added after real native .rodata filename disclosures.
Reports member names/reasons only, never matched contents. Private patterns must
stay outside public source. This heuristic is not copyright/security clearance.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
from check_public_history import TOKEN


def inspect(apk, private_pattern_file=None):
    patterns=[]
    if private_pattern_file:
        for line in private_pattern_file.read_text(encoding='utf-8-sig').splitlines():
            value=line.strip().lower()
            if value:
                patterns.extend((value.encode('utf-8'),value.encode('utf-16le')))
    findings=[]
    members=0

    def member(name,data):
        nonlocal members
        members+=1
        reasons=[]
        if TOKEN.search(data):reasons.append('credential_pattern')
        folded=data.lower()
        if any(value in folded for value in patterns):reasons.append('private_pattern')
        if reasons:findings.append(dict(member=name,reasons=reasons))

    with zipfile.ZipFile(apk) as package:
        for name in package.namelist():
            data=package.read(name)
            member(name,data)
            # The generated support archive is part of the installed product;
            # checking only its compressed bytes would miss contained strings.
            if name=='assets/import-support/ASSETS.ZIP':
                with zipfile.ZipFile(io.BytesIO(data)) as support:
                    for inner in support.namelist():member(name+'!'+inner,support.read(inner))
    with apk.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return dict(passed=not findings,apk_sha256=digest,members_checked=members,
                private_patterns_supplied=bool(patterns),findings=findings,
                scope='Known UTF-8/UTF-16LE private strings and credential markers; not independent copyright/security clearance')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk',type=Path)
    parser.add_argument('--private-pattern-file',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    result=inspect(args.apk,args.private_pattern_file)
    text=json.dumps(result,indent=2)
    if args.report:args.report.write_text(text+'\n',encoding='utf-8')
    print(text)
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
