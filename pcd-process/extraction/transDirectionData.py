# 将方向文件转换为按方向分类

import numpy as np
import pandas as pd
from pathlib import Path

headings = '../../data-result/data-direction-night.xlsx'
df = pd.read_excel(headings, sheet_name='data-direction', header=None)

def trans():
  data = df.values
  print(data[0])

  ret = []
  for row in data:
    arr = row[3].split('\t')
    for ind, item in enumerate(row[2].split('\t')):
      itemT = item.replace('.', '_')
      name = '_'.join([row[0], row[1], itemT])
      ret.append([row[0], row[1], item, arr[ind], name])
    
  df2 = pd.DataFrame(ret, columns=['campaign', 'plan', 'cattle', 'direction', 'stem'])

  spath = Path(headings).parent
  print(spath)
  df2.to_excel(Path(spath, 'data-direction-night-flat.xlsx'), index=False)
    
trans()