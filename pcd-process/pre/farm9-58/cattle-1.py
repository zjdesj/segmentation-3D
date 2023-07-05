import sys
import numpy as np
sys.path.append('/Users/wyw/Documents/Chaper2/github-code/segmentation-3D/pcd-process/')
from farm import Farm

# 手动处理挑选站立牛的点云后，处理
pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx/9-58_cropx_cropz/standing'
cattle_1 = Farm('9-58_cropx_cropz_cluster_0.pcd', data_path=pcd_path, mkdir=False)
cattle_1.show_summary()
#farm.visual()

cattle = cattle_1.cropFarm_y(11.2, 10.3)
cattle_1.updatePCD(cattle)
cattle_1.show_summary()
#cattle_1.visual()

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'
farm = Farm('9-58.pcd', rotate=True, data_path=pcd_path, mkdir=False)

pcd = farm.cropCattle(cattle_1) 
cattle_1.updatePCD(pcd)
cattle_1.show_summary()
cattle_1.visual()

cattle_1.savePCD('segment', newDir=True)