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
  #target = Path(standing_path, 'rotation', direction)
  target = Path(standing_path, 'rotation', 'first')

  if direction == '1':
    cattle = rotateReverse(cattle)
    cattle.savePCD('rro', targetDir=target)
    dire = '3'
  elif direction == '2':
    cattle = rotateReverse(cattle)
    cattle.savePCD('rro', targetDir=target)
    dire = '0'
  else:
    dire = direction

  if direction in ['4', '5', '6', '7']:
    cattle = rotateSpe(cattle, dire)
  else:
    arc1 = getaArc(cattle)
    cattle = rotate(cattle, dire, arc1)

    #cattle.savePCD('rfo', targetDir=target)
    
    #cattle.visual()
    arc2 = getBodyArc(cattle, dire)
    #cattle = rotate(cattle, direction, arc1 + arc2)
    #cattle.visual()

    cattle = getPCD(name)
    cattle = rotate(cattle, dire, arc1 + arc2)

  if direction in ['1', '2']:
    cattle = rotateReverse(cattle)

  #cattle.savePCD('ro', targetDir=target)

def for12(name, direction):
  cattle = getPCD(name)
  target = Path(standing_path, 'rotation', direction)
  cattle.savePCD('rpo', targetDir=target)
  cattle = rotateReverse(cattle)

if __name__ == '__main__':
  name1 = '8-7_8-33_7_above.pcd' # 1
  name2 = '8-2_9-59_1_above.pcd' #2
  name0 = '8-2_9-59_9_above.pcd' #0
  name3 = '15-1_9-52_6_0_above.pcd' #3


  for ind, item in enumerate([name1, name2]):
    forOne(item, f'{ind + 1}')
  #forCategory('1')
  #forAll()
  #for12(name, '1')
