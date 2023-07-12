import numpy as np
from farm import Farm
from tqdm import tqdm

import time

farm = Farm('31-7_crop_roof.pcd')
#farm.visual()
farm.show_Summary()

points = farm.getPoints()
colors = np.asarray(farm.pcd.colors)
print(colors.shape)
print(points.shape)

cattleIndex = np.where(points[:, 2] >= -7.6)
print(f'confirmed points as cattle or building contain {np.array(cattleIndex).shape} points')

l_points = points[np.where(points[:, 2] < -7.6)]
print(f'uncerain points (< -7.6): {points.shape}')


#for point in l_points[0:5]:
#  [x, y, z] = point
#  z_threshold = z + 0.1
#  
  
  #tmp = points[points[:,1] >= y -0.005 ] 
  #print(f'tmp.shape(1) {tmp.shape}')
  #tmp = tmp[tmp[:, 0] == x]
  #print(f'tmp.shape(2) {tmp.shape}')
X = np.arange(-56.3, 7.1, 0.1)
#print(X.shape)
Y = np.arange(0, 11, 0.1)
#print(Y.shape)

grid = []
count = 0

inds = ()
#for i in range(X.shape[0]):
for l in tqdm(X, desc='X in '):
  x0 = l
  x1 = l + 0.1
  for w in Y:
    count = count + 1
    y0 = w
    y1 = w + 0.1
    tmp = np.where(np.logical_and(np.logical_and(points[:, 0] >= x0, 
                                  points[:, 0] < x1
                                  ), np.logical_and(points[:, 1] >= y0,
                                  points[:, 1] < y1))) 
    arr = points[tmp]
    len = arr.shape[0]
    gap = 0
#    mean = 0
#    var = 0
    if len > 1:
      gap = np.ptp(arr[:,2])
#      mean = np.percentile(arr[:,2], 90)
#      var = np.var(arr[:,2])
#    #print(f'{arr.shape}, mean: {np.mean(arr[:,2])}, variance: {np.var(arr[:,2])}')
    #grid.append([x0, x1, y0, y1, len, gap, mean, var])
    grid.append([x0, x1, y0, y1, len, gap])
    #grid = np.concatenate((grid, [[x0, x1, y0, y1, len, gap]]))

    if gap < 0.1:
      inds = inds + tmp

np.savetxt('./inds.txt', np.asarray(inds))
np.savetxt('./grid.txt', grid)
