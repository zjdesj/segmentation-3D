import numpy as np
from basement import Farm
from pathlib import Path


def segmentation(pcd_path, pcd_name, shift=3.5, shift_y=0, min_points=10, min_clusters=2000):
  farm = Farm(pcd_name, rotate=True, data_path=pcd_path)
  # 分析原始数据
  farm.show_summary()
  farm.visual()
  farm.savePCDInfo()

  # 截取x
  cpcd = farm.cropFarm(shift=shift)

  if shift_y > 0:
    farm.updatePCD(cpcd)
    cpcd = farm.cropFarm_y_2(shift_y)

  farm.updatePCD(cpcd)
  farm.show_summary()
  farm.visual()
  save = input('Save cropped farm along x(and y) axis:')
  if save == 'Y':
    farm.savePCD('cropx')
    farm.newSaveDir()
    farm.savePCDInfo()
  else:
    return


  # 根据分析x后的height 去掉地面屋顶
  min_height = float(input('输入最小高度: '))
  max_height = float(input('输入最大高度: '))
  cpcd = farm.removeRoofAndGround(max_threshold=max_height, min_threshold=min_height)
  farm.updatePCD(cpcd)
  farm.show_summary()
  farm.visual()
  save = input('Save cropped farm along z axis:')
  if save == 'Y':
    farm.savePCD('cropz')
    farm.newSaveDir()
    farm.savePCDInfo()
  else:
    return

  eps = float(input('输入邻域: '))
  points = int(input('输入最小点数: '))
  cluster_points = int(input('输入点云最小包含点数: '))

  labels = farm.cluster(min_points=points, min_cluster=cluster_points, eps=eps)
  farm.saveClusters(labels, standing_height=(min_height + 0.25), foot_height=min_height)


def test_segment(pcd_path, eps, points, cluster_points, save):
  dir = Path(pcd_path).parent
  farm = Farm(Path(pcd_path).name, rotate=False, data_path=dir)
  #farm.visual()
  labels = farm.cluster(min_points=points, min_cluster=cluster_points, eps=eps)
  farm.showClusters(labels, save=save)
#def segment(pcd_path, labels):

def getNumbers(pcd_path, ground_height):
  dir = Path(pcd_path).parent
  name = Path(pcd_path).name
  farm = Farm(Path(pcd_path).name, rotate=False, data_path=dir)
  
  min_height = ground_height + 0.7
  max_height = ground_height + 1.3

  cpcd = farm.removeRoofAndGround(max_threshold=max_height, min_threshold=min_height)
  farm.updatePCD(cpcd)
  farm.show_summary()
  farm.visual()

def dbscan(pcd_path, min_height, eps, points, cluster_points):
  dir = Path(pcd_path).parent
  farm = Farm(Path(pcd_path).name, rotate=False, data_path=dir, mkdir=False)
  labels = farm.cluster(min_points=points, min_cluster=cluster_points, eps=eps)
  farm.saveClusters(labels, standing_height=(min_height + 0.25), foot_height=min_height)


  