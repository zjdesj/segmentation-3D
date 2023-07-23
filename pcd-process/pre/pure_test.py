import open3d as o3d
import sys
import numpy as np
sys.path.append('..')
from farm import Farm
from individuals import process
from pathlib import Path

stem = '9-62'
#root_path = '/Volumes/2T-Experiment/许昌牛场PCD/'
root_path = '/Users/wyw/Documents/Chaper2/github-code/data'
farm_path = Path(root_path, 'ret_pcd', stem)

cattle_path = Path(root_path, 'cattle', stem)

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
def purify_1(cattle_path, name):

  # 截取去除地面的部分
  cattle = Farm(name, rotate=False, data_path=cattle_path, mkdir=False)
  cpcd = cattle.crop_z(0.2)
  cattle.updatePCD(cpcd)
  cattle.show_summary()

  # 过滤outlier
  #cl, ind = cattle.pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.1, print_progress=True)
  #cl, ind = cattle.pcd.remove_radius_outlier(nb_points=3, radius=0.01, print_progress=True)
  #colors[ind] = [0, 0, 1]
  #print(f'removal {len(ind)}')

  #cattle.updatePCD(cattle.pcd.select_by_index(ind))
  #colors = np.asarray(cattle.pcd.colors)

  x = np.arange(cattle.summary['min_bound'][0], cattle.summary['max_bound'][0], 0.01)

  points = cattle.getPoints() 

  tops = None 
  for cur in x:
    #tmp = np.where(np.logical_and(points[:, 2] > pre, points[:, 2] <= cur)) 
    slice = crop_x(cattle, cur)
    sp = cattle.getPoints(slice)
    z = sp[:, 2] 
    
    if len(sp) > 10:
      # 取前3平均值
      ind = np.argpartition(z, -3)[-3:]
      mu = np.mean(sp[ind], axis = 0)

      if not type(tops) is np.ndarray:
        tops = np.array([mu])
      else:
        tops = np.r_[tops, [mu]]
    else:
      ind = np.where(z == np.max(z))
      max = sp[ind]
      if not type(tops) is np.ndarray:
        tops = np.array(max)
      else:
        tops = np.r_[tops, max]
  print(tops.shape[0], tops[:3])
  cc = np.tile([0,1,0], (tops.shape[0], 1))
  print(cc.shape, cc[0:3])
  #tops[:,1] = 0

  tpcd = o3d.geometry.PointCloud()
  #tp = np.concatenate((points, tops), axis=0)
  #tc = np.concatenate((np.asarray(cattle.pcd.colors), cc), axis=0)

  tpcd.points = o3d.utility.Vector3dVector(tops)
  tpcd.colors = o3d.utility.Vector3dVector(cc)

  cattle.updatePCD(tpcd)

  #cattle.pcd.points = o3d.utility.Vector3dVector(np.concatenate(points, np.array(tops)))

  #colors[indx] = [0, 1, 0]

  ## 获取只有点
  #curve = cattle.pcd.select_by_index(indx)
  #curve.paint_uniform_color([1, 1, 1])

  #cattle.updatePCD(curve)
  ##curve.colors = o3d.utility.Vector3dVector([0,0,0])
  ##cattle.pcd.colors = o3d.utility.Vector3dVector([1., 0., 0.])


  cattle.show_summary()
  cattle.visual()


  #cattle.showHeightDense()
  #cattle.dense()
  


purify_1(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')

  

#purify(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')
