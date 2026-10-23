"""Read-only prepublication scan of reachable Git history; OpenAI Codex (LLM).

Findings are file/object references only, never credential contents. Optional
private patterns must be kept outside tracked sources. This heuristic is not
proof of absence of all secrets or a legal assessment of asset ownership.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

FORBIDDEN_PREFIXES=('upstream/','reports/','build/','dist/','.gradle/',
                    '.npm-cache/','app/build/','app/.cxx/',
                    'app/src/main/assets/music/','app/src/main/assets/import-support/')
FORBIDDEN_SUFFIXES=('.apk','.aab','.rez','.pat','.exe','.dll','.so','.jks',
                    '.keystore','.mp4','.wmv','.avi','.wav','.mp3')
TOKEN=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')


def git(*args):
    return subprocess.check_output(['git',*args])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-pattern-file',type=Path)
    args=parser.parse_args()
    patterns=[]
    if args.private_pattern_file:
        patterns=[v.strip().lower().encode('utf-8') for v in args.private_pattern_file.read_text(encoding='utf-8-sig').splitlines() if v.strip()]
    findings=[]
    # Inspect every changed historical path, including removed files. A blob may
    # have appeared under several names; rev-list's single path hint is not enough.
    historical_paths=set(git('log','--all','--format=','--name-only','-z').decode('utf-8').split('\0'))
    for raw in sorted(historical_paths):
        name=raw.strip('\n')
        if name.lower().startswith(FORBIDDEN_PREFIXES) or name.lower().endswith(FORBIDDEN_SUFFIXES):
            findings.append({'path':name,'reason':'excluded_historical_path'})
    rows=git('rev-list','--objects','--all').decode('utf-8').splitlines()
    paths={v.split(' ',1)[0]:v.split(' ',1)[1] for v in rows if ' ' in v}
    meta=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype)'],input='\n'.join(paths)+'\n',text=True,capture_output=True,check=True).stdout.splitlines()
    blobs=[v.split()[0] for v in meta if v.endswith(' blob')]
    total=0
    with subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE) as reader:
        for oid in blobs:
            reader.stdin.write((oid+'\n').encode('ascii'));reader.stdin.flush()
            header=reader.stdout.readline().split();size=int(header[2])
            data=reader.stdout.read(size);reader.stdout.read(1);total+=size
            reasons=[]
            if size>10*1024*1024:reasons.append('large_blob')
            if TOKEN.search(data):reasons.append('credential_pattern')
            if any(v in data.lower() for v in patterns):reasons.append('private_pattern')
            if reasons:findings.append({'object':oid,'path_hint':paths[oid],'reasons':reasons})
        reader.stdin.close()
        reader.wait()
    print(json.dumps({'reachable_blobs':len(blobs),'bytes_scanned':total,'findings':findings},indent=2))
    raise SystemExit(bool(findings))


if __name__=='__main__':
    main()
