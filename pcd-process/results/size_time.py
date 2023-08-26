import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm, SymLogNorm
import datetime

resultFile = '../../data-result/results-campaigns.xlsx'
df = pd.read_excel(resultFile, sheet_name='flights-points', dtype={'time': datetime.timedelta})

def plotSize():
  data = df.values

  data[:, 3:6] = data[:, 3:6].astype(int)
  #ret = data[:, 5].astype(float)
  #ret = np.log(ret)
  #data[:,5] = ret

  data1 = data[:, 5] /data[:, 6]
  print(f'points rate mean: {np.mean(data1)}, deviation: {np.std(data1)}')

  data2 = data[:30, [6, 5]].T
  #data2[1] = np.log()
  print(data2, data2.shape)
  points = np.reshape(data2, (2, 5, 6))
  print(points, points.shape)

  data3 =data[30:, [6, 5]].T
  print(data3, data3.shape)
  points2 = np.reshape(data3, (2, 3, 2))
  print(points2, points2.shape)

  fig = plt.figure(figsize=(8, 8))  # Adjust the figure size if needed
  ax = fig.add_subplot(111, label='1') 

  heights = [8, 10, 15, 30, 50, 15, 10, 8]

  for i in range(5):
    x = points[0, i]
    y = points[1, i]
    print(x, y)
    ax.plot(x, y, marker='o', label=f'{heights[i]} m')

  for i in range(3):
    x = points2[0, i]
    y = points2[1, i]
    print(x, y)
    ax.plot(x, y, marker='o', label=f'{heights[i + 5]} m at night')

  def millions(x, pos):
    """The two arguments are the value and tick position."""
    return f'{x*1e-6:1.1f}M'
  ax.yaxis.set_major_formatter(millions)

  # Add labels and title
  plt.xlabel('campaign duration (seconds)')
  plt.ylabel('point cloud size')

  plt.legend()
  plt.show()

plotSize()

