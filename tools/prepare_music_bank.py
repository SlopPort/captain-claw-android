"""Package the locked FreePats patches as SDL-readable Android assets."""
from pathlib import Path
import json
import shutil

PORT = Path(__file__).resolve().parents[1]
(PORT / 'reports').mkdir(parents=True, exist_ok=True)
source = PORT / 'upstream/freepats'
target = PORT / 'app/src/main/assets/music'
target.mkdir(parents=True, exist_ok=True)
for folder in ('Tone_000', 'Drum_000'):
    dest = target / folder
    dest.mkdir(exist_ok=True)
    for patch in (source / folder).glob('*.pat'):
        if not (dest / patch.name).exists():
            shutil.copyfile(patch, dest / patch.name)
config = 'dir music\n' + (source / 'freepats.cfg').read_text()
# This historic FreePats set is incomplete. Approximate absent GM programs
# with an available instrument in the same family, without extra samples.
tones = {}
bank = None
for line in config.splitlines():
    words = line.split()
    if not words: continue
    if words[0] in ('bank', 'drumset'):
        bank = words[0]
    elif bank == 'bank' and words[0].isdigit() and len(words) > 1:
        tones[int(words[0])] = words[1]
aliases = {}
config += '\n# Android port: approximate missing GM programs using FreePats families.\nbank 0\n'
for program in range(128):
    if program in tones: continue
    family = [p for p in tones if p // 8 == program // 8]
    replacement = min(family or list(tones), key=lambda p: abs(program-p))
    config += f'{program} {tones[replacement]}\n'
    aliases[program] = {'replacement_program': replacement, 'sample': tones[replacement]}
(target / 'freepats.cfg').write_text(config, encoding='utf-8')
(PORT / 'reports/music-instrument-aliases.json').write_text(json.dumps(aliases, indent=2), encoding='utf-8')
licenses = PORT / 'app/src/main/assets/licenses'
licenses.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source / 'LICENSE', licenses / 'FreePats-GPL.txt')
shutil.copyfile(source / 'README_FREEPATS.txt', licenses / 'FreePats-notice.txt')
shutil.copyfile(PORT / 'upstream/SDL_mixer/src/codecs/timidity/COPYING', licenses / 'TiMidity-Artistic.txt')
print('FreePats music bank ready')
