import sys
import numpy as np
sys.path.append('..')
from farm import segmentation
from individuals import process
from pathlib import Path

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
pcd_name = '9-59.pcd'
segmentation(pcd_path, pcd_name)

stem = Path(pcd_name).stem
farm_path = str(Path(pcd_path, stem))
cattle_path = str(Path(pcd_path, stem, stem + '_cropx', stem + '_cropx_cropz/clusters'))

process(cattle_path, farm_path)