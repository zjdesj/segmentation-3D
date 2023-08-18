from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
from shutil import copy, copytree

def getZip(root):
  # zip 文件夹
  root = Path(root)
  source = Path(root, 'ret_pcd')
  #source = Path(root, 'ret_pcd').glob('31-*')
  target = Path(root, 'cattle')

  #for plan in  tqdm(source, desc='Moving cattle'):
  for plan in  tqdm(source.iterdir(), desc='Moving cattle'):
    print(f'\n plan: {plan}')
    if not plan.is_dir():
      continue
    stem = Path(plan).stem
    cropped_farm_path = Path(plan, stem + '_cropx', stem + '_cropx_cropz', stem + '_cropx_cropz.pcd')
    cattle_path = Path(plan, stem + '_cropx', stem + '_cropx_cropz/clusters')

    print(f'cropped_farm: {cropped_farm_path}')

    target_path = Path(target, stem) 
    target_path.mkdir(exist_ok=True)
    print(f'target_path: {target_path}')

    copytree(Path(cattle_path, 'standing'), target_path, dirs_exist_ok=True)
    copytree(Path(cattle_path, 'uncertain'), Path(target_path, 'uncertain'))
    copy(cropped_farm_path, Path(target_path, stem + '_cropx_cropz.pcd'))
    
    
if __name__ == '__main__':
  root = '/Volumes/2T-Experiment/许昌牛场PCD/'
  getZip(root)