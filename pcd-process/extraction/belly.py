import open3d as o3d
import sys
sys.path.append('..')
from basement import Farm
from pathlib import Path
from backbone import backbone, top_points
import numpy as np
from queryMeasurement import queryGround, updateWidth
#from denoise_batch import reDenoise
from backbone_batch import filter

import re

def getPCD(name):
  root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'
  #root_path = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/belly'
  calf = Farm(name, rotate=False, data_path=root_path, mkdir=False)

  calf.show_summary()
  #calf.visual()
  return calf

def castXY(calf):
  pts = calf.getPoints()

  pts[:, 2] = 0

  return calf

def getBelly(name):
  calf = getPCD(name)

  stem = re.sub(r'_re_pure.*', '', name)

  ground_height = queryGround(stem)

  print(f'ground_height: {ground_height}')

  roAbove = calf.crop_z2(ground_height + 0.6)

  calf.savePCDG('above', roAbove)

  calf.updatePCD(roAbove)
  roPAbove = filter(calf)
  calf.savePCDG('abovePure', roPAbove.pcd)

  minx = roPAbove.summary['min_bound'][0]
  roPAboveCutPCD = roPAbove.crop_x(minx + 0.1, minx + 0.9)
  calf.savePCDG('abovePureCropX', roPAboveCutPCD)
  roPAbove.updatePCD(roPAboveCutPCD)

  return roPAbove

  #crap = castXY(roPAbove)
  #calf.savePCDG('abovePure-C', crap.pcd) 

def setWidth(calf):
  #calf.visual()  
  width = calf.summary['region'][1]
  print(f'width: {width}')

  stem = re.sub(r'_re_pure.*', '', calf.name)

  updateWidth(stem, width)

def batchBelly():
  bellyPath = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/r-feature'
  #bellyPath = '/Users/wyw/Documents/Chaper2/github-code/data/cattle-individual/belly'
  cattle_dir = Path(bellyPath)
  patten = '*bbInCattle.pcd'
  files = cattle_dir.glob(patten)

  for calfFile in files:
    name = Path(calfFile).name
    print('calf file name:', calfFile, name)
    calf = getBelly(name)
    setWidth(calf)

if __name__ == '__main__':
  #name = '8-1_9-58_5_0_re_pure_0_bbInCattle.pcd'
  #name = '8-1_9-58_3_re_pure_2_bbInCattle.pcd'
  #name = '8-1_9-58_0_0_re_pure_0_bbInCattle.pcd'
  #getBelly(name)

  #name = '8-1_9-58_0_0_re_pure_0_bbInCattle_abovePure.pcd'
  #calf = getPCD(name)
  #setWidth(calf)

  #name = '8-1_9-58_3_re_pure_2_bbInCattle_abovePure.pcd'
  #calf = getPCD(name)
  #setWidth(calf)

  #name = '8-1_9-58_3_re_pure_2_bbInCattle.pcd'
  #name = '8-1_9-58_0_0_re_pure_0_bbInCattle.pcd'
  #name = '15-2_9-51_8_re_pure_0_bbInCattle.pcd'
  #calf = getBelly(name)
  #setWidth(calf)


  #batchBelly()

  
