import open3d as o3d
import sys
import numpy as np
sys.path.append('..')
from basement import Farm
from pathlib import Path


pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-59'
pcd_name = '9-59.pcd'
#segmentation(pcd_path, pcd_name, 3.5)
#farm = Farm(pcd_name, rotate=False, data_path=pcd_path, mkdir=False)
#farm.visual()

stem = Path(pcd_name).stem
farm_path = str(Path(pcd_path, stem))
cattle_path = str(Path(pcd_path, stem + '_cropx', '9-59_cropx_cropz' ))
farm = Farm('9-59_cropx_cropz.pcd', rotate=False, data_path=cattle_path, mkdir=False)
#farm.visual()


labels = np.load('/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-59/9-59_cropx/9-59_cropx_cropz/9-59_cropx_cropz_0.05_1_5000.npy')
farm.showClusters(labels, save=True)

#process(cattle_path, farm_path)


p_path = str(Path(pcd_path, stem, stem + '_cropx', stem + '_cropx_cropz/', stem + '_cropx_cropz.pcd'))
#test_segment(p_path, 0.05, 1, 4000, save=True)

#getNumbers(p_path, -9.45)

#