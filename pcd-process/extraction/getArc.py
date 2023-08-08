# a component for normalisation.
import sys
sys.path.append('..')
from basement import Farm
from sklearn.linear_model import LinearRegression
import math
import matplotlib.pyplot as plt


def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/above'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)
  return calf

def getEPCD(name):
  name = name.replace('_above', '')
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/entity'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)
  return calf

def getaArc(cattle, show=False):
  #print('getaArc')
  #cattle.show_summary()

  data = cattle.getPoints()

  x = data[:, 0].reshape(-1, 1)
  y = data[:, 1].T
  model = LinearRegression().fit(x, y)
  coef = model.coef_
  angle = math.atan(coef)
  print(f'coef: {coef}; angle: {angle}')

  if show:
    plt.scatter(x, y)
    plt.show()
  return angle

def getBodyArc(cattle, direction, show=False):
  #print('getbodyArc')
  #cattle.show_summary()
  x_min = cattle.summary["min_bound"][0]
  x_max = cattle.summary["max_bound"][0]
  gap = cattle.summary["region"][0]

  if int(direction) == 0 or int(direction) == 3:
    x_max = x_min + 0.6 * gap
  else:
    x_min = x_min + 0.4 * gap

  cpcd = cattle.crop_x(x_min, x_max)
  cattle.updatePCD(cpcd)
  #cattle.visual()

  return getaArc(cattle)

if __name__ == '__main__':
  getaArc('8-7_8-33_4_above.pcd', '0', show=True)
