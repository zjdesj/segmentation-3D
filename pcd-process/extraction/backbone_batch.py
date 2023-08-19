import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
from backbone import backbone, top_points
import numpy as np
from queryMeasurement import queryDBSCAN
from denoise_batch import reDenoise

import seaborn as sns
import matplotlib.pyplot as plt
import re

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  calf.show_summary()
  #calf.visual()
  return calf


def sc(a, b):
  plt.scatter(a, b, color='blue', marker='.' )
  plt.gcf().set_size_inches(19, 7)
  plt.gca().set_aspect('equal', adjustable='box')
  plt.show()

def castPointToXY(calf, show=False):
  points = calf.getPoints()

  xyPoints = points[:, [0,1]]

  if show:
    x = points[:, 0].T
    y = points[:, 1].T
    sc(x, y)

  return xyPoints

def castPointToYZ(calf, show=False):
  points = calf.getPoints()

  yzPoints = points[:, [1,2]]

  if show:
    y = points[:, 1].T
    z = points[:, 2].T
    sc(y, z)

  return yzPoints

def castPointToXZ(calf, show=False):
  points = calf.getPoints()

  xzPoints = points[:, [0,2]]

  if show:
    x = points[:, 0].T
    z = points[:, 2].T
    sc(x, z)

  return xzPoints

def backboneXY(name):

  calf = getPCD(name)
  calf.show_summary()
  calf.visual()

  tpcd = backbone(calf)
  #data = backbone_xy(calf, name)

  calf.updatePCD(tpcd)
  calf.show_summary()
  calf.visual()

def backboneXY(cattle):
  [tops, a, b] = top_points(cattle)

  return tops[:, [0,1]]
  #return a[:, [0,1]]
  #return b[:, [0,1]]

def backboneOnXYPlane(cattle):
  bxy = backboneXY(cattle).T.tolist()
  cxy = castPointToXY(cattle).T.tolist()

  plt.scatter(cxy[0], cxy[1], color='blue', label='Cattle', marker='.')
  plt.scatter(bxy[0], bxy[1], color='green', label='Backbone', marker='.')

  plt.xlabel('x')
  plt.ylabel('y')
  plt.title('backbone on cattle')

  plt.gca().set_aspect('equal', adjustable='box')
  plt.gcf().set_size_inches(19, 7)

  plt.legend()
  plt.show()

def display_inlier_outlier(cloud, ind):
  inlier_cloud = cloud.select_by_index(ind)
  outlier_cloud = cloud.select_by_index(ind, invert=True)

  print("Showing outliers (red) and inliers (gray): ")
  inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
  outlier_cloud.paint_uniform_color([1, 0, 0])
  o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


def filter(cattle):
  calf, ind = cattle.pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=0.01)
  #return calf
  #display_inlier_outlier(cattle.pcd, ind)
  #cpcd = cattle.pcd.select_by_index(ind, invert=True)

  name = cattle.name
  stem = re.sub(r'_re_pure.*', '', Path(name).stem)
  ret = queryDBSCAN(stem)
  print(f'pure cattle DBSCAN: {ret}')

  cattle.updatePCD(calf)
  cattle = reDenoise(cattle, ret)
  return cattle
  

def mergePCD(a, b):
  return a + b

def getBackbonePCD(calf):

  bb_pcd = backbone(calf)

  return bb_pcd 

def getBackBoneInd(backbonePCD, calf):
  bbpt = np.asarray(backbonePCD.points)

  pts = calf.getPoints()

  ret = []
  for pt in bbpt:
    ind = np.where(np.all(pts == pt, axis=1))[0][0]
    ret.append(ind)
  
  return ret

def backboneInCalf(ind, calf):
  bb_cloud = calf.pcd.select_by_index(ind)

  #bbpt = np.asarray(bb_cloud.points)
  #bbpt[:,2] = bbpt[:, 2] + 0.01

  other_cloud = calf.pcd.select_by_index(ind, invert=True)
  
  bb_cloud.paint_uniform_color([1, 0, 0])

  calf.updatePCD(bb_cloud + other_cloud)

  return calf

