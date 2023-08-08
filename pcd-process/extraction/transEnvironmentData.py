# 将方向文件转换为按方向分类

import numpy as np
import pandas as pd
from pathlib import Path

envs = '../../data-result/flight-result-segment.xlsx'
df = pd.read_excel(envs, sheet_name='environment', header=None)

def trans():
  data = df.values
  print(data[0:3, :], len(data[0]))

  for row in data:
    name = '_'.join([row[1], row[0]])
    row[8] = name
    
  df2 = pd.DataFrame(data, columns=['plan', 'campaign' , 'time', 'max-illumiantion', 'min-illumiantion', 'temperature', 'moisture', 'max-wind-speed', 'stem'])


  spath = Path(envs).parent
  df2.to_excel(Path(spath, 'data-envs.xlsx'), index=False)
    
trans()