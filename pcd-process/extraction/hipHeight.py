import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
import numpy as np
from queryMeasurement import updateHH
#from denoise_batch import reDenoise

import re

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/hipheight'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  calf.show_summary()
  #calf.visual()
  return calf

def getHH(name):
  calf = getPCD(name)
  HH = calf.summary['max_bound'][2]
  print(f'Hip height: {HH}')

  return HH

def setWidth(name, HH):
  stem = re.sub(r'_re_pure_.*_bbInCattle_HH.pcd', '', name)

  updateHH(stem, HH)

def batchHH(patten):
  HH_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/hipheight'
  cattle_dir = Path(HH_path)
  files = cattle_dir.glob(patten)

  for calfFile in files:
    name = Path(calfFile).name
    print('calf file name:', calfFile, name)

    # 设置去噪后宽度
    HH = getHH(name)
    setWidth(name, HH)

if __name__ == '__main__':
  
  patten = '*bbInCattle_HH.pcd'
  batchHH(patten)

  
