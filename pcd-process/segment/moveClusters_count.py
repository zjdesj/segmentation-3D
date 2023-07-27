from pathlib import Path
from tqdm import tqdm
import csv

def getZip(root):
  # zip 文件夹
  root = Path(root)
  source = Path(root, 'ret_pcd')
  target = Path(root, 'cattle')

  f = open(Path(source, 'summary.csv'), 'w')
  writer = csv.writer(f)

  for plan in tqdm(source.iterdir(), desc='Moving cattle'):
    if not plan.is_dir():
      continue
    stem = Path(plan).stem
    cattle_path = Path(plan, stem + '_cropx', stem + '_cropx_cropz/clusters')

    standing = Path(cattle_path, 'standing')

    files = standing.glob('*.pcd')
    writer.writerow([stem, len(list(files))])

  f.close()
    
if __name__ == '__main__':
  root = '/Volumes/2T-Experiment/许昌牛场PCD/'
  getZip(root)