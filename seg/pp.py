import pptk
import numpy as np
import laspy as lp

las = '../../data/las/19-5.las'
pd = lp.read(las)
points = np.vstack((pd.x, pd.y, pd.z)).transpose()
colors = np.vstack((pd.red, pd.green, pd.blue)).transpose()

print(len(points))
decimated_points_random = points[::10]
print(len(decimated_points_random))
v = pptk.viewer(decimated_points_random)
