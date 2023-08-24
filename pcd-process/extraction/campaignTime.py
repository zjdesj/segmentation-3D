import sys
sys.path.append('..')
from pathlib import Path
import numpy as np
import pandas as pd
from queryMeasurement import updateColumn, queryGround, queryColumn
import datetime

import json
import re

resultFile = '../../data-result/flight-result-segment.xlsx'
df = pd.read_excel(resultFile, sheet_name='flights-points', dtype={'time': datetime.timedelta})
fileData = df.values

def updateDuration(stem, duration):
  colInd = np.where(df.columns == 'duration')[0][0]

  try:
    index = np.where(fileData[:, 0] == stem)[0][0]
    fileData[index][colInd] = duration
  except:
    print('update duration failed', stem)

def writeDuration():
    df2 = pd.DataFrame(fileData, columns=df.columns)
    df2.to_excel('../../data-result/flight-result-segment_duration.xlsx', sheet_name='flights-points', index=False)

def setWithersH(name, value, gap):
  stem = re.sub(r'_re_pure_.*', '', name)
  groundH = queryGround(stem)

  updateColumn(stem, value, 'withers height')
  updateColumn(stem, value - groundH, 'withers H')
  updateColumn(stem, gap, 'withersgap')

def batchDuration():
  HH_path = '/Volumes/2T-Experiment/许昌牛场PCD/ret_all'
  cattle_dir = Path(HH_path)
  files = cattle_dir.rglob('report.json')

  for calfFile in files:
    name = calfFile.name
    stem = calfFile.parent.parent.parent.name
    print('calf file name:', calfFile, stem)

    # Read the JSON file
    with open(calfFile, 'r') as json_file:
      data = json.load(json_file)
    
    duration = data["point cloud collection time"] / 1000
    
    updateDuration(stem, duration)
  
  writeDuration()

if __name__ == '__main__':
  
  batchDuration()
