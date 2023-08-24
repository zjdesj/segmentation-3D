
import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
import numpy as np
from queryMeasurement import updateColumn, queryGround, queryZ

import re

def getSpinePoints(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  pts = calf.getPoints()
  print(f'backbone pts size: {len(pts)}')

  sortedInd = np.argsort(pts[:, 2])
  return pts[sortedInd]

def queryValues(name):
  stem = re.sub(r'_re_pure_.*', '', name)
  zs = queryZ(stem)
  print('zs', zs)
  [LA_z, LD1_z, LD2_z, LB1_z, LB2_z] = zs
  pts = getSpinePoints(name)

  z =  pts[:, 2]
  print('LA_z', LA_z, type(LA_z), LD2_z)
  inds = np.where(z == LD2_z)
  
  #inds =  [i for i, e in enumerate() if e in zs]
  print(f'inds: {inds}')

  return pts[inds, :]

if __name__ == '__main__':
  patten = '*_bb.pcd'
  ret = queryValues('8-1_9-58_3_re_pure_2_bb.pcd')
  #ret = queryValues('8-1_9-58_3')
  print('ret:', ret)