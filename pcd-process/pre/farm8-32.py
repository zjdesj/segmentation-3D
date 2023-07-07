import sys
import numpy as np
sys.path.append('..')
from farm import segmentation, test_segment, getNumbers, dbscan
from individuals import process
from pathlib import Path

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
pcd_name = '8-32.pcd'
segmentation(pcd_path, pcd_name, 6.2)

#stem = Path(pcd_name).stem
#farm_path = str(Path(pcd_path, stem))
#cattle_path = str(Path(pcd_path, stem, stem + '_cropx', stem + '_cropx_cropz/clusters'))
#process(cattle_path, farm_path)


#p_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/8-32/8-32_cropx/8-32_cropx_cropz/8-32_cropx_cropz.pcd'
##
#test_segment(p_path, 0.03, 1, 400, save=True)
#
#getNumbers(p_path, -9.45)

#dbscan(p_path, -9, 0.05, 1, 400)