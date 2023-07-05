import sys
import numpy as np
sys.path.append('../..')
from farm import Farm

# 手动处理挑选站立牛的点云后，处理
pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx/9-58_cropx_cropz/standing'
cattle_3 = Farm('9-58_cropx_cropz_cluster_21.pcd', data_path=pcd_path, mkdir=False)
cattle_3.show_summary()
cattle_3.visual()

#pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'
#farm = Farm('9-58.pcd', rotate=True, data_path=pcd_path, mkdir=False)
#
#pcd = farm.cropCattle(cattle_3) 
#cattle_3.updatePCD(pcd)
#cattle_3.show_summary()
#cattle_3.visual()
#
#cattle_3.savePCD('segment', newDir=True)