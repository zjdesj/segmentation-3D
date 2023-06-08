import laspy
import numpy as np

inFile = laspy.read(r"../../data/las/31-7.las") # read a las file
points = inFile.points
xyz = np.vstack((inFile.x, inFile.y, inFile.z)).transpose() # extract x, y, z and put into a list

print(xyz.shape)
print(np.array(inFile.x).shape)