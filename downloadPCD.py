import subprocess
import os

__PCD__ = "https://filetransfer.io/data-package/aXA3Sv6d/download"
subprocess.call('wget ' + __PCD__ + ' -O /content/1.zip')

subprocess.call('mkdir /content/pcd')
subprocess.call('unzip /content/1.zip -d /content/pcd')
