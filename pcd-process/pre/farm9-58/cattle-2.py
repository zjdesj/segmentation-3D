import sys
import numpy as np
sys.path.append('../..')
from farm import Farm

# 手动处理挑选站立牛的点云后，处理
pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx/9-58_cropx_cropz/standing'
cattle_2 = Farm('9-58_cropx_cropz_cluster_7.pcd', data_path=pcd_path, mkdir=False)
cattle_2.show_summary()
#cattle_2.visual()

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'
farm = Farm('9-58.pcd', rotate=True, data_path=pcd_path, mkdir=False)

pcd = farm.cropCattle(cattle_2) 
cattle_2.updatePCD(pcd)
cattle_2.show_summary()
cattle_2.visual()

cattle_2.savePCD('segment', newDir=True)