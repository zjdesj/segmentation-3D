import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path


pcd_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/9-51/uncertain')
name = '9-51_cropx_cropz_cluster_6.pcd'

def proc():
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  labels = calf.cluster(min_points=1, min_cluster=3000, eps=0.03)
  calf.saveClusters_2(labels)
  #calf.visual()
  return

  max_y = calf.summary['max_bound'][1] - 0.5
  min_y = calf.summary['min_bound'][1]

  #min_x = calf.summary['min_bound'][0]
  #max_x = min_x + 1.35

  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)

  #cpcd = calf.crop_x(min_x, max_x)
  #calf.updatePCD(cpcd)

  calf.show_summary()
  #calf.visual()
  #return 

  #calf.saveCattlePCD('cattle_0', cpcd)
  #return

  labels = calf.cluster(min_points=1, min_cluster=3000, eps=0.05)
  calf.saveClusters_2(labels)

proc()