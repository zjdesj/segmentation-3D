import sys
import numpy as np
sys.path.append('../..')
from farm import Farm
from pathlib import Path

# 手动处理挑选站立牛的点云后，处理

def process(id, extraWork=False, mode='visual'):
  cattle_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx/9-58_cropx_cropz/standing'
  files = Path(cattle_path).glob('*.pcd') 

  for file in files:
    print(file, '\n')
  return 


  cattle = Farm(f'9-58_cropx_cropz_cluster_{id}.pcd', data_path=cattle_path, mkdir=False)
  cattle.show_summary()

  if extraWork:
    cattle = extraWork(cattle)

  if mode == 'visual':
    cattle.visual()
    return
  
  farm_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'
  farm = Farm('9-58.pcd', rotate=True, data_path=farm_path, mkdir=False)
  
  pcd = farm.cropCattle(cattle) 
  cattle.updatePCD(pcd)
  cattle.show_summary()
  cattle.visual()
  
  cattle.savePCD('segment', newDir=True)

# normal
#cattle_3 = process('21')
#cattle_3 = process('21', mode='save')

#cattle_4 = process('24')
#cattle_4 = process('24', mode='save')

# normal
#cattle_5 = process('31')
#cattle_5 = process('31', mode='save')

# normal
#cattle_6 = process('42')
#cattle_6 = process('42', mode='save')

# normal
#cattle_7 = process('60')
#cattle_7 = process('60', mode='save')

process(1)