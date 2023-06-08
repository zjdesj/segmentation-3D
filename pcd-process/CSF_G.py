import numpy as np
from farm import Farm
import CSF
import time

farm = Farm('31-7_crop_roof.pcd')
#farm.visual()
farm.show_Summary()

xyz = farm.getPoints()
print(xyz.shape)

csf = CSF.CSF()

# prameter settings
csf.params.bSloopSmooth = True
csf.params.cloth_resolution = 0.005

csf.params.time_step = 0.65
#Classification threshold refers to a threshold (the unit is same as the unit of pointclouds) to classify the pointclouds into ground and non-ground parts based on the distances between points and the simulated terrain. 0.5 is adapted to most of scenes.
csf.params.class_threshold = 0.001
csf.params.interations = 500

csf.setPointCloud(xyz)
ground = CSF.VecInt()  # a list to indicate the index of ground points after calculation
non_ground = CSF.VecInt() # a list to indicate the index of non-ground points after calculation
s_t = time.time()
csf.do_filtering(ground, non_ground) # do actual filtering.
e_t = time.time()

print(f'time span: {e_t - s_t}')

g = farm.pcd.select_by_index(np.array(ground))
c = farm.pcd.select_by_index(np.array(non_ground))
g_name = f'./31-7_crop_roof_ground_0005_0001.pcd'
c_name = f'./31-7_crop_roof_cattle_0005_0001.pcd'
farm.savePCD(g_name, g)
farm.savePCD(c_name, c)

