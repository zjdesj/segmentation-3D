import numpy as np
from basement import Farm
from pathlib import Path

pcd_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_pcd'
pcd_name = '8-333.pcd'


def segmentation(pcd_path, pcd_name, shift=3.5, shift_y=0, min_points=10, min_clusters=2000):
  farm = Farm(pcd_name, rotate=True, data_path=pcd_path)
  # 分析原始数据
  #farm.visual()
  farm.savePCDInfo()

segmentation(pcd_path, pcd_name, 6.2)

  