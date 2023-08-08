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

def showBackbone(name):
  calf = getPCD(name)
  calf.show_summary()
  calf.visual()

  tpcd = backbone(calf)
  #data = backbone_xy(calf, name)

  calf.updatePCD(tpcd)
  calf.show_summary()
  calf.visual()

  #tpcd = backbone(calf, name)

def filterGround_show(cattle):
  plane_model, inliers = cattle.pcd.segment_plane(distance_threshold=0.015, ransac_n=3, num_iterations=1000)
  display_inlier_outlier(cattle.pcd, inliers)

  
def filterGround(cattle):
  plane_model, inliers = cattle.pcd.segment_plane(distance_threshold=0.015, ransac_n=3, num_iterations=1000)
  ground = cattle.pcd.select_by_index(inliers)
  ground.paint_uniform_color([1, 0, 0])
  cpcd = cattle.pcd.select_by_index(inliers, invert=True)

  # 保存两个pcd做图
  cattle.savePCDG('noGround', pcd=cpcd, targetDir=cattle.dir)
  #cattle.savePCDG('ground', pcd=ground, targetDir=cattle.dir)

  cattle.show_summary()

  cattle.updatePCD(cpcd)

  cattle.show_summary()

  ground_height = cattle.summary["min_bound"][2]

  updateGround(cattle.name.replace('_re', ''), ground_height)
  
  return cattle, ground_height 

def filterNoise(cattle, eps=0.03, min_points=4, min_cluster=3000):
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
    if summary["max_bound"][2] - ground_height < 0.75:
      continue
    # remove wall.
    if summary["region"][0] < 0.2:
      continue

    print('......', summary["points"])
    updateSize(cattle.name.replace('_re', ''), summary["points"])
    cattle.updatePCD(cluster)
    cattle.savePCD(f'pure_{i}', targetDir=cattle.dir)

  return cattle

def denoise(name):
  calf = getPCD(name)
  cpcd = calf.crop_z(0)
  calf.updatePCD(cpcd)
  #[calf, ground_height] = filterGround(calf)

  cpcd = calf.crop_z(0.5)
  calf.updatePCD(cpcd)
  ground_height = -7.96043062210083

  labels = filterNoise(calf)
  pure_cattle = getCluster(calf, labels, ground_height)
  return pure_cattle

def batch_denoise(patten):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/rotate'
  cattle_dir = Path(root_path)
  file = cattle_dir.glob(patten)
  for calf in file:
    print(calf)
    pure_cattle = denoise(calf) 


if __name__ == '__main__':
  conf = {
    #'a': [0.04, 2, 2000],
    #'0_0': [0.04, 2, 1000 ],
    '4_0': [0.03, 4, 3000, 0.5]
  }
  #batch_denoise('30-2_*_re.pcd')
  name = '8-3_9-60_4_0_re.pcd'
  pure_cattle = denoise(name)  
