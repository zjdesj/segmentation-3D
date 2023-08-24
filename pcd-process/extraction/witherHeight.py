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

def getEnds(joint, pts):
  minLeft = joint[0] - 0.4
  maxRight =  joint[0] + 0.8
  #print('len', len(pts))
  tmp = pts[pts[:, 0] > minLeft]
  torso = tmp[tmp[:, 0] < maxRight]
  #print('ffff', len(torso))
  #print(torso[:10,:])
  return torso[0], torso[-1]

def getBE(pts):
  torso = pts
  return torso[0], torso[-1]

def getLeftPeek(joint, pts):
  leftPts = pts[pts[:, 0] < joint[0]]
  # 左半部分 划出掉尾巴可能性
  minLeft = joint[0] - 0.4
  partLeftPts = leftPts[leftPts[:, 0 ] > minLeft]
  print(len(leftPts), len(partLeftPts))
  
  sortedPartLeftX = partLeftPts[np.argsort(partLeftPts[:, 0])]

  gap = (len(leftPts) - len(partLeftPts) > 10)

  sortedPartLeft = partLeftPts[np.argsort(partLeftPts[:, 2])]
  return np.max(partLeftPts[:, 2]), gap, sortedPartLeft[-1], sortedPartLeftX[0]

def getRightPeek(joint, pts, shift=0.6):
  minRight = joint[0] + shift
  rightPts = pts[pts[:, 0] > minRight]
  # 右半部分 去头
  maxRight =  joint[0] + 0.8
  partRightPts = rightPts[rightPts[:, 0 ] < maxRight]
  print(len(rightPts), len(partRightPts))

  sortedPartRight = partRightPts[np.argsort(partRightPts[:, 2])]
  peek = np.max(partRightPts[:, 2])

  gap = pts[pts[:,2] == peek][0][0] - minRight
  return peek, gap, sortedPartRight[-1]

def getBackheight(joint, pts):
  rightPts = pts[pts[:, 0] > joint[0]]

  maxRight =  joint[0] + 0.5
  partRightPts = rightPts[rightPts[:, 0 ] < maxRight]

  sortedPartRight = partRightPts[np.argsort(partRightPts[:, 2])]
  valley = np.min(partRightPts[:, 2])

  return valley, sortedPartRight[0]

def getStem(name):
  stem = re.sub(r'_re_pure_.*', '', name)
  return stem

def setWaistH(name, value, gap, lxyz):
  stem = getStem(name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'waist height')
  updateColumn(stem, value - groundH, 'waist H')
  updateColumn(stem, gap, 'waistgap')
  updateColumn(stem, lxyz, 'LA')

def setWithersH(name, value, gap, rxyz, key):
  stem = getStem(name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'withers height')
  updateColumn(stem, value - groundH, 'withers H')
  updateColumn(stem, gap, 'withersgap')
  updateColumn(stem, rxyz, key)

def setBackH(name, value, bxyz):
  stem = getStem(name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'back height')
  updateColumn(stem, value - groundH, 'back H')
  updateColumn(stem, bxyz, 'LD')

def setEnds(name, s, e):
  stem = getStem(name)
  updateColumn(stem, s, 'LT1')
  updateColumn(stem, e, 'LM1')

def setBE(name, s, e):
  stem = getStem(name)
  updateColumn(stem, s, 'LT2')
  updateColumn(stem, e, 'LM2')

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
    #leftH, lgap, lxyz = getLeftPeek(joint, pts)
    #setWaistH(name, leftH, lgap, lxyz)
    #rightH1, rgap1, rxyz1 = getRightPeek(joint, pts, shift=0.55)
    #rightH2, rgap2, rxyz2 = getRightPeek(joint, pts, shift=0.6)
    #setWithersH(name, rightH1, rgap1, rxyz1, 'LB1')
    #setWithersH(name, rightH2, rgap2, rxyz2, 'LB2')
    #backH, bxyz = getBackheight(joint, pts)
    #setBackH(name, backH, bxyz)
    #leftxyz, rightxyz = getEnds(joint, pts)
    #setEnds(name, leftxyz, rightxyz)
    leftBxyz, rightBxyz = getBE(pts)
    setBE(name, leftBxyz, rightBxyz)
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
  #patten = '8-1_9-58_3_re_pure_2_bb.pcd'
  batchWaistH(patten)