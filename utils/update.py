import os
import subprocess

os.chdir('/content/3d/segmentation-3D')
subprocess.call('git pull', shell=True)
subprocess.call('pip install -r requirements.txt', shell=True)
