import open3d as o3d
import sys
import numpy as np
sys.path.append('..')
from farm import Farm
from pathlib import Path
from sklearn.linear_model import LinearRegression
import math
import matplotlib.pyplot as plt


def crop_x(cattle, min, step=0.01):
  min_bound = cattle.summary["min_bound"]
  max_bound = cattle.summary["max_bound"]

  max = min + step

  min_bound[0] = min
  max_bound[0] = max 

  box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

  cpcd = cattle.pcd.crop(box)
  return cpcd

# slice by slice
def top_points(cattle):
  # 截取去除地面的部分
  #cpcd = cattle.crop_z(0.2)
  #cattle.updatePCD(cpcd)
  cattle.show_summary()

  x = np.arange(cattle.summary['min_bound'][0], cattle.summary['max_bound'][0], 0.01)

  print(f'x.length: {len(x)}')
  points = cattle.getPoints() 

  # 取最大
  tops = None 
  # 取前3平均值
  tops1 = None
  # 取二大
  tops2 = None
  for cur in x:
    slice = crop_x(cattle, cur)
    sp = cattle.getPoints(slice)
    
    #print(f'sp.leng: {len(sp)}')
    z = sp[:, 2] 

    if not len(sp):
      continue
    
    ind = np.where(z == np.max(z))
    max = sp[ind]
    if not type(tops) is np.ndarray:
      tops = np.array(max)
      tops1 = np.array(max)
      tops2 = np.array(max)
    else:
      tops = np.r_[tops, max]
      tops1 = np.r_[tops, max]
      tops2 = np.r_[tops, max]

    if len(sp) > 20:
      ind = np.argpartition(z, -3)[-3:]
      ps = sp[ind]
      
      mu = np.mean(ps, axis = 0)

      zs = np.median(z[ind])
      median = sp[np.where(z == zs)]

      if not type(tops) is np.ndarray:
        tops1 = np.array([mu])
        tops2 = np.array([median])
      else:
        tops1 = np.r_[tops, [mu]]
        tops2 = np.array([median])

  return [tops, tops1, tops2]

def backbones(cattle):
  [tops, tops1, tops2] = top_points(cattle)
  print(len(tops), len(tops1), len(tops2))

  cc = np.tile([0,1,0], (tops.shape[0], 1))
  cc1 = np.tile([1,0,0], (tops1.shape[0], 1))
  cc2 = np.tile([0,0,1], (tops2.shape[0], 1))

  #tops[:,1] = 0
  tops1[:, 1] = 0.5 + tops1[:, 1]
  tops2[:, 1] = 1 + tops2[:, 1]

  cs = np.r_[cc, cc1, cc2]
  ps = np.r_[tops, tops1, tops2]

  tpcd = o3d.geometry.PointCloud()
  #tp = np.concatenate((points, tops), axis=0)
  #tc = np.concatenate((np.asarray(cattle.pcd.colors), cc), axis=0)

  tpcd.points = o3d.utility.Vector3dVector(ps)
  tpcd.colors = o3d.utility.Vector3dVector(cs)

  return tpcd

def backbone(cattle):
  [tops, a, b] = top_points(cattle)
  print(len(tops))

  cc = np.tile([1,0,0], (tops.shape[0], 1))

  #tops[:,1] = 0

  tpcd = o3d.geometry.PointCloud()
  #tp = np.concatenate((points, tops), axis=0)
  #tc = np.concatenate((np.asarray(cattle.pcd.colors), cc), axis=0)

  tpcd.points = o3d.utility.Vector3dVector(tops)
  tpcd.colors = o3d.utility.Vector3dVector(cc)

  return tpcd

def backbone_xy(cattle, cattle_path, name):
  stem = Path(name).stem
  [tops, a, b] = top_points(cattle)
  print(len(tops))

  cc = np.tile([0,1,0], (tops.shape[0], 1))

  tops[:,2] = 0

  savePath = Path(cattle_path, f'{stem}.npy')
  np.save(savePath, tops[:, [0,1]])

  return tops[:, [0,1]]

#root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/total'
#name = '8-1_9-58_8_0.pcd'
#
#cattle_path = Path(root_path, name)
#
#calf = Farm(name, rotate=False, data_path=cattle_path, mkdir=False)
#calf.show_summary()
#calf.visual()
#
#tpcd = backbone(cattle_path, name)
#data = backbone_xy(cattle_path, name)
#
#calf.updatePCD(tpcd)
#calf.show_summary()
#calf.visual()
#
#getAngle(data)

def casty(cattle):
  points = cattle.getPoints() 
  points[:, 1] = 0
  cattle.visual()