import numpy as np
from farm import Farm
from tqdm import tqdm

import time

points = np.loadtxt('../../data/pcd/mesh_01_01.txt')
print(points.shape)

X = np.arange(-56.3, 7.1, 0.1)
Y = np.arange(0, 11, 0.1)

grid = []
count = 0

inds = ()
#for i in range(X.shape[0]):
for x in tqdm(X[20:30], desc='X in '):
  for y in Y:
    count = count + 1
    tmp = np.where(np.logical_and(points[:, 3] == x, points[:, 4] == y)) 
    arr = points[tmp]
    len = arr.shape[0]
    gap = 0
    mean = 0
    var = 0
    if len > 1:
      gap = np.ptp(arr[:,2])
      mean = np.percentile(arr[:,2], 90)
      var = np.var(arr[:,2])
#    #print(f'{arr.shape}, mean: {np.mean(arr[:,2])}, variance: {np.var(arr[:,2])}')
    #grid.append([x0, x1, y0, y1, len, gap, mean, var])
    grid.append([x, y, len, gap, mean, var])
    #grid = np.concatenate((grid, [[x0, x1, y0, y1, len, gap]]))

    if gap < 0.1:
      inds = inds + tmp

np.savetxt('./inds.txt', np.asarray(inds))
np.savetxt('./grid.txt', grid)
