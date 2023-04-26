import subprocess
import os

__PCD__ = "https://filetransfer.io/data-package/aXA3Sv6d/download"
subprocess.call('wget ' + __PCD__ + ' -O /content/1.zip', shell=True)

subprocess.call('mkdir /content/pcd', shell=True)
subprocess.call('unzip /content/1.zip -d /content/pcd', shell=True)
subprocess.call('rm /content/1.zip', shell=True)

__LAS__ = "https://filetransfer.io/data-package/qVimfcn2/download"
subprocess.call('wget ' + __LAS__ + ' -O /content/2.zip', shell=True)

subprocess.call('mkdir /content/las', shell=True)
subprocess.call('unzip /content/2.zip -d /content/las', shell=True)
subprocess.call('rm /content/2.zip', shell=True)