def processBackbone(name):
  cattle = getPCD(name)
  calf = filter(cattle)

  calf.savePCDG('filter', calf.pcd, feature_path)

  bb = getBackbonePCD(calf)
  calf.savePCDG('bb', bb, feature_path)

  bb_ind = getBackBoneInd(bb, calf)
  bbInCalf = backboneInCalf(bb_ind, calf)

  calf.savePCDG('bbInCalf', bbInCalf.pcd, feature_path)


  ocalf = getPCD(name)
  bb_ind = getBackBoneInd(bb, ocalf)
  bbInCatttle = backboneInCalf(bb_ind, ocalf)
  calf.savePCDG('bbInCattle', bbInCatttle.pcd, feature_path)

def batch_processBackbone(patten):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  cattle_dir = Path(root_path)
  file = cattle_dir.glob(patten)
  for calf in file:
    print('calf file name:', calf)
    processBackbone(calf)


if __name__ == '__main__':
  feature_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'

  #batch_processBackbone('50-1_*_re_pure_*.pcd')
  #batch_processBackbone('50-2_*_re_pure_*.pcd')
  #batch_processBackbone('50-3_*_re_pure_*.pcd')
  #batch_processBackbone('50-5_*_re_pure_*.pcd')
  #batch_processBackbone('50-7_*_re_pure_*.pcd')
  #batch_processBackbone('50-9_*_re_pure_*.pcd')

  #batch_processBackbone('30-1_*_re_pure_*.pcd')
  #batch_processBackbone('30-2_*_re_pure_*.pcd')
  #batch_processBackbone('30-3_*_re_pure_*.pcd')
  #batch_processBackbone('30-5_*_re_pure_*.pcd')
  #batch_processBackbone('30-7_*_re_pure_*.pcd')
  #batch_processBackbone('30-9_*_re_pure_*.pcd')

  #batch_processBackbone('15-1_*_re_pure_*.pcd')
  #batch_processBackbone('15-2_*_re_pure_*.pcd')
  #batch_processBackbone('15-3_*_re_pure_*.pcd')
  #batch_processBackbone('15-5_*_re_pure_*.pcd')
  #batch_processBackbone('15-7_*_re_pure_*.pcd')
  #batch_processBackbone('15-9_*_re_pure_*.pcd')

  #batch_processBackbone('10-1_*_re_pure_*.pcd')
  #batch_processBackbone('10-2_*_re_pure_*.pcd')
  #batch_processBackbone('10-3_*_re_pure_*.pcd')
  #batch_processBackbone('10-5_*_re_pure_*.pcd')
  #batch_processBackbone('10-7_*_re_pure_*.pcd')
  #batch_processBackbone('10-9_*_re_pure_*.pcd')

  #batch_processBackbone('8-1_*_re_pure_*.pcd')
  #batch_processBackbone('8-2_*_re_pure_*.pcd')
  #batch_processBackbone('8-3_*_re_pure_*.pcd')
  #batch_processBackbone('8-5_*_re_pure_*.pcd')
  #batch_processBackbone('8-7_*_re_pure_*.pcd')
  #batch_processBackbone('8-9_*_re_pure_*.pcd')

  #batch_processBackbone('n8-3_*_re_pure_*.pcd')
  #batch_processBackbone('n8-5_*_re_pure_*.pcd')
  #batch_processBackbone('n10-3_*_re_pure_*.pcd')
  #batch_processBackbone('n10-5_*_re_pure_*.pcd')
  #batch_processBackbone('n15-3_*_re_pure_*.pcd')
  #batch_processBackbone('n15-5_*_re_pure_*.pcd')
  

  name = 'n15-5_31-82_5_re_pure_0.pcd'
  processBackbone(name)



  #pts = calf.getPoints()
  #z = pts[:, 2]
  #pts[:, 2] = 0

  #calf.savePCDG('pp', calf.pcd, feature_path)

  #backboneOnXYPlane(calf)
  #calf = calf.crop_z()
  #castPointToXY(calf, show=True)
  #castPointToXZ(calf, show=True)
  #test()
  #backboneOnXYPlane(calf)