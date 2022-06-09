import os
import sys
import subprocess

def createDirectory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        print(directory+"생성 실패")

def install(packageName):
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', packageName])