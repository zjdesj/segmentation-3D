import os
import subprocess

os.chdir('/content/3d/segmentation-3D')
subprocess.call('git pull', shell=True)
