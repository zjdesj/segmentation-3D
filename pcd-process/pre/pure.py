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


def purify(cattle_path, name):
  cattle = Farm(name, rotate=False, data_path=cattle_path, mkdir=False)
  cpcd = cattle.crop_z(0.07)
  cattle.updatePCD(cpcd)

  cattle.show_summary()
  #cattle.showHeightDense()
  #cattle.dense()

  # 法线估计
  radius = 0.01   # 搜索半径
  max_nn = 30     # 邻域内用于估算法线的最大点数

  cattle.pcd.estimate_normals()     # 执行法线估计

  #cattle.visual(show_normal=True)

  normals = np.asarray(cattle.pcd.normals)
  print(normals, len(normals))


# slice by slice
def purify_1(cattle_path, name):

  # 截取去除地面的部分
  cattle = Farm(name, rotate=False, data_path=cattle_path, mkdir=False)
  cattle.visual()
  cpcd = cattle.crop_z(0.2)
  cattle.updatePCD(cpcd)

  x = np.arange(cattle.summary['min_bound'][0], cattle.summary['max_bound'][0], 0.005)

  points = cattle.getPoints() 

  pre = x[0]
  indx = np.array([], dtype='int8')
  for cur in x:
    #tmp = np.where(np.logical_and(points[:, 2] > pre, points[:, 2] <= cur)) 
    tmp = np.where(np.logical_and(points[:, 0] > pre, points[:, 0] <= cur)) 
    slice = points[tmp]
    
    if len(slice):
      ind = np.where(points[:,2] == np.max(slice[:, 2]))
      indx = np.append(indx, ind[0][0])
    pre = cur

  colors = np.asarray(cattle.pcd.colors)
  print('colors:', colors[0], len(colors), len(points))
  colors[indx] = [0, 1, 0]

  ## 获取只有点
  #curve = cattle.pcd.select_by_index(indx)
  #curve.paint_uniform_color([1, 1, 1])

  #cattle.updatePCD(curve)
  ##curve.colors = o3d.utility.Vector3dVector([0,0,0])
  ##cattle.pcd.colors = o3d.utility.Vector3dVector([1., 0., 0.])

  cattle.show_summary()
  cattle.visual()


  cattle.show_summary()

  #cattle.showHeightDense()
  #cattle.dense()
  


purify_1(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')

  

#purify(cattle_path, '9-62_cropx_cropz_cluster_5_segment.pcd')
