import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
import numpy as np
from queryMeasurement import updateColumn, queryGround, queryColumn

import re

def getSpinePoints(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  pts = calf.getPoints()
  print(f'pts: {len(pts)}')

  sortedInd = np.argsort(pts[:, 0])

  return pts[sortedInd]

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/hipheight'
  #root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/f-feature'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  calf.show_summary()

  #calf.visual()
  return calf

def getJoint(name):
  #stem = re.sub(r'_re_pure_.*_bbInCattle_HH.pcd', '', name)
  stem = re.sub(r'_re_pure_.*', '', name)
  joint = queryColumn(stem, 'joint')
  if joint != joint:
    return None

  cleaned_data = joint.strip('[]').split()
  float_data = [float(value) for value in cleaned_data]
  joint = np.array(float_data)

  return joint

def getLeftPeek(joint, pts):
  leftPts = pts[pts[:, 0] < joint[0]]
  # 左半部分 划出掉尾巴可能性
  minLeft = joint[0] - 0.4
  partLeftPts = leftPts[leftPts[:, 0 ] > minLeft]
  print(len(leftPts), len(partLeftPts))

  gap = (len(leftPts) - len(partLeftPts) > 10)
  return np.max(partLeftPts[:, 2]), gap

def getRightPeek(joint, pts):
  rightPts = pts[pts[:, 0] > (joint[0] + 0.6)]
  # 右半部分 去头
  maxRight =  joint[0] + 0.8
  partRightPts = rightPts[rightPts[:, 0 ] < maxRight]
  print(len(rightPts), len(partRightPts))

  peek = np.max(partRightPts[:, 2])

  gap = peek[0] - (joint[0] + 0.6)
  return peek, gap

def setWaistH(name, value, gap):
  stem = re.sub(r'_re_pure_.*', '', name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'waist height')
  updateColumn(stem, value - groundH, 'waist H')
  updateColumn(stem, gap, 'waistgap')

def setWithersH(name, value, gap):
  stem = re.sub(r'_re_pure_.*', '', name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'withers height')
  updateColumn(stem, value - groundH, 'withers H')
  updateColumn(stem, gap, 'withersgap')

def batchWaistH(patten):
  HH_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'
  cattle_dir = Path(HH_path)
  files = cattle_dir.glob(patten)

  for calfFile in files:
    name = Path(calfFile).name
    print('calf file name:', calfFile, name)

    pts = getSpinePoints(name)
    joint = getJoint(name)
    if joint is None:
      continue
    # 设置去噪后宽度
    leftH, lgap = getLeftPeek(joint, pts)
    setWaistH(name, leftH, lgap)
    rightH, rgap = getRightPeek(joint, pts)
    setWithersH(name, rightH, rgap)
    #rightH = getRightPeek(joint, pts)
if __name__ == '__main__':
  
  #patten = '8-1_9-58_3_re_pure_2_bbInCattle_HH.pcd'
  #joint = getJoint(patten)
  #print(joint)
  ##patten = '*bbInCattle_HH.pcd'
  ##batchJointHH(patten)

  #patten = 'n10-5_31-84_10_0*'
  #batchJointHH(patten)

  #getJoint('8-1_9-58_0_0_re_pure_0_bb.pcd')


  #patten = '30-1_9-73_11_0_re_pure_0_bb.pcd'
  patten = '*_bb.pcd'
  batchWaistH(patten)