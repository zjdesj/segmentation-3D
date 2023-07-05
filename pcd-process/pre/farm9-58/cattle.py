import sys
sys.path.append('../..')
from individuals import process

cattle_path  = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx/9-58_cropx_cropz/standing'
farm_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'

process(cattle_path, farm_path)