import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
from backbone import backbone, backbone_xy, casty
import numpy as np
from queryMeasurement import updateGround, updateCluster,updateSize


def display_inlier_outlier(cloud, ind):
  inlier_cloud = cloud.select_by_index(ind)
  outlier_cloud = cloud.select_by_index(ind, invert=True)

  print("Showing outliers (red) and inliers (gray): ")
  #outlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
  inlier_cloud.paint_uniform_color([1, 0, 0])
  o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)
  #calf.show_summary()
  #calf.visual()
  #calf.savePCDInfo()

  # remove height over 1.35m
  if calf.summary["max_bound"][2] - calf.summary["min_bound"][2] > 1.35:
    cpcd = calf.crop_z(0)
    calf.updatePCD(cpcd)

  calf.show_summary()
  return calf


def filterGround_show(cattle):
  plane_model, inliers = cattle.pcd.segment_plane(distance_threshold=0.015, ransac_n=3, num_iterations=1000)
  display_inlier_outlier(cattle.pcd, inliers)

  
def filterGround(cattle):
  plane_model, inliers = cattle.pcd.segment_plane(distance_threshold=0.015, ransac_n=3, num_iterations=1000)
  ground = cattle.pcd.select_by_index(inliers)
  ground.paint_uniform_color([1, 0, 0])
  cpcd = cattle.pcd.select_by_index(inliers, invert=True)

  # 保存两个pcd做图
  #cattle.savePCDG('ground', pcd=ground, targetDir=cattle.dir)

  cattle.savePCDG('noGround', pcd=cpcd, targetDir=cattle.dir)


  cattle.show_summary()

  cattle.updatePCD(cpcd)

  cattle.show_summary()

  groundCenter = ground.get_center()
  ground_height = groundCenter[2]
  print('ground_center', ground_height, ground.get_max_bound()[2] - ground_height)
  #ground_height = cattle.summary["min_bound"][2]

  updateGround(cattle.name.replace('_re', ''), ground_height)
  
  return cattle, ground_height 

def filterNoise(cattle, eps=0.03, min_points=1, min_cluster=3000):
  print(' start cluster, method: DBSCAN: ')
  pcd = cattle.pcd
  dbscan = {
    'eps': eps,
    'min_points': min_points,
    'min_cluster': min_cluster
  }

  updateCluster(cattle.name.replace('_re', ''), eps, min_points, min_cluster)

  labels = np.array(pcd.cluster_dbscan(dbscan['eps'], dbscan['min_points'], print_progress=True))
  labels = cattle.filterLabels(labels, dbscan['min_cluster'])
  #labels = labels[labels > -1]
  max_label = labels.max()    # 获取聚类标签的最大值 [-1,0,1,2,...,max_label]，label = -1 为噪声，因此总聚类个数为 max_label + 1
  print(f"point cloud has {max_label + 1} clusters")

  #cattle.showClusters(labels)
  return labels

def getCluster(cattle, labels, ground_height):
  max_label = labels.max()
  pcd = cattle.pcd

  for i in range(max_label + 1):
    ind = np.where(labels == i)[0]
    cluster = pcd.select_by_index(ind)

    summary = cattle.set_summary(cluster)
    # remove lying
    if (ground_height != 0) and (summary["max_bound"][2] - ground_height < 0.75):
      continue
    # remove wall.
    if summary["region"][0] < 0.2:
      continue

    print('......', summary["points"])
    cattle.updatePCD(cluster)
    if ground_height != 0:
      updateSize(cattle.name.replace('_re', ''), summary["points"])
      cattle.savePCD(f'pure_{i}', targetDir=cattle.dir)

  return cattle

def denoise(name):
  calf = getPCD(name)
  cpcd = calf.crop_z(0)
  calf.updatePCD(cpcd)
  [calf, ground_height] = filterGround(calf)
  ### 过滤
  #return

  #cpcd = calf.crop_z(0.5)
  #calf.updatePCD(cpcd)

  #ground_height =  -9.988052368164062
  labels = filterNoise(calf)
  pure_cattle = getCluster(calf, labels, ground_height)
  return pure_cattle

# for bb use
def reDenoise(calf, ret):
  #cpcd = calf.crop_z(0.2)
  #calf.updatePCD(cpcd)

  [esp, m, ps] = ret

  labels = filterNoise(calf, esp, m, ps)

  pure_cattle = getCluster(calf, labels, 0)
  return pure_cattle


def batch_denoise(patten):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  cattle_dir = Path(root_path)
  file = cattle_dir.glob(patten)
  for calf in file:
    print(calf)
    pure_cattle = denoise(calf) 

def update_ground(patten):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  cattle_dir = Path(root_path)
  file = cattle_dir.glob(patten)
  for calf in file:
    print(calf)
    pure_cattle = denoise(calf) 

if __name__ == '__main__':
  #batch_denoise('8-1_*_re.pcd')
  #batch_denoise('8-2_*_re.pcd')
  #batch_denoise('8-3_*_re.pcd')
  #batch_denoise('8-5_*_re.pcd')
  #batch_denoise('8-7_*_re.pcd')
  #batch_denoise('8-9_*_re.pcd')

  #batch_denoise('10-1_*_re.pcd')
  #batch_denoise('10-2_*_re.pcd')
  #batch_denoise('10-3_*_re.pcd')
  #batch_denoise('10-5_*_re.pcd')
  #batch_denoise('10-7_*_re.pcd')
  #batch_denoise('10-9_*_re.pcd')

  #batch_denoise('15-1_*_re.pcd')
  #batch_denoise('15-2_*_re.pcd')
  #batch_denoise('15-3_*_re.pcd')
  #batch_denoise('15-5_*_re.pcd')
  #batch_denoise('15-7_*_re.pcd')
  #batch_denoise('15-9_*_re.pcd')

  #batch_denoise('30-1_*_re.pcd')
  #batch_denoise('30-2_*_re.pcd')
  #batch_denoise('30-3_*_re.pcd')
  #batch_denoise('30-5_*_re.pcd')
  #batch_denoise('30-7_*_re.pcd')
  #batch_denoise('30-9_*_re.pcd')

  #batch_denoise('50-1_*_re.pcd')
  #batch_denoise('50-2_*_re.pcd')
  #batch_denoise('50-3_*_re.pcd')
  #batch_denoise('50-5_*_re.pcd')
  #batch_denoise('50-7_*_re.pcd')
  #batch_denoise('50-9_*_re.pcd')

  name = 'n15-5_31-82_5_re.pcd'
  pure_cattle = denoise(name)  
