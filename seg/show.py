import open3d as o3d
import numpy as np
print("Load a ply point cloud, print it, and render it")
#ply_point_cloud = o3d.data.PCDPointCloud(data_root='/content/pcd')
pcd = o3d.io.read_point_cloud('../../data/pcd/31-7.pcd')
print(pcd)
print(np.asarray(pcd.points))
points = np.asarray(pcd.points)


#半径滤波
num_points = 20
radius = 0.05
sor_pcd, ind = pcd.remove_radius_outlier(num_points, radius)



o3d.visualization.draw_geometries([sor_pcd])