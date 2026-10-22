"""Compile the production journal class and run isolated JVM boundary checks."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

port=Path(__file__).resolve().parents[1]
jdk=Path(os.environ.get('JAVA_HOME','C:/Program Files/Android/Android Studio/jbr'))/'bin'
javac=str(jdk/('javac.exe' if os.name=='nt' else 'javac'))
java=str(jdk/('java.exe' if os.name=='nt' else 'java'))
if not Path(javac).is_file():javac=shutil.which('javac') or javac
if not Path(java).is_file():java=shutil.which('java') or java
with tempfile.TemporaryDirectory(prefix='pazur-import-classes-') as output:
    subprocess.run([javac,'-d',output,str(port/'app/src/main/java/pl/pazur/port/ImportTransaction.java'),
                    str(port/'tools/java/pl/pazur/port/ImportTransactionChecks.java')],check=True)
    subprocess.run([java,'-cp',output,'pl.pazur.port.ImportTransactionChecks'],check=True)
