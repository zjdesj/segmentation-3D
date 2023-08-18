import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm, SymLogNorm
import datetime

resultFile = '../../data-result/flight-result-segment.xlsx'
df = pd.read_excel(resultFile, sheet_name='flights-points', dtype={'time': datetime.timedelta})

def plotStanding():
  data = df.values[:, :]

  sortedData = data[data[:, 2].argsort()]
  sortedData[:, 3:] = sortedData[:, 3:].astype(int)

  d8 = np.array([cam for cam in sortedData if cam[0].startswith('8')])
  d9 = np.array([cam for cam in sortedData if cam[0].startswith('9')])
  
  time1 = d8.T[2]
  total1 = d8.T[3]
  a1 = d8.T[4]

  time1 = [datetime.datetime.combine(datetime.date.today(), t) for t in time1]

  time2 = d9.T[2]
  total2 = d9.T[3]
  a2 = d9.T[4]
  time2 = [datetime.datetime.combine(datetime.date.today(), t) for t in time2]

  #创建子图
  fig, ax = plt.subplots(1, 1, figsize=(10, 5)) 
  ax.grid(False) 

  #ax.xaxis.set_major_locator(mdates.AutoDateLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.plot(time1, total1, 'd-', color = 'b', label='afternoon campaigns on 9th Jan.')
  ax.plot(time1, a1, 'd-', color = 'g', label='individuals from afternoon campaigns on 9th Jan.')
  ax.plot(time2[0:13], total2[0:13], 's-', color = 'b', label='morning campaigns on 9th Jan.')
  ax.plot(time2[0:13], a2[0:13], 's-', color = 'g', label='individuals from morning campaigns on 9th Jan.')
  ax.plot(time2[13:], total2[13:], 'o-', color = 'b', label='afternoon campaigns on 9th Jan.')
  ax.plot(time2[13:], a2[13:], 'o-', color = 'g', label='individuals from afternoon campaigns on 9th Jan.')

  plt.xlabel('time of conducting campaigns')
  plt.ylabel('count of standing cattle')
  plt.legend(loc='best')

  fig.autofmt_xdate()

  plt.tight_layout()
  plt.show()

def plotRatio():
  data = df.values[:, [1, 3, 4]].T
  ratio = data[2, :] / data[1, :] * 100
  data = np.r_[data, [ratio]]
  
  rs = np.reshape(data[3], (5, 6))
  print(rs[0])
  r8 = data[3, 0:6]
  print(r8)
  r10 = data[3, 6:12]
  r15 = data[3, 12:18]
  r30 = data[3, 18:24]
  r50 = data[3, 24:]

  s = [1,2,3,5,7,9]
  
  fig, ax = plt.subplots(1, 1, figsize=(10, 5)) 
  ax.grid(False) 
  ax.plot(s, r8, 'o-', color = 'b', label='ratio of usage at height 8m')
  ax.plot(s, r10, 'o-', color = 'r', label='ratio of usage at height 10m')
  ax.plot(s, r15, 'o-', color = 'g', label='ratio of usage at height 15m')
  ax.plot(s, r30, 's-', color = 'b', label='ratio of usage at height 30m')
  ax.plot(s, r50, 's-', color = 'g', label='ratio of usage at height 50m')

  plt.xlabel('speed')
  plt.ylabel('ratio of standing cattle usage')
  plt.legend(loc='best')
  
  plt.tight_layout()
  plt.show()


def plotRatioPlot():
  data = df.values[:, [1, 3, 4]].T
  ratio = data[2, :] / data[1, :] * 100
  data = np.r_[data, [ratio]]
  
  rs = np.reshape(data[3], (5, 6))
  s = [1,2,3,5,7,9]

  fig, ax = plt.subplots(1, 1, figsize=(10, 5)) 
  ax.grid(False) 

  ax.boxplot(rs, labels=s)

  plt.xlabel('speed')
  plt.ylabel('ratio of standing cattle usage')
  plt.legend(loc='best')
  
  plt.tight_layout()
  plt.show()


