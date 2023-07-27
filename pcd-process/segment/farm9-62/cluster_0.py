import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path


pcd_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/9-62/uncertain')
name = '9-62_cropx_cropz_cluster_0.pcd'

# 处理出联合的干净牛
def proc():
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  #calf.visual()

  min_y = calf.summary['min_bound'][1] + 1.5
  max_y = calf.summary['max_bound'][1] - 2.5

  max_x = calf.summary['max_bound'][0] - 1.83
  min_x = max_x - 2.0

  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)

  cpcd = calf.crop_x(min_x, max_x)
  calf.updatePCD(cpcd)

  calf.show_summary()
  #calf.visual()

  labels = calf.cluster(min_points=1, min_cluster=6000, eps=0.03)
  calf.saveClusters_2(labels)

def proc2(name):
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  #calf.visual()

  R1 = calf.pcd.get_rotation_matrix_from_xyz((0, 0, -np.pi/7.6))
  calf.pcd.rotate(R1)
  #calf.visual()

  min_y = calf.summary['min_bound'][1]
  max_y = calf.summary['max_bound'][1]
  min_y = min_y + 0.685
  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)
  #calf.visual()
  calf.saveCattlePCD('cattle_0', cpcd)


  #min_y = calf.summary['min_bound'][1]
  #max_y = min_y + 0.685
  #cpcd = calf.cropFarm_y(max_y, min_y)
  #calf.updatePCD(cpcd)
  #calf.saveCattlePCD('cattle_1', cpcd)

#proc()

name = '9-62_cropx_cropz_cluster_0_cattle_0.pcd'
proc2(name)