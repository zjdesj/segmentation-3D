import open3d as o3d
import sys
import numpy as np
sys.path.append('..')
from farm import Farm
from individuals import process
from pathlib import Path


def crop_x(cattle, min, step=0.01):
  min_bound = cattle.summary["min_bound"]
  max_bound = cattle.summary["max_bound"]

  max = min + step

  min_bound[0] = min
  max_bound[0] = max 

  box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

  cpcd = cattle.pcd.crop(box)
  return cpcd

def crop_z_range(cattle, min_z, max_z):
    min_bound = cattle.summary["min_bound"]
    max_bound = cattle.summary["max_bound"]

    min = min_bound[2] + min_z 
    max = min_bound[2] + max_z

    return cattle.removeRoofAndGround(max_threshold=max, min_threshold=min)

# slice by slice
def getCalves(cattle_path, name):
  # 截取去除地面的部分
  cattle = Farm(name, rotate=False, data_path=cattle_path, mkdir=False)
  #cattle.visual()
  cpcd = crop_z_range(cattle, 0.1, 0.25)
  cattle.show_summary()
  cattle.updatePCD(cpcd)
  cattle.show_summary()
  cpcd, ind = cattle.pcd.remove_radius_outlier(nb_points=7, radius=0.05)
  cattle.updatePCD(cpcd)
  cattle.show_summary()
  cattle.visual()
  cattle.savePCDInfo()

  
stem = '9-62'
root_path = '/Users/wyw/Documents/Chaper2/github-code/data'
name = '9-62_cropx_cropz_cluster_5_segment.pcd'
cattle_path = Path(root_path, 'cattle', stem)

#tpcd = backbone(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')
tpcd = getCalves(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')
