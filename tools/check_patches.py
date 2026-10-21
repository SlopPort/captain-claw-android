"""Apply both source patches to clean copies of their changed files.

Never reverses/resets the developer's actual upstream working trees.
"""
from pathlib import Path
import subprocess
import tempfile

PORT=Path(__file__).resolve().parents[1]


def main():
    reports=PORT/'reports';reports.mkdir(exist_ok=True)
    for name,patch in [('OpenClaw','openclaw-android.patch'),('SDL','sdl-android.patch')]:
        source=PORT/'upstream'/name
        git=['git','-c','safe.directory='+source.as_posix(),'-C',str(source)]
        paths=subprocess.check_output(git+['diff','--name-only','-z']).decode('utf-8').split('\0')
        paths=[p for p in paths if p]
        with tempfile.TemporaryDirectory(prefix='patch-check-',dir=reports) as temporary:
            clean=Path(temporary).resolve()
            assert clean.is_relative_to(reports.resolve()) # Bounds auto-cleanup to the report workspace.
            for name_in_repo in paths:
                file=clean/name_in_repo;assert file.resolve().is_relative_to(clean)
                original=subprocess.run(git+['show','HEAD:'+name_in_repo],capture_output=True)
                if original.returncode==0:file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(original.stdout)
            subprocess.run(['git','init','-q',str(clean)],check=True)
            apply=['git','-c','safe.directory='+clean.as_posix(),'-C',str(clean),'apply']
            subprocess.run(apply+['--check',str(PORT/'patches'/patch)],check=True)
            subprocess.run(apply+[str(PORT/'patches'/patch)],check=True)
            for name_in_repo in paths:
                actual=clean/name_in_repo;wanted=source/name_in_repo
                assert actual.is_file()==wanted.is_file(),name_in_repo
                # Git attributes normalize some legacy CRLF files. Compare every
                # other byte, including the original source encoding.
                if actual.is_file():assert actual.read_bytes().replace(b'\r\n',b'\n')==wanted.read_bytes().replace(b'\r\n',b'\n'),name_in_repo
            print(patch+': clean apply matches '+str(len(paths))+' changed source files (CRLF normalized)')


if __name__=='__main__':main()
