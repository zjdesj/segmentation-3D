import sys
sys.path.append('../..')
from individuals import process

cattle_path  = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-62/9-62_cropx/9-62_cropx_cropz/clusters'
farm_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-62'

process(cattle_path, farm_path)