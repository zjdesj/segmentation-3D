# a component for normalisation.
import numpy as np
import pandas as pd
from pathlib import Path

headings = '../../data-result/data-direction-night-flat.xlsx'
df = pd.read_excel(headings, sheet_name='Sheet1', header=None)

def queryDirection(name):
  data = df.values

  stem = Path(name).stem

  index = np.where(data[:, 4] == stem)
  print(index)
  direction = data[:, 3][index][0]
  print(direction)
  #print('innnnnn', index, direction)

  return direction

def getCategory(cate):
  data = df.values
  print(data)
  dirctions = data[:, 3]
  inds = np.where(dirctions == cate)
  stems = data[inds][:, [3,4]]
  #print(stems)
  return stems

#headings_old = '../../data-result/data-derection.xlsx'
#df = pd.read_excel(headings, sheet_name='data-derection', header=None)
#def queryDirection_old(name):
#  data = df.values.T
#  data[3] = [item.split('\t') for item in data[3]]
#  data[2] = [item.split('\t') for item in data[2]]
#
#  data = data.T
#
#  ## 检验不对等的数据
#  #inds = data[len(data[:,2]) != len(data[:,3])]
#  #print(inds)
#
#  arr = Path(name).stem.split('_')
#
#  campaign = arr[0]
#  ind = np.where(data[:, 0] == campaign)
#  item = data[ind][0]
#  #print(item)
#  cattle = '.'.join(arr[2:])
#  #print(cattle)
#
#  index = np.where(np.array(item[2]) == cattle)
#  direction = np.array(item[3])[index][0]
#  #print('innnnnn', index, direction)
#
#  return direction
#