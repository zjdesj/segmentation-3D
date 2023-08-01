from feature import rotate 
from pathlib import Path
import numpy as np
from tqdm import tqdm

standing_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/'

def main():
  # zip 文件夹
  source = Path(standing_path, 'entity')
  target = Path(standing_path, 'entity-r')

  source_a = Path(standing_path, 'above')   
  traget_a = Path(standing_path, 'above-r')

  for cattle in  tqdm(source_a.iterdir(), desc='Rotating cattle'):
    
