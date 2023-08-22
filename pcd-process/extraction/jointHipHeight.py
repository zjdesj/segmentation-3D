import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
import pandas as pd
import numpy as np
from queryMeasurement import updateColumn, queryGround

import re

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/hipheight'
  #root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/f-feature'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  calf.show_summary()

  #calf.visual()
  return calf

def getJoint(name):
  calf = getPCD(name)
  colors = np.asarray(calf.pcd.colors)

  # 一级筛选
  inds = colors[:, 0] == 1
  colorsP = colors[inds]
  pts = calf.getPoints()
  bs = pts[inds]
  #print(f'point count of bs: {len(bs)}')

  # 二级筛选
  inds2 = colorsP[:, 1] == 0
  bss = bs[inds2]
  print(f'point count of bss: {len(bss)}')

  sortedBsInd = np.argsort(bss[:, 0])
  sortedBs = bss[sortedBsInd]

  return sortedBs[0], len(bss)

def setJointHH(name, HH, count):
  stem = re.sub(r'_re_pure_.*_bbInCattle_HH.pcd', '', name)
  groundH = queryGround(stem)

  #updateColumn(stem, HH, 'joint Hip H')
  #updateColumn(stem, HH - groundH, 'joint HH')

  updateColumn(stem, HH, 'JHH')
  updateColumn(stem, HH - groundH, 'JHHG')
  updateColumn(stem, count, 'BSize')
def recordJoint(name,value):
  stem = re.sub(r'_re_pure_.*_bbInCattle_HH.pcd', '', name)
  updateColumn(stem, value, 'joint')

def batchJointHH(patten):
  HH_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/hipheight'
  cattle_dir = Path(HH_path)
  files = cattle_dir.glob(patten)

  for calfFile in files:
    name = Path(calfFile).name
    print('calf file name:', calfFile, name)

    joint, count = getJoint(name)
    setJointHH(name, joint[2], count)
    recordJoint(name, joint)

if __name__ == '__main__':
  
  #patten = '8-1_9-58_3_re_pure_2_bbInCattle_HH.pcd'
  #joint = getJoint(patten)
  #print(joint)

  patten = '*bbInCattle_HH.pcd'
  batchJointHH(patten)

  #patten = 'n10-5_31-84_10_0*'
  #batchJointHH(patten)
