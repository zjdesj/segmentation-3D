import subprocess
import os

subprocess.call('python --version', shell=True)
subprocess.call('apt-get install python3.7', shell=True)


# 需要输入
subprocess.call(
    'sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1', shell=True)

subprocess.call('python --version', shell=True)
subprocess.call('sudo apt install python3.7-distutils', shell=True)
