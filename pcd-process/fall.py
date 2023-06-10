import numpy as np
from farm import Farm
from tqdm import tqdm

import time

farm = Farm('31-7_crop_roof.pcd')
#farm.visual()
farm.show_Summary()

points = farm.getPoints()

X = np.arange(-56.3, 7.1, 0.1)
#print(X.shape)
Y = np.arange(0, 11, 0.1)
#print(Y.shape)

M = []
N = []

for point in tqdm(points):
  [x, y, z] = point
  m = np.floor((x - (-56.3)) / 0.1)
  n = np.floor(y / 0.1)

  M.append(m)
  N.append(n)

arr = np.stack((M, N))
arr = np.transpose(arr)

points = np.hstack((points, arr))

np.savetxt('./mesh_01_01.txt', points)