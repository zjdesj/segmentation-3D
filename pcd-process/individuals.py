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

  ## create standingDir 
  #Path(cattle_dir, 'standing').mkdir(exist_ok=True)
  #Path(cattle_dir, 'no-standing').mkdir(exist_ok=True)

  farm_dir = Path(farm_path) 
  farm = Farm(f'{farm_dir.stem}.pcd', rotate=True, data_path=farm_path, mkdir=False)

  for file in sorted(files):
    print(file.name, '\n')

    cattle = Farm(file.name, data_path=cattle_path, mkdir=False)
    cattle.show_summary()

    cattle.visual()
    time.sleep(1) 
    can_crop = input('可以直接截取否？(Y or N)')

    if can_crop == 'N':
      #is_extra = input('是否加载额外处理？(Y or N)')
      #if is_extra == 'N':
      #  continue
      #elif is_extra == 'Y':
      #  pass
      continue
    elif can_crop == 'M':
      shutil.move(file, Path(cattle_dir, 'no-standing', file.name))
    elif can_crop == 'Y':
      pcd = farm.cropCattle(cattle) 
      cattle.updatePCD(pcd)
      cattle.show_summary()
      cattle.visual()
      
      time.sleep(1) 
      is_save = input('是否保存？(Y or N)')
      if is_save == 'Y':
        cattle.saveCattlePCD('segment', cattle.pcd)
        cattle.newSaveDir()
        cattle.savePCDInfo()
        
        shutil.move(cattle.dir, Path(cattle_dir, './standing/', cattle.name))
        target_file_path = Path(cattle_dir, './standing/', cattle.name + '_segment.pcd')
        print(target_file_path)
        shutil.move(Path(cattle_dir, cattle.name + '_segment.pcd'), target_file_path)
  return 
