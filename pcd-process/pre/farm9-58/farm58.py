import sys
import numpy as np
sys.path.append('../..')
from farm import Farm

#pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
#farm = Farm('9-58.pcd', rotate=True, data_path=pcd_path)
#
## 分析原始数据
#farm.show_summary(save='raw')
#farm.visual()
#farm.dense(save='raw', show=False)
#farm.showHeightDense(save='raw', show=False)
#farm.showXYDense(save='raw', show=False)
#
## 截取x
#cpcd = farm.cropFarm()
#farm.updatePCD(cpcd)
#farm.show_summary(save='cropx')
#farm.visual()
#save = input('Save cropped farm along x axis:')
#if save == 'Y':
#  farm.savePCD('cropx')

## 根据分析x后的height 去掉地面屋顶
#pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58'
#farm = Farm('9-58_cropx.pcd', data_path=pcd_path)
#farm.show_summary()
##farm.visual()
#farm.removeRoofAndGround(max_threshold=-10.3, min_threshold=-11.55)
#cpcd = farm.cropFarm()
#farm.updatePCD(cpcd)
##farm.show_summary()
##farm.visual()
#farm.show_summary(save='cropz')
#save = input('Save cropped farm along z axis:')
#if save == 'Y':
#  farm.savePCD('cropz')

# 分割
#pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-58/9-58_cropx'
#farm = Farm('9-58_cropx_cropz.pcd', data_path=pcd_path)
#farm.show_summary()
#
##labels = farm.cluster()
#labels = np.load(pcd_path + '/9-58_cropx_cropz/9-58_cropx_cropz_0.05_10.npy')
##farm.showClusters(labels)
##farm.showClusters(labels, save=True)
#
## 保存可能站立的
#farm.saveClusters(labels)

