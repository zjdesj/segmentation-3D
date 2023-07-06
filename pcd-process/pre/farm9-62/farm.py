import sys
import numpy as np
sys.path.append('../..')
from basement import Farm

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
farm = Farm('9-62.pcd', rotate=True, data_path=pcd_path)

# 分析原始数据
farm.show_summary()
farm.visual()
farm.savePCDInfo()

# 截取x
cpcd = farm.cropFarm()
farm.updatePCD(cpcd)
farm.show_summary()
farm.visual()
save = input('Save cropped farm along x axis:')
if save == 'Y':
  farm.savePCD('cropx')
  farm.newSaveDir()
  farm.savePCDInfo()


# 根据分析x后的height 去掉地面屋顶
min_height = float(input('输入最小高度: '))
max_height = float(input('输入最大高度: '))
farm.removeRoofAndGround(max_threshold=max_height, min_threshold=min_height)
cpcd = farm.cropFarm()
farm.updatePCD(cpcd)
farm.show_summary()
farm.visual()
save = input('Save cropped farm along z axis:')
if save == 'Y':
  farm.savePCD('cropz')
  farm.newSaveDir()
  farm.savePCDInfo()

labels = farm.cluster()
farm.saveClusters(labels, standing_height=(min_height + 0.8), foot_height=(min_height + 0.01))



## 分割
#pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd/9-62/9-62_cropx'
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

