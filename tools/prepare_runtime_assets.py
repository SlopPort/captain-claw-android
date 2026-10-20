"""Prepare redistributable runtime assets from the pinned source dependencies."""
from pathlib import Path
import subprocess
import sys

tools=Path(__file__).resolve().parent
for name in ('prepare_music_bank.py','prepare_controller_db.py'):
    subprocess.run([sys.executable,str(tools/name)],check=True)