def plotPoints():
  data = df.values[:, [1, 5]].T

  points = np.reshape(data[1], (5, 6))
  s = [1,2,3,5,7,9]

  fig, ax = plt.subplots(1, 1, figsize=(10, 5)) 
  ax.grid(False) 

  ax.boxplot(points, labels=s, patch_artist=True)

  #ax.plot(s, points[0], 'o-', color = 'b', label='number of the point cloud at height 8m')
  #ax.plot(s, points[1], 's-', color = 'b', label='number of the point cloud at height 10m')
  #ax.plot(s, points[2], 'p-', color = 'b', label='number of the point cloud at height 15m')
  #ax.plot(s, points[3], '*-', color = 'b', label='number of the point cloud at height 30m')
  #ax.plot(s, points[4], 'x-', color = 'b', label='number of the point cloud at height 50m')

  def millions(x, pos):
    """The two arguments are the value and tick position."""
    return f'{x*1e-6:1.1f}M'
  ax.yaxis.set_major_formatter(millions)
  #ax.xaxis.set_major_formatter()

  plt.xlabel('flight speed(m/s)')
  plt.ylabel('point numbers in point clouds')
  #plt.legend(loc='best')
  
  plt.tight_layout()
  plt.show()

def plotDouble():
  # 设置两种绘图颜色
  c1='r'
  c2='b'
  c3='y'
  data = df.values

  sortedData = data[data[:, 2].argsort()]
  sortedData[:, 3:] = sortedData[:, 3:].astype(int)

  d8 = np.array([cam for cam in sortedData if cam[0].startswith('8')])
  d9 = np.array([cam for cam in sortedData if cam[0].startswith('9')])
  
  time1 = d8.T[2]
  total1 = d8.T[3]
  a1 = d8.T[4]

  time1 = [datetime.datetime.combine(datetime.date.today(), t) for t in time1]

  time2 = d9.T[2]
  total2 = d9.T[3]
  a2 = d9.T[4]
  time2 = [datetime.datetime.combine(datetime.date.today(), t) for t in time2]

  #创建子图
  fig = plt.figure(figsize=(10, 5))

  ax = fig.add_subplot(111, label='1') 
  ax2 = fig.add_subplot(111, label='2', frame_on=False)
  ax.grid(False) 

  #ax.xaxis.set_major_locator(mdates.AutoDateLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.plot(time1, total1, 'd-', color = c1, label='afternoon campaigns on 8th Jan.')
  #ax.plot(time1, a1, 'd-', color = c3, label='individuals from afternoon campaigns on 9th Jan.')
  ax.plot(time2[0:12], total2[0:12], 's-', color = c1, label='morning campaigns on 9th Jan.')
  #ax.plot(time2[0:12], a2[0:12], 's-', color = c3, label='individuals from morning campaigns on 9th Jan.')
  ax.plot(time2[12:], total2[12:], 'o-', color = c1, label='afternoon campaigns on 9th Jan.')
  #ax.plot(time2[12:], a2[12:], 'o-', color = c3, label='individuals from afternoon campaigns on 9th Jan.')

  ax.set_xlabel('time of conducting campaigns', color=c1)
  ax.set_ylabel('count of standing cattle', color=c1)
  ax.legend(loc='lower center')
  ax.set_yticks([0,5,10,15,20,25,30,35,40, 45, 50])

  # 调整第二对坐标轴的label和tick位置，以实现双X轴双Y轴效果
  ax2.xaxis.tick_top()
  ax2.yaxis.tick_right()
  ax2.xaxis.set_label_position('top')
  ax2.yaxis.set_label_position('right')
  ax2.set_xlabel('flight speed(m/s)', color=c2)
  ax2.set_ylabel('point numbers in point clouds', color=c2)
  def millions(x, pos):
    """The two arguments are the value and tick position."""
    return f'{x*1e-6:1.1f}M'
  ax2.yaxis.set_major_formatter(millions)

  data2 = df.values[:, [1, 5]].T
  points = np.reshape(data2[1], (5, 6))
  s = [1,2,3,5,7,9]
  ax2.boxplot(points, labels=s, patch_artist=True)

  # 设置坐标轴刻度颜色
  ax.tick_params(axis='x', colors=c1)
  ax.tick_params(axis='y', colors=c1)
  ax2.tick_params(axis='x', colors=c2)
  ax2.tick_params(axis='y', colors=c2)

  ti = np.array([5,10,15,20,25,30,35,40,45,50]) * 1000000
  ax2.set_yticks(ti)
  ax2.invert_yaxis()
  # 设置坐标轴线颜色
  ax.spines["left"].set_color(c1) # 修改左侧颜色
  ax.spines["right"].set_color(c2) # 修改右侧颜色
  ax.spines["top"].set_color(c2) # 修改上边颜色
  ax.spines["bottom"].set_color(c1) # 修改下边颜色

  fig.autofmt_xdate()

  plt.tight_layout()
  plt.show()

  

#plotRatio()
#plotRatioPlot()
#plotStanding()
#plotPoints()
plotDouble()

