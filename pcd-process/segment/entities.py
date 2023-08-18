import open3d as o3d
import sys
import numpy as np
sys.path.append('..')
from farm import Farm
from individuals import process
from pathlib import Path
from tqdm import tqdm


def entity(cattle_path, farm_path, stem):
  print(f'farm path: {farm_path}')
  print(f'cattle path: {cattle_path}')

  farm = Farm(f'{stem}.pcd', rotate=True, data_path=farm_path, mkdir=False)
  cattle = cattle_path.glob('*_cropx_cropz_cluster*.pcd')

  for file in sorted(cattle):
    print(file.name, '\n')

    calf = Farm(file.name, data_path=cattle_path, mkdir=False)
    calf.show_summary()
    #calf.visual()

    body = farm.cropCattle(calf) 
    calf.updatePCD(body)
    calf.show_summary()
    #calf.visual()
      
    calf.saveCattlePCD('segment', calf.pcd)
    calf.newSaveDir()
    calf.savePCDInfo()
  return 

#entity(cattle_path, farm_path)


def getEntities(root_path):
  farm_path = Path(root_path, 'ret_pcd')
  cattle_path = Path(root_path, 'cattle')
  dirs = cattle_path.glob('31-*')

  for plan in tqdm(dirs, desc='get cattle entities of standard standing'):
  #for plan in tqdm(['9-53', '9-54'], desc='get cattle entities of standard standing'):
    if not plan.is_dir():
      continue
    stem = Path(plan).stem
    #print(f'stem: {stem}')
    farm = Path(farm_path, stem)
    cattle = Path(cattle_path, stem)
    entity(cattle, farm, stem)

  return

def getUncertain(root_path, stem):
  # stem = '9-62'
  farm_path = Path(root_path, 'ret_pcd')
  cattle_path = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/', stem, 'uncertain/uncertain_clusters')

  farm = Path(farm_path, stem)
  entity(cattle_path, farm, stem)


if __name__ == '__main__':
  root = '/Volumes/2T-Experiment/许昌牛场PCD/'
  #getEntities(root)

  #getUncertain(root, '31-77')
  #getUncertain(root, '31-79')
  #getUncertain(root, '31-80')
  #getUncertain(root, '31-82')
  getUncertain(root, '31-83')
  getUncertain(root, '31-84')
  getUncertain(root, '31-85')
  getUncertain(root, '31-86')
