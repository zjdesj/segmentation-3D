import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path


pcd_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/31-80/uncertain')
name = '31-80_cropx_cropz_cluster_5.pcd'

def proc():
  calf = Farm(name, rotate=False, data_path=pcd_path, mkdir=False)
  calf.show_summary()
  #labels = calf.cluster(min_points=8, min_cluster=3000, eps=0.03)
  #calf.saveClusters_2(labels)
  #calf.visual()
  #return

  #min_y = calf.summary['min_bound'][1] 
  #max_y = calf.summary['max_bound'][1] - 1.7
  max_y = calf.summary['max_bound'][1]
  min_y = max_y - 1.6

  #min_x = calf.summary['min_bound'][0]
  #max_x = calf.summary['max_bound'][0] - 0.3

  cpcd = calf.cropFarm_y(max_y, min_y)
  calf.updatePCD(cpcd)

  #cpcd = calf.crop_x(min_x, max_x)
  #calf.updatePCD(cpcd)

  #calf.show_summary()
  #calf.visual()
  #return 

  #calf.saveCattlePCD('cattle_0', cpcd)
  #return

  labels = calf.cluster(min_points=1, min_cluster=4000, eps=0.03)
  calf.saveClusters_2(labels)

proc()

