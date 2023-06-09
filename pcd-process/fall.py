import numpy as np
from farm import Farm
from tqdm import tqdm

import time

farm = Farm('31-7_crop_roof.pcd')
#farm.visual()
farm.show_Summary()

points = farm.getPoints()

print(points[1:3])

X = np.arange(-56.3, 7.1, 0.1)
#print(X.shape)
Y = np.arange(0, 11, 0.1)
#print(Y.shape)

for point in tqdm(points):
  