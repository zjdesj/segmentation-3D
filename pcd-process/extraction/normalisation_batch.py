from rotate import rotate, rotateSpe, rotateReverse
from queryDirection import getCategory
from getArc import getaArc, getPCD, getBodyArc, getEPCD
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
  cattleE = getEPCD(name)
  target = Path(standing_path, 'rotation', direction)
  #target = Path(standing_path, 'rotate')

  cattle.show_summary()

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
    cattleE = rotateSpe(cattleE, dire)
  else:
    arc1 = getaArc(cattle)
    cattle = rotate(cattle, dire, arc1)

    arc2 = getBodyArc(cattle, dire)

    cattle = getPCD(name)
    cattleE = getEPCD(name)
    cattle = rotate(cattle, dire, arc1 + arc2)
    cattleE = rotate(cattleE, dire, arc1 + arc2)

  if direction in ['1', '2']:
    cattle = rotateReverse(cattle)
    cattleE = rotateReverse(cattleE)

  cattle.savePCD('ro', targetDir=target)
  cattleE.savePCD('re', targetDir=target)

if __name__ == '__main__':
  #forCategory('1')
  ##for12(name, '1')
  #forAll()
  forOne('n15-5_31-82_5_above.pcd', '3')
