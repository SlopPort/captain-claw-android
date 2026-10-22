"""Identify the installed APK instead of a mutable local build output. Codex."""
import hashlib
import subprocess
from gamepad_quit_smoke import adb


def installed_apk_sha256():
    base=next(line.removeprefix('package:') for line in adb('shell','pm','path','pl.pazur.port').splitlines() if line.endswith('/base.apk'))
    digest=hashlib.sha256()
    with subprocess.Popen(['adb','exec-out','cat',base],stdout=subprocess.PIPE) as process:
        while block:=process.stdout.read(1024*1024):digest.update(block)
        if process.wait()!=0:raise RuntimeError('Cannot hash installed package')
    return digest.hexdigest()
