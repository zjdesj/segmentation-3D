import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path


pcd_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/8-33/uncertain')
name = '8-33_cropx_cropz_cluster_8.pcd'

def proc():
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  #calf.visual()
  #return

  min_y = calf.summary['min_bound'][1]
  max_y = min_y + 0.95

  max_x = calf.summary['max_bound'][0] - 0.3
  min_x = calf.summary['min_bound'][0]

  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)

  cpcd = calf.crop_x(min_x, max_x)
  calf.updatePCD(cpcd)

  calf.show_summary()
  #calf.visual()

  calf.saveCattlePCD('cattle_0', cpcd)
  return

  labels = calf.cluster(min_points=1, min_cluster=6000, eps=0.03)
  calf.saveClusters_2(labels)

proc()