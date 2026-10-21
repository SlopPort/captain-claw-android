"""Fetch locked engine/library revisions and apply the Android adaptation."""
import json
from pathlib import Path
import subprocess

PORT = Path(__file__).resolve().parents[1]


def run(args, check=True):
    return subprocess.run(args, check=check)


def git(dest):
    return ['git', '-c', 'safe.directory='+dest.resolve().as_posix(), '-C', str(dest)]


def main():
    for entry in json.loads((PORT / 'sources.lock.json').read_text()):
        dest = PORT / 'upstream' / entry['name']
        if not dest.exists():
            run(['git', 'clone', '--no-checkout', entry['url'], str(dest)])
            run(git(dest)+['checkout', entry['commit']])
        revision = subprocess.check_output(git(dest)+['rev-parse', 'HEAD'], text=True).strip()
        if revision != entry['commit']:
            raise RuntimeError(f'{dest}: unexpected revision {revision}; preserve your changes before updating')
    run(git(PORT / 'upstream/SDL_ttf')+['submodule', 'update', '--init', '--depth', '1', 'external/freetype'])
    for name,filename in [('OpenClaw','openclaw-android.patch'),('SDL','sdl-android.patch')]:
        engine = PORT / 'upstream' / name
        patch = PORT / 'patches' / filename
        if run(git(engine)+['apply', '--reverse', '--check', str(patch)], check=False).returncode != 0:
            run(git(engine)+['apply', '--check', str(patch)])
            run(git(engine)+['apply', str(patch)])
    print('Locked dependencies and Android patch are ready.')


if __name__ == '__main__':
    main()
