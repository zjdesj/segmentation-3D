import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm, SymLogNorm
import datetime

resultFile = '../../data-result/results-height&width.xlsx'

def updateSpeedAndHeight():
  df = pd.read_excel(resultFile)
  data = df.values

  col = data[:, 0].astype(str)
  speedAndHeight = np.vstack(np.char.split(col, sep='-'))

  data[:, [1,2]] = speedAndHeight 

  df2 = pd.DataFrame(data, columns=df.columns)
  df2.to_excel(resultFile, index=False)
  
def getDataframe():
  df = pd.read_excel(resultFile)
  return df

def summary():
  df = getDataframe()

  print(df.columns)
  grouped = df.groupby(['speed', 'height']).agg({'width': ['mean', 'std'],
                                                 'Rwidth': ['mean', 'std'],
                                                 'widthNopure': ['mean', 'std'],
                                                 'HH1': ['mean', 'std'],
                                                 'HH2': ['mean', 'std'],
                                                 'WiH1': ['mean', 'std'],
                                                 'WiH2': ['mean', 'std'],
                                                 'BH': ['mean', 'std'],
                                                 })

  print(grouped)
if __name__ == '__main__':
  #updateSpeedAndHeight()

  summary()
