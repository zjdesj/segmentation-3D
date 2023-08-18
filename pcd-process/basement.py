import open3d as o3d
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, SymLogNorm
import shutil

def pretty(d, save_path=False): 
  if save_path:
    with open(save_path, 'w') as fw:
      fw.write('{\n')
      for e in d:
        fw.write(f'  {e}: {d[e]}\n')
      fw.write('}\n')
      fw.close()
  else:
    print('{')
    for e in d:
      print(f'  {e}: {d[e]}')
    print('}\n')

def add_dataPath(data_path):
# 相对于项目根目录的数据目录
    __Data__ = data_path
    file_path = Path(__file__)
    project_root = file_path.parent.parent
    data_path = Path(project_root, __Data__)
    return data_path

def set_dir_path(path, name):
  file = Path(path, name + '.pcd')
  dir = Path(path, name) 
  dir.mkdir(exist_ok=True)
  if file.is_file():
    shutil.move(file, dir)
  return dir

class Farm():
  
  def __init__(self, pcd_name, rotate=False, data_path = add_dataPath('../data/pcd'), mkdir=True):
    # load point cloud data path
    self.name = Path(pcd_name).stem
    self.dir = data_path
    if mkdir:
      self.newSaveDir()
    #if mkdir:
    #  self.dir = set_dir_path(data_path, pcd_name)
    
    pcd_path = Path(self.dir, pcd_name)
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
    
  def show_summary(self, pcd=None, save=False, show=True):
    if not pcd:
      pcd = self.pcd 
    #self.get_summary(pcd)
    if save:
      pretty(self.summary, save_path=Path(self.dir,f'{self.name}_summary.txt'))
    if show:
      print('\n')
      print(f"summary of point cloud {self.name}: ")
      pretty(self.summary)
  
  def visual(self, pcd=None, show_normal=False):
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
    #visualizer.add_geometry(sphere)

    ro = visualizer.get_render_option()
    # must after added geometry, then it is possible to set the point_size.
    ro.point_size = 1
    # set the background color of the open3d window to total black.
    #ro.background_color = np.asarray([0.6,0.6,0.6])
    #ro.background_color = np.asarray([1,1,1])
    ro.background_color = np.asarray([0,0,0])
    # show coordination system
    ro.show_coordinate_frame = True

    #ro.point_show_normal = show_normal

    # must after added geometry, then it is possible to set full screen.
    visualizer.set_full_screen(True)
    view_ctl = visualizer.get_view_control()
    view_ctl.set_zoom(1)
    #view_ctl.set_zoom(0.2)
    visualizer.run()
    #visualizer.destroy_window()

  def dense(self, pcd=None, save=False, show=True):
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
    if save:
      self.saveFig(plt, 'dense')
    if show:
      plt.show()

  def showHeightDense(self, pcd=None, save=False, show=True):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    z = points[:,2]

    z = z - self.summary["min_bound"][2]

    fig, ax = plt.subplots()
    ax.set_title('points distribution on height/ 1cm')
    #ax.hist(z, bins=332)
    ax.hist(z, bins=270)
    #ax.annotate(" cattle should be under this height",xy=(-6.5,100),xytext=(-6.8,500),
    #  arrowprops=dict(facecolor="red",shrink=0.05,headwidth=12,headlength=6,width=4),
    #  fontsize=12)
    if save:
      self.saveFig(plt, 'heightDense')
    if show:
      plt.show()
    
  def showXYDense(self, pcd=None, hexbin=False, all=False, save=True, show=True):
    if not pcd:
      pcd = self.pcd 
    points = self.getPoints(pcd) 
    x = points[:, 0]
    y = points[:, 1]

    fig, ahex = plt.subplots()
    ahex.set_title('points distribution on xy plane/ 5cm x 5cm')
    ret = ahex.hist2d(points[:, 0], points[:, 1], [1240, 440], norm=LogNorm())
    ahex.set_aspect(1)

    #ahex.tick_params(labelsize=6)

    fig.colorbar(ret[3], ax=ahex, orientation='horizontal')

    if save:
      self.saveFig(plt, 'xyDense')

    if show:
      plt.show() 

  def saveFig(self, plt, type): 
    path = Path(self.dir, f'{self.name}_{type}.png')
    pathStr = str(path.resolve())
    plt.savefig(pathStr, dpi=300, transparent=True)

  def updatePCD(self, pcd):
    self.pcd = pcd
    self.set_summary()
  def getPoints(self, pcd=None):
    if not pcd:
      pcd = self.pcd 
    points = np.asarray(pcd.points)
    return points 

  #--------- below methods introduce filters to copy with point cloud.
  def cropFarm(self, shift=3.5):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]
    
    max_bound[0] = min_bound[0] + 59.5 + shift
    min_bound[0] = min_bound[0] + shift 

    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)
    return cpcd
    
  def removeRoofAndGround(self, max_threshold=-6.5, min_threshold=-7.85):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]
    # roof
    max_bound[2] = max_threshold
    # ground
    min_bound[2] = min_threshold

    ## sample slice 
    #max_bound[0] = max_bound[0] - 25
    #min_bound[0] = min_bound[0] + 25
    
    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)

    return cpcd
  
  def crop_x(self, min, max):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]

    min_bound[0] = min
    max_bound[0] = max 

    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)
    return cpcd

  def crop_z(self, gap):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]

    min = min_bound[2] + gap
    max = min_bound[2] + 1.35

    return self.removeRoofAndGround(max_threshold=max, min_threshold=min)
  
  def crop_z2(self, min, max=None):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]

    min_bound[2] = min
    if max:
      max_bound[2] = max 
    else:
      max_bound[2] = max_bound[2] 
      
    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)
    return cpcd

  def cropFarm_y_2(self, shift_y):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]
    
    max_bound[1] = min_bound[1] + 9.5 + shift_y
    min_bound[1] = min_bound[1] + shift_y 

    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)
    return cpcd

  def cropFarm_y(self, max_y, min_y):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]
    
    max_bound[1] = max_y
    min_bound[1] = min_y

    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)
    return cpcd

  def cropCattle(self, pcd):
    min_bound = self.summary["min_bound"]
    max_bound = self.summary["max_bound"]

    min_bound[0:2] = pcd.summary["min_bound"][0:2]
    max_bound[0:2] = pcd.summary["max_bound"][0:2]
    max_bound[2] = pcd.summary["min_bound"][2] + 1.7

    print(f'min_bound: {min_bound}, max_bound: {max_bound}')
    box = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)

    cpcd = self.pcd.crop(box)

    return cpcd
  

  def newSaveDir(self):
    name = self.name
    data_path = self.dir
    self.dir = set_dir_path(data_path, name)

  # for save ground backup.
  def savePCDG(self, tag, pcd, targetDir=None):
    name = f'{self.name}_{tag}'
    if not targetDir:
      targetDir = self.dir 

    pcd_path = Path(targetDir, f'{name}.pcd')
    pcd_path_str = str(pcd_path)

    print(f"Filter: save a point cloud: {pcd_path_str}")

    o3d.io.write_point_cloud(pcd_path_str, pcd)

  def savePCD(self, tag, pcd=None, targetDir=None):
    if not pcd:
      pcd = self.pcd 
      self.name = f'{self.name}_{tag}'
    #else:
    #  self.updatePCD(pcd)

    if targetDir:
      pcd_path = Path(targetDir, f'{self.name}.pcd')
    else:
      pcd_path = Path(self.dir, f'{self.name}.pcd')

    pcd_path_str = str(pcd_path)

    print(f"save a point cloud: {pcd_path_str}")

    o3d.io.write_point_cloud(pcd_path_str, pcd)
  
  def saveCattlePCD(self, tag, cattle):
    name = f'{self.name}_{tag}'
    pcd_path = Path(self.dir, f'{name}.pcd')
    pcd_path_str = str(pcd_path)
    print(f"save a point cloud for cattle: {pcd_path_str}")
    o3d.io.write_point_cloud(pcd_path_str, cattle)

  def savePCDInfo(self):
    self.show_summary(save=True, show=False)
    self.dense(save=True, show=False)
    self.showHeightDense(save=True, show=False)
    self.showXYDense(save=True, show=False)

  def removal(self, pcd=None):
    if not pcd:
      pcd = self.pcd
    #rpcd, list = self.pcd.remove_radius_outlier(15, 0.05, True)
    rpcd, list = self.pcd.remove_radius_outlier(30, 0.05, True)
    #rpcd, list = self.pcd.remove_radius_outlier(100, 0.1, True)
    return rpcd

  def cluster(self, pcd=None, eps=0.05, min_points=10, min_cluster=2000):
    if not pcd:
      pcd = self.pcd
    print(' start cluster, method: DBSCAN: ')

    dbscan = {
      'eps': eps,
      #'min_points': 10,
      #'min_cluster': 2000
      'min_points': min_points,
      'min_cluster': min_cluster
    }
    self.dbscan = dbscan
    labels = np.array(pcd.cluster_dbscan(dbscan['eps'], dbscan['min_points'], print_progress=True))
    labels = self.filterLabels(labels, dbscan['min_cluster'])
    max_label = labels.max()    # 获取聚类标签的最大值 [-1,0,1,2,...,max_label]，label = -1 为噪声，因此总聚类个数为 max_label + 1
    print(f"point cloud has {max_label + 1} clusters")


    # save labels
    npyPath = Path(self.dir, f'{self.name}_{dbscan["eps"]}_{dbscan["min_points"]}_{dbscan["min_cluster"]}.npy')
    print(f'str(npyPath): {str(npyPath)}')
    np.save(str(npyPath), labels)
    return labels
  
  def filterLabels(self, labels, min_cluster):
    max_label = labels.max() 
    print(f'min_cluster: {min_cluster}')
    n = 0
    for i in range(max_label + 1):
      li = labels[labels == i]
      if len(li) < min_cluster:
        labels[labels == i] = -1
      else: 
        labels[labels == i] = n
        n += 1

    return labels
    
  def showClusters(self, labels, save=False):
    max_label = labels.max()
    print('...labels', len(labels))
    print(f'max_label: {max_label}')
    #print(labels/max_label)
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0  # labels = -1 的簇为噪声，以黑色显示
    self.pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

    if save:
      self.savePCD('color')
    self.visual()

  def saveClusters(self, labels, foot_height=-11.54, standing_height=-10.8):
    max_label = labels.max()
    pcd = self.pcd
    self.dir = set_dir_path(self.dir, 'clusters')


    # create standingDir 
    Path(self.dir, 'standing').mkdir(exist_ok=True)
    Path(self.dir, 'no-standing').mkdir(exist_ok=True)
    Path(self.dir, 'uncertain').mkdir(exist_ok=True)

    for i in range(max_label + 1):
      ind = np.where(labels == i)[0]
      cluster = pcd.select_by_index(ind)

      summary = self.set_summary(cluster)
      #if (summary["max_bound"][2] > standing_height) and (summary["min_bound"][2] <= foot_height):
      if (summary["max_bound"][2] > standing_height) and (summary["min_bound"][2] - foot_height >= 0):
        # remove wall.
        if summary["region"][0] < 0.2:
          continue
        self.saveCattlePCD(f'cluster_{i}', cluster)
  def saveClusters_2(self, labels):
    max_label = labels.max()
    pcd = self.pcd
    self.dir = set_dir_path(self.dir, f'uncertain_clusters')

    for i in range(max_label + 1):
      ind = np.where(labels == i)[0]
      cluster = pcd.select_by_index(ind)

      summary = self.set_summary(cluster)
      if summary["region"][0] < 0.2:
        continue
      self.saveCattlePCD(f'cattle_{i}', cluster)


if __name__ == '__main__':
  farm = Farm('31-7.pcd', rotate=True)
  #farm.show_summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()

  #cpcd = farm.removeRoofAndGround(min_threshold=-8)
  #farm.updatePCD(cpcd)
  #farm.show_summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()
  #farm.savePCD('31-7_sample.pcd')

  #rpcd = farm.removal()
  #farm.updatePCD(rpcd)
  #farm.show_summary()
  #farm.visual()
  #farm.dense()
  #farm.showHeightDense()
  #farm.showXYDense()
  #farm.savePCD('31-7_crop_raius.pcd')


  #farm = Farm('31-7_crop.pcd')
  #farm.visual()
  #farm.show_summary()
  #labels = farm.cluster()
  #farm.showClusters(labels)
  #farm.saveClusters(labels)

  #farm = Farm('./31-7/31-7_crop_dbscan_5.0-10-2000-5.pcd')
  #farm.show_summary()
  #farm.visual()


  farm = Farm('./31-7/31-7_crop_dbscan.pcd')
  farm.show_summary()
  farm.visual()