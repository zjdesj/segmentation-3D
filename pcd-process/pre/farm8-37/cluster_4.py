import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path


pcd_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/8-37/uncertain')
name = '8-37_cropx_cropz_cluster_4.pcd'

def proc():
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  #calf.visual()
  #return

  max_y = calf.summary['max_bound'][1] - 0.22
  min_y = calf.summary['min_bound'][1]

  #max_x = calf.summary['max_bound'][0] - 0.3
  #min_x = calf.summary['min_bound'][0]

  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)

  #cpcd = calf.crop_x(min_x, max_x)
  #calf.updatePCD(cpcd)

  calf.show_summary()
  #calf.visual()
  #return 

  #calf.saveCattlePCD('cattle_0', cpcd)
  #return

  labels = calf.cluster(min_points=1, min_cluster=400, eps=0.06)
  calf.saveClusters_2(labels)

proc()