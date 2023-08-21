# a component for normalisation.
import numpy as np
import pandas as pd
from pathlib import Path

measurement = '../../data-result/data-measurement.xlsx'

def updateGround(stem, height):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][8] = height
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateGround failed')

def updateCluster(stem, eps, ps, num):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][4] = eps
    data[index][5] = ps
    data[index][6] = num
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateCluster failed')

def updateSize(stem, size):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][7] = size
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateSize failed')

def updateWidth(stem, width):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][9] = width
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateWidth failed')

def updateWidthNoPure(stem, width):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][11] = width
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateWidth failed')

def updateHH(stem, HH):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  try:
    index = np.where(data[:, 3] == stem)[0][0]
    data[index][12] = HH
    df2 = pd.DataFrame(data, columns=df.columns)
    df2.to_excel(measurement, index=False)
  except:
    print('updateHipheight failed')


def queryDBSCAN(stem):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  index = np.where(data[:, 3] == stem)[0][0]
  item = data[index]

  return item[4:7]

def queryGround(stem):
  df = pd.read_excel(measurement , sheet_name='Sheet1')
  data = df.values
  index = np.where(data[:, 3] == stem)[0][0]
  item = data[index]

  return item[8]


if __name__ == '__main__':
  ground_height = -11.72945499
  updateGround('8-1_9-58_7_re'.replace('_re', ''), ground_height)