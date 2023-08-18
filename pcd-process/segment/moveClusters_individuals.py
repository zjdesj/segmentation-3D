from pathlib import Path
from tqdm import tqdm
from shutil import copy

target_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/'
root = Path('/Users/wyw/Documents/Chaper2/github-code/data/cattle/')

def move_individual(plan, flight, arr):
  # zip 文件夹
  source = Path(root, flight)
  target = Path(target_path)

  for cattle in tqdm(arr, desc='Moving cattle'):
    if '.' not in cattle:
      name = f'{flight}_cropx_cropz_cluster_{cattle}'
      copy(Path(source, name, name + '.pcd'), Path(target_path, 'above', f'{plan}_{flight}_{cattle}_above.pcd'))
      copy(Path(source, name + '_segment.pcd'), Path(target_path,'entity', f'{plan}_{flight}_{cattle}.pcd')) 
      continue
    [a, b] = cattle.split('.')
    name = f'{flight}_cropx_cropz_cluster_{a}_cattle_{b}'
    copy(Path(source, name, name + '.pcd'), Path(target_path, 'above', f'{plan}_{flight}_{a}_{b}_above.pcd'))
    copy(Path(source, name + '_segment.pcd'), Path(target_path,'entity', f'{plan}_{flight}_{a}_{b}.pcd')) 
    
if __name__ == '__main__':

  flight = '9-70'
  plan = '50-9'
  arr = ['2', '0.0', '0.1', '1.0']
  move_individual(plan, flight, arr)