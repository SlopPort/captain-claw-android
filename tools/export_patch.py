"""Export and reverse-check the local adaptation against the locked OpenClaw revision."""
from pathlib import Path
import subprocess

port=Path(__file__).resolve().parents[1]
for name,filename in [('OpenClaw','openclaw-android.patch'),('SDL','sdl-android.patch')]:
    engine=port/'upstream'/name
    patch=port/'patches'/filename
    git=['git','-c','safe.directory='+engine.as_posix(),'-C',str(engine)]
    subprocess.run(git+['diff','--binary','--no-ext-diff','--output='+str(patch)],check=True)
    subprocess.run(git+['apply','--reverse','--check',str(patch)],check=True)
    print('Exported and checked',patch.name)
