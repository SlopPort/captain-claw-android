"""Build an archived Git revision with fresh sources and local pinned dependencies.

OpenAI Codex (LLM). No checkout resets, deletions, APK installs or downloads.
Uses the installed SDK/JDK and Gradle's existing dependency cache; this is a
clean source/native-object check, not a clean-machine or offline SDK bootstrap.
Shared Git objects are read from existing upstream repositories; no working
tree modifications from them are copied. Every output stays in a new report.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import sys
import zipfile


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision',default='HEAD')
    parser.add_argument('--report',required=True)
    parser.add_argument('--abis',default='arm64-v8a,armeabi-v7a')
    args=parser.parse_args()
    # Fail before cloning dependencies when Gradle would inherit an old JRE.
    # This machine can have Java 8 on PATH beside Android Studio's current JDK.
    executable='java.exe' if os.name=='nt' else 'java'
    java=Path(os.environ['JAVA_HOME'])/'bin'/executable if os.environ.get('JAVA_HOME') else Path(shutil.which('java') or executable)
    compiler=java.with_name('javac.exe' if os.name=='nt' else 'javac')
    if not java.is_file() or not compiler.is_file():parser.error('Set JAVA_HOME to a full JDK 17 or newer (for example Android Studio jbr).')
    java_version=subprocess.check_output([str(java),'-version'],stderr=subprocess.STDOUT,text=True).strip()
    major=re.search(r'version "(\d+)',java_version)
    if not major or int(major[1])<17:parser.error('This Android build needs JDK 17 or newer; set JAVA_HOME before retrying. Selected: '+java_version.splitlines()[0])
    port=Path(__file__).resolve().parents[1]
    report=(port/'reports'/args.report).resolve()
    if not report.is_relative_to((port/'reports').resolve()):raise ValueError('Report must stay under reports')
    report.mkdir(parents=True,exist_ok=False)
    source=report/'source';source.mkdir()
    def git(path):return ['git','-c','safe.directory='+path.as_posix(),'-C',str(path)]
    revision=subprocess.check_output(git(port)+['rev-parse',args.revision+'^{commit}'],text=True).strip()
    archive=subprocess.check_output(git(port)+['archive','--format=zip',revision])
    # Archive content is our local Git tree, never an untrusted downloaded ZIP.
    with zipfile.ZipFile(io.BytesIO(archive)) as package:package.extractall(source)
    metadata=dict(revision=revision,source_zip_sha256=hashlib.sha256(archive).hexdigest(),
                  abis=args.abis,passed=False,installed_toolchain_and_cached_gradle=True,
                  clean_machine=False,upstream_worktree_changes_copied=False,java_version=java_version)
    def run(command,cwd=source):
        print(command[0]+' '+(' '.join(map(str,command[1:3]))),flush=True)
        subprocess.run(command,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True)
    with (report/'build.log').open('wb') as log:
        try:
            dependencies=json.loads((source/'sources.lock.json').read_text())
            for entry in dependencies:
                target=source/'upstream'/entry['name']
                run(['git','clone','--shared','--no-checkout',str(port/'upstream'/entry['name']),str(target)])
                run(git(target)+['checkout','--detach',entry['commit']])
            ttf=source/'upstream/SDL_ttf'
            run(git(ttf)+['config','submodule.external/freetype.url',str(port/'upstream/SDL_ttf/external/freetype')])
            run(git(ttf)+['-c','protocol.file.allow=always','submodule','update','--init','external/freetype'])
            for name,patch in [('OpenClaw','openclaw-android.patch'),('SDL','sdl-android.patch')]:
                run(git(source/'upstream'/name)+['apply','--check',str(source/'patches'/patch)])
                run(git(source/'upstream'/name)+['apply',str(source/'patches'/patch)])
            wrapper=source/('gradlew.bat' if os.name=='nt' else 'gradlew')
            run([str(wrapper),'--offline','--no-daemon','--console=plain','-Pabis='+args.abis,':app:assembleDebug'])
            apk=source/'app/build/outputs/apk/debug/app-debug.apk'
            metadata.update(passed=True,apk_sha256=hashlib.sha256(apk.read_bytes()).hexdigest())
        finally:(report/'results.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps(metadata),flush=True)


if __name__=='__main__':main()
