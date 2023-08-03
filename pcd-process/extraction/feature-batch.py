from rotate import rotate, rotateSpe, rotateReverse
from queryDirection import getCategory
from getArc import getaArc, getPCD, getBodyArc
from pathlib import Path
import numpy as np
from tqdm import tqdm

standing_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/'
rotation = Path(standing_path, 'rotation')

def forCategory(cate):
  target = Path(rotation, cate)
  target.mkdir(exist_ok=True)
  data = getCategory(cate)
  print(f'data: {data}')
  for stem in tqdm(data[:, 1].T, desc='Rotating cattle'):
    print(f'stem: {stem}')
    name = stem + '_above.pcd'
    forOne(name, cate)

def forAll():
  for cate in tqdm(['0', '1', '2', '3', '4', '5', '6', '7'], desc='Cattle categories'):
    forCategory(cate)
  

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

  if direction in ['4', '5', '6', '7']:
    cattle = rotateSpe(cattle, dire)
  else:
    arc1 = getaArc(cattle)
    cattle = rotate(cattle, dire, arc1)

    #cattle.visual()
    arc2 = getBodyArc(cattle, dire)
    #cattle = rotate(cattle, direction, arc1 + arc2)
    #cattle.visual()

    cattle = getPCD(name)
    cattle = rotate(cattle, dire, arc1 + arc2)

  if direction in ['1', '2']:
    cattle = rotateReverse(cattle)

  target = Path(standing_path, 'rotation', direction)
  cattle.savePCD('ro', targetDir=target)

if __name__ == '__main__':
  name = '15-3_9-49_18_above.pcd'
  #forOne(name, '5')
  #forCategory('1')
  forAll()