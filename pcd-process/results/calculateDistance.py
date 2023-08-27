import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

xyzFile = '../../data-result/results-landmarks.xlsx'

def getInd(columns, keys):
  columns = np.array(columns)
  colInd = [np.where(columns == key)[0][0] for key in keys]
  return colInd

def str2Arr(point):
  cleaned_data = point.strip('[]').split()
  float_data = [float(value) for value in cleaned_data]
  xyz = np.array(float_data)
  return xyz[0]

def modifyRow(row, columns):
  landmarks = ['LT2', 'LT1', 'LA', 'LH', 'LD', 'LB', 'LM1', 'LM2']
  landmarkInd = getInd(columns, landmarks)
  landmarkStrArr = row[landmarkInd]

  vectorized_function = np.vectorize(str2Arr)

  landmarkXArr = vectorized_function(landmarkStrArr)

  LT2, LT1, LA, LH, LD, LB, LM1, LM2  =  landmarkXArr
  print('LH', LH, 'LA:', LA)

  AH = LH - LA
  BH = LB - LH
  DH = LD - LH
  AB = LB - LA
  M2T2 = LM2 - LT2
  T2H = LH - LT2
  M2H = LM2 - LH

  distances = [
    [ 'AH', 'BH', 'DH', 'AB', 'M2T2', 'T2H', 'M2H' ],
    [ AH, BH, DH, AB, M2T2, T2H, M2H ]
  ]

  distancesInd = getInd(columns, distances[0])
  row[distancesInd] = distances[1]

  return row
  
def updateData(data, cols):
  df2 = pd.DataFrame(data, columns=cols)
  df2.to_excel(xyzFile, index=False)

def batch(): 
  df = pd.read_excel(xyzFile , sheet_name='Sheet1')
  data = df.values

  for ind, row  in enumerate(data[:2, :]):
    row = modifyRow(row, df.columns)
  
  updateData(data, df.columns)

if __name__ == '__main__':
  #modifyRow('8-1_9-58_3')
  batch()
