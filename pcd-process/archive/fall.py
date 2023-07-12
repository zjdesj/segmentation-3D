import numpy as np
from farm import Farm
from tqdm import tqdm

import time

def seive(farm, step = 0.1):
  [x_max, y_max, z_max] = farm.summary["max_bound"]
  [x_min, y_min, z_min] = farm.summary["min_bound"]

  print(f'x_min: {x_min}, x_max: {x_max}')

  points = farm.getPoints()[1:10]

  #X = np.arange(np.floor(x_min / step), np.ceil(x_max / step), 1)
  #Y = np.arange(np.floor(y_min / step), np.ceil(y_max / step), 1)
  #print(X.shape)
  #print(Y.shape)

  M = []
  N = []

  for point in tqdm(points):
    [x, y, z] = point
    print(f'point: {point}')
    m = np.floor((x - x_min) / step)
    n = np.floor((y - y_min) / step)
    print(m, n)

    M.append(m)
    N.append(n)

  print(M, N)
  arr = np.stack((M, N)).astype(int)
  print(arr)
  arr = np.transpose(arr)
  
  print(arr.dtype)
  dt = np.dtype(['float64, float64, float64, int32, int32]'])
  points = np.hstack((points, arr)).astype(dt)
  print(points)


if __name__ == '__main__':
  farm = Farm('31-7_sample.pcd')
  farm.show_summary()
  seive(farm)
