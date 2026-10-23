"""Identify the installed APK instead of a mutable local build output. Codex."""
import hashlib
import re
import subprocess
from gamepad_quit_smoke import adb


def installed_apk_sha256(package='pl.pazur.port'):
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+',package):raise ValueError('Invalid package identity')
    base=next(line.removeprefix('package:') for line in adb('shell','pm','path',package).splitlines() if line.endswith('/base.apk'))
    digest=hashlib.sha256()
    with subprocess.Popen(['adb','exec-out','cat',base],stdout=subprocess.PIPE) as process:
        while block:=process.stdout.read(1024*1024):digest.update(block)
        if process.wait()!=0:raise RuntimeError('Cannot hash installed package')
    return digest.hexdigest()
