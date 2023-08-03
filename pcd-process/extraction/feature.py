import open3d as o3d
import sys
sys.path.append('..')
from farm import Farm
from pathlib import Path
from backbone import backbone, backbone_xy, getAngle
import numpy as np
import pandas as pd
from queryDirection import queryDirection

#root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/entity'
root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/above'


def display_inlier_outlier(cloud, ind):
  inlier_cloud = cloud.select_by_index(ind)
  outlier_cloud = cloud.select_by_index(ind, invert=True)

  print("Showing outliers (red) and inliers (gray): ")
  outlier_cloud.paint_uniform_color([1, 0, 0])
  inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
  o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

def getPCD(name):
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)
  #calf.show_summary()
  #calf.visual()
  #calf.savePCDInfo()

  # remove height over 1.35m
  if calf.summary["max_bound"][2] - calf.summary["min_bound"][2] > 1.35:
    cpcd = calf.crop_z(0)
    calf.updatePCD(cpcd)

  calf.show_summary()
  return calf

def getArc(calf, direction):
  data = backbone_xy(calf, root_path, name)
  arc = getAngle(data, direction)
  print(f'arc: {arc}')

  return arc


def rotate(name, direction):
  #name = '8-1_9-58_6.pcd'  #0
  #name = '8-9_8-31_11.pcd' #3

  #name = '8-1_9-58_8_0.pcd' #5
  #name = '50-5_9-68_2.pcd' #6
  #name = '8-1_9-58_3.pcd' #2
  #name = '8-2_9-59_1.pcd' #2
  #name = '8-3_9-60_3.pcd' #2
  #name = '10-5_9-57_1.pcd' #1
  #direction = queryDirection(name)

  cattle = getPCD(name)
  arc = getArc(cattle, direction)
  #cattle.visual()

  #print(f'dirction: {direction}')
  if direction == '0':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, 2 * np.pi - arc))
  elif direction == '3':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, -arc))
  elif direction == '5':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, - np.pi/2))
  elif direction == '6':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi/2))
  elif direction == '1':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi + abs(arc)))
  elif direction == '2':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi - abs(arc)))

 
  #R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, 0.75 * np.pi ))
  cattle.pcd = cattle.pcd.rotate(R1)
  #cattle.visual()
  return cattle




#getCategory('0')

if __name__ == '__main__':
  rotate('8-7_8-33_4_above.pcd', '0')