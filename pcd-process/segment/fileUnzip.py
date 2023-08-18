from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
from shutil import copy

def getZip(root, dir):
  # zip 文件夹
  root = Path(root)
  # 保存文件夹
  dir_all = Path(dir, 'ret_all')
  dir_laz = Path(dir, 'ret_laz')
  dir_pcd = Path(dir, 'ret_pcd')
  zips = Path(root, 'ret/31_76-86-ret').glob('*.zip')
  print(dir_laz, dir_pcd)

  if not dir_all.is_dir():
    dir_all.mkdir()
  if not dir_laz.is_dir():
    dir_laz.mkdir()    
  if not dir_pcd.is_dir():
    dir_pcd.mkdir()    

  for file in tqdm(zips, desc='Unziping'):
      name = file.stem
      dir_path = Path(dir_all, name)
      ZipFile(file).extractall(dir_path)
      pcd_path = Path(dir_path, 'lidars', 'terra_pcd', 'cloud_merged.pcd')
      laz_path = Path(dir_path, 'lidars', 'terra_las', 'cloud_merged.las')
      if pcd_path.is_file():
        copy(pcd_path, Path(dir_pcd, name + '.pcd'))
      if laz_path.is_file():
        copy(laz_path, Path(dir_laz, name + '.las'))
      
    
if __name__ == '__main__':
  root = '/Volumes/2T-Experiment/许昌牛场PCD/'
  dir = root
  getZip(root, dir)