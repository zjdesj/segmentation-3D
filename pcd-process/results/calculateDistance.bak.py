import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

xyzFile = '../../data-result/results-landmarks.xlsx'

def updateColumn(stem, distances):
  df = pd.read_excel(xyzFile , sheet_name='Sheet1')
  data = df.values
  keys, values = distances
  colInd = [np.where(df.columns == key)[0][0] for key in keys]

  try:
    index = np.where(data[:, 4] == stem)[0][0]
    data[index][colInd] = values
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(xyzFile, index=False)
  except:
    print('updateColumn failed')

def queryColumn(stem, A, B):
  df = pd.read_excel(xyzFile , sheet_name='Sheet1')
  data = df.values
  AInd = np.where(df.columns == A)[0][0]
  BInd = np.where(df.columns == B)[0][0]

  try:
    index = np.where(data[:, 4] == stem)[0][0]
    return data[index][AInd], data[index][BInd]
  except:
    print('QueryColumn failed')

def str2Arr(point):
  cleaned_data = point.strip('[]').split()
  float_data = [float(value) for value in cleaned_data]
  xyz = np.array(float_data)
  return xyz

def calD(stem, L1, L2):
  A, B = queryColumn(stem, L1, L2)
  A = str2Arr(A)
  B = str2Arr(B)
  return round(A[0] - B[0], 3)

def modifyRow(stem):
  AH = calD(stem, 'LH', 'LA')
  BH = calD(stem, 'LB', 'LH')
  DH = calD(stem, 'LD', 'LH')
  AB = calD(stem, 'LB', 'LA')
  MT = calD(stem, 'LM2', 'LT2')
  TH = calD(stem, 'LH', 'LT2')
  MH = calD(stem, 'LM2', 'LH')

  distances = [
    [ 'AH', 'BH', 'DH', 'AB', 'MT', 'TH', 'MH' ],
    [ AH, BH, DH, AB, MT, TH, MH ]
  ]

  updateColumn(stem, distances)

  return 
  
  print(f'AH: {AH}')
  print(f'BH: {BH}')
  print(f'DH: {DH}')
  print(f'AB: {AB}')
  print(f'MT: {MT}')
  print(f'TH: {TH}')
  print(f'MH: {MH}')
  
if __name__ == '__main__':
  modifyRow('8-1_9-58_3')
