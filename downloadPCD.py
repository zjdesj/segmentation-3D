import subprocess
import os

__PCD__ = "https://filetransfer.io/data-package/aXA3Sv6d/download"
subprocess.call('wget ' + __PCD__ + ' -O /content/1.zip', shell=True)

subprocess.call('mkdir /content/pcd', shell=True)
subprocess.call('unzip /content/1.zip -d /content/pcd', shell=True)
subprocess.call('rm /content/1.zip', shell=True)
