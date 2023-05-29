import open3d as o3d
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, SymLogNorm

def pretty(d): 
  print('{')
  for e in d:
    print(f'  {e}: {d[e]}')
  print('}\n')

# 相对于项目根目录的数据目录
__Data__ = '../data/pcd'
def add_dataPath():
    file_path = Path(__file__)
    project_root = file_path.parent.parent
    data_path = Path(project_root, __Data__)
    return data_path

class Farm():
  
  def __init__(self, pcd_name, rotate=False):
    # load point cloud data path
    self.name = Path(pcd_name).stem
    data_path = add_dataPath() 
    pcd_path = Path(data_path, pcd_name).resolve()
    pcd_path_str = str(pcd_path)
    print(f"Load a ply point cloud: {pcd_path_str}")
    pcd = o3d.io.read_point_cloud(pcd_path_str)

    # rotate point cloud 
    if rotate:
      R1 = pcd.get_rotation_matrix_from_xyz((0, 0, np.pi/18))
      #R2 = pcd.get_rotation_matrix_from_xyz((0, np.pi/3, 0))
      pcd = pcd.rotate(R1)

    self.updatePCD(pcd)
    #self.pcd = pcd
    #self.set_summary()
    
    print(f'name: {self.name}')

  def set_summary(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    summary = {}
    summary['points'] = len(points)
    summary["center"] = pcd.get_center()
    summary["max_bound"] = pcd.get_max_bound()
    summary["min_bound"] = pcd.get_min_bound()
    summary["region"] = (summary["max_bound"] - summary["min_bound"])
    summary["area"] = np.prod(summary["region"][0:2])

    self.summary = summary
    return summary
    
  def show_Summary(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    #self.get_summary(pcd)
    print('\n')
    print(f"summary of point cloud {self.name}: ")
    pretty(self.summary)
  
  def visual(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    
    visualizer = o3d.visualization.Visualizer()
    visualizer.create_window(self.name)

    visualizer.add_geometry(pcd)

    # note the center of point cloud in the window
    center = self.summary["center"]
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.1)
    sphere.translate(center)
    sphere.paint_uniform_color(np.asarray([1., 0., 0.]))
    visualizer.add_geometry(sphere)

    ro = visualizer.get_render_option()
    # must after added geometry, then it is possible to set the point_size.
    ro.point_size = 1
    # set the background color of the open3d window to total black.
    #ro.background_color = np.asarray([0,0,0])
    # show coordination system
    ro.show_coordinate_frame = True

    # must after added geometry, then it is possible to set full screen.
    visualizer.set_full_screen(True)
    view_ctl = visualizer.get_view_control()
    view_ctl.set_zoom(0.2)
    visualizer.run()
    #visualizer.destroy_window()

  def dense(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    fig = plt.figure(num=1, figsize=(8,8))

    # blue
    z = fig.add_subplot(221)
    z.hist(points[:,2] - self.summary["min_bound"][2], bins=100)
    z.set_title('z-axis')

    # red
    x = fig.add_subplot(222)
    x.hist(points[:,0], bins=620)
    x.set_title('x-axis')

    # green
    y = fig.add_subplot(223)
    y.hist(points[:,1], bins=220)
    y.set_title('y-axis')

    xy = fig.add_subplot(224) 
    xy.hist2d(points[:, 0], points[:, 1], [620, 220], norm=LogNorm())
    xy.set_aspect(1)
    xy.set_title('x-y plane')
    
    fig.suptitle('points distribution')
    plt.show()

  def showHeightDense(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    z = points[:,2]
    #z = z - self.summary["min_bound"][2]
    fig, ax = plt.subplots()
    ax.set_title('points distribution on height/ 1cm')
    ax.hist(z, bins=332)
    ax.annotate(" cattle should be under this height",xy=(-6.5,100),xytext=(-6.8,500),
      arrowprops=dict(facecolor="red",shrink=0.05,headwidth=12,headlength=6,width=4),
      fontsize=12)
    plt.show()
    
  def showXYDense(self, pcd=None, hexbin=False, all=False):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    x = points[:, 0]
    y = points[:, 1]

    fig, ahex = plt.subplots()
    ahex.set_title('points distribution on xy plane/ 5cm x 5cm')
    ret = ahex.hist2d(points[:, 0], points[:, 1], [1240, 440], norm=LogNorm())
    ahex.set_aspect(1)

    fig.colorbar(ret[3], ax=ahex, orientation='horizontal')

    plt.show() 

  def updatePCD(self, pcd):
    self.pcd = pcd
    self.set_summary()
  def getPoints(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    points = np.asarray(self.pcd.points)
    return points 

  #--------- below methods introduce filters to copy with point cloud.
  def removeRoofAndGround(self, max_threshold=-6.5, min_threshold=-7.85):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]
    # roof
    max_bound[2] = max_threshold
    # ground
    min_bound[2] = min_threshold
    
    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)

    #self.show_Summary(cpcd)
    return cpcd
    self.updatePCD(cpcd)
    #self.visual()
  def savePCD(self, name, pcd=None):
    if not pcd:
      pcd = self.pcd 

    data_path = add_dataPath() 
    pcd_path = Path(data_path, name).resolve()
    pcd_path_str = str(pcd_path)
    print(f"save a point cloud: {pcd_path_str}")

    o3d.io.write_point_cloud(pcd_path_str, pcd)
  
  def removal(self, pcd=None):
    if not pcd:
      pcd = self.pcd
    #rpcd, list = self.pcd.remove_radius_outlier(15, 0.05, True)
    #rpcd, list = self.pcd.remove_radius_outlier(30, 0.05, True)
    rpcd, list = self.pcd.remove_radius_outlier(100, 0.1, True)
    return rpcd

  def cluster(self, pcd=None):
    if not pcd:
      pcd = self.pcd
    print(' start cluster, method: DBSCAN: ')

    eps = 0.5
    min_points = 1000
    labels = np.array(pcd.cluster_dbscan(eps, min_points, print_progress=True))
    max_label = labels.max()    # 获取聚类标签的最大值 [-1,0,1,2,...,max_label]，label = -1 为噪声，因此总聚类个数为 max_label + 1
    print(f"point cloud has {max_label + 1} clusters")

    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0  # labels = -1 的簇为噪声，以黑色显示
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    self.visual(pcd)



if __name__ == '__main__':
  #farm = Farm('31-7.pcd', rotate=True)
  #farm.show_Summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()

  #cpcd = farm.removeRoofAndGround()
  #farm.updatePCD(cpcd)
  #farm.show_Summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()
  #farm.savePCD('31-7_crop.pcd')

  #rpcd = farm.removal()
  #farm.updatePCD(rpcd)
  #farm.show_Summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()
  #farm.savePCD('31-7_crop_raius.pcd')


  farm = Farm('31-7_crop.pcd')
  #farm.visual()
  farm.show_Summary()
  farm.cluster()


