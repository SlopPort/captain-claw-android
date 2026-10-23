"""Create a new local release identity once; never print its password.

OpenAI Codex (LLM). Run only for this project's first release identity. Existing
files are never replaced. Back up both outputs privately before distributing a
release. A new key cannot upgrade the existing SDK-debug-signed installations.
"""
from pathlib import Path
import argparse
import os
import secrets
import subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--keytool',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
folder=root/'private-signing'
if folder.exists():raise SystemExit('Signing folder already exists; preserve existing identity and inspect it locally.')
folder.mkdir()
password=folder/'password.txt';key=folder/'pazur-release.keystore'
with password.open('x',encoding='ascii') as out:out.write(secrets.token_hex(32)+'\n')
os.chmod(password,0o600)
try:
 subprocess.run([args.keytool,'-genkeypair','-alias','pazur','-keyalg','RSA','-keysize','3072',
  '-validity','10000','-dname','CN=SlopPort','-storetype','PKCS12','-keystore',str(key),
  '-storepass:file',str(password),'-keypass:file',str(password),'-noprompt'],check=True)
 os.chmod(key,0o600)
except Exception:
 # Retain evidence/partial key rather than silently replacing an identity.
 raise
print('Created private-signing/pazur-release.keystore and password.txt. Back up both privately. Never commit or publish them.')
