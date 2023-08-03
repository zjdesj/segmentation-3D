from rotate import rotate, rotateSpe, rotateReverse
from queryDirection import getCategory
from getArc import getaArc, getPCD, getBodyArc
from pathlib import Path
import numpy as np
from tqdm import tqdm

standing_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/'


def main():
  rotation = Path(standing_path, 'rotation')
  
  #for cate in  tqdm(['0', '1', '2', '3'], desc='Rotating cattle'):
  cate = '1'
  target = Path(rotation, cate)
  target.mkdir(exist_ok=True)
  data = getCategory(cate)
  print(f'data: {data}')
  for stem in tqdm(data[:, 1].T, desc='Rotating cattle'):
    print(f'stem: {stem}')
    name = stem + '_above.pcd'
    forOne(name, cate)

def forOne2R(cattle, dire):
  arc1 = getaArc(cattle)
  cattle = rotate(cattle, dire, arc1)

  arc2 = getBodyArc(cattle, dire)

  return arc1 + arc2


def forOne(name, direction):
  cattle = getPCD(name)

  if direction == '1':
    cattle = rotateReverse(cattle)
    dire = '3'
  elif direction == '2':
    cattle = rotateReverse(cattle)
    dire = '0'
  else:
    dire = direction

  if direction in ['4', '5', '6']:
    cattle = rotateSpe(cattle, dire)
  else:
    arc = forOne2R(cattle, dire)

    cattleR = getPCD(name)
    if direction in ['1', '2']:
      cattleR = rotateReverse(cattle)

    cattleN = rotate(cattleR, dire, arc)

    target = Path(standing_path, 'rotation', direction)
    cattleN.savePCD('ro', targetDir=target)

if __name__ == '__main__':
  name = '15-3_9-49_18_above.pcd'
  #forOne(name, '5')
  main()




