"""Export and reverse-check the local adaptation against the locked OpenClaw revision."""
from pathlib import Path
import subprocess

port=Path(__file__).resolve().parents[1]
engine=port/'upstream/OpenClaw'
patch=port/'patches/openclaw-android.patch'
git=['git','-c','safe.directory='+engine.as_posix(),'-C',str(engine)]
subprocess.run(git+['diff','--binary','--no-ext-diff','--output='+str(patch)],check=True)
subprocess.run(git+['apply','--reverse','--check',str(patch)],check=True)
print('Exported and checked',patch.name)
