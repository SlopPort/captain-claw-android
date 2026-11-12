"""Compile the actual tile converter against an independent REA-bound oracle.

OpenAI Codex (LLM). Synthetic tiles only; no phone/original execution. Exit 1
means a recorded conversion mismatch, not successful parity acceptance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PORT=Path(__file__).resolve().parents[1]


def function(source, signature):
    start=source.index(signature)
    # Ignore strings/comments when locating matching braces; retain the exact
    # original source slice in the private generated compilation input.
    masked=re.sub(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"',
                  lambda match:' '*len(match.group()), source)
    opening=masked.index('{',start); depth=0
    for end in range(opening,len(masked)):
        if masked[end]=='{': depth+=1
        elif masked[end]=='}':
            depth-=1
            if depth==0: return source[start:end+1]
    raise ValueError('Unclosed source function')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--compiler')
    args=parser.parse_args()
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()): parser.error('Private reports only')
    report.mkdir(parents=True,exist_ok=False)
    compiler=args.compiler or shutil.which('g++')
    if not compiler: parser.error('Supply a host C++ compiler')
    source_path=PORT/'upstream/OpenClaw/OpenClaw/Engine/Util/Util.cpp'
    raw=source_path.read_bytes(); source=raw.decode('utf-8')
    extracted='\n'.join(function(source,name) for name in
        ('inline bool IsInBetween(', 'void ParseCollisionRectanglesFromTile('))
    (report/'tile_source.inc').write_text(extracted,encoding='utf-8')
    result=dict(source_sha256=hashlib.sha256(raw).hexdigest(),
        harness_sha256=hashlib.sha256((PORT/'tests/tile_partition_audit.cpp').read_bytes()).hexdigest(),
        scope='Actual extracted OpenClaw function, synthetic 64x64 tiles; no runtime/campaign claim')
    executable=report/'tile_partition_audit.exe'
    # Keep MinGW's compiler helpers on their own DLL set without changing the
    # user's global PATH (other installed toolchains may expose the same names).
    environment=os.environ.copy()
    environment['PATH']=str(Path(compiler).resolve().parent)+os.pathsep+environment.get('PATH','')
    build=subprocess.run([compiler,'-std=c++17','-O0','-static','-I',str(report),
        str(PORT/'tests/tile_partition_audit.cpp'),'-o',str(executable)],capture_output=True,text=True,env=environment)
    (report/'compile.log').write_text(build.stdout+build.stderr,encoding='utf-8')
    build.check_returncode()
    run=subprocess.run([str(executable)],capture_output=True,text=True,env=environment)
    (report/'stdout.json').write_text(run.stdout,encoding='utf-8')
    (report/'stderr.txt').write_text(run.stderr,encoding='utf-8')
    result.update(json.loads(run.stdout),returncode=run.returncode)
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    raise SystemExit(run.returncode)


if __name__=='__main__': main()
