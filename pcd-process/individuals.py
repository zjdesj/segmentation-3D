import sys
import numpy as np
from farm import Farm
from pathlib import Path
import time
import shutil

# 手动处理挑选站立牛的点云后，处理

def process(cattle_path, farm_path):
  cattle_dir = Path(cattle_path)
  files = cattle_dir.glob('*.pcd') 
  cattle_dir_name = cattle_dir.parent.stem + '_cluster'
  print(f'cattle_dir_name: {cattle_dir_name}')

  farm_dir = Path(farm_path) 
  farm = Farm(f'{farm_dir.stem}.pcd', rotate=True, data_path=farm_path, mkdir=False)

  for file in sorted(files):
    print(file.name, '\n')

    cattle = Farm(file.name, data_path=cattle_path, mkdir=False)
    cattle.show_summary()

    pcd = farm.cropCattle(cattle) 
    cattle.updatePCD(pcd)
    cattle.show_summary()
      
    cattle.saveCattlePCD('segment', cattle.pcd)
    cattle.newSaveDir()
    cattle.savePCDInfo()
  return 
