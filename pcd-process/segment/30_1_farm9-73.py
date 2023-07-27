import sys
import numpy as np
sys.path.append('..')
from farm import segmentation, test_segment, getNumbers, dbscan
from individuals import process
from pathlib import Path

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
pcd_name = '9-73.pcd'

stem = Path(pcd_name).stem
farm_path = str(Path(pcd_path, stem))
cattle_path = str(Path(pcd_path, stem, stem + '_cropx', stem + '_cropx_cropz/clusters/standing'))
p_path = str(Path(pcd_path, stem, stem + '_cropx', stem + '_cropx_cropz/', stem + '_cropx_cropz.pcd'))

segmentation(pcd_path, pcd_name, 20, 15.5)

#process(cattle_path, farm_path)

#test_segment(p_path, 0.03, 1, 400, save=True)

#dbscan(p_path, -11.7, 0.07, 1, 2000)

#getNumbers(p_path, -9.45)
