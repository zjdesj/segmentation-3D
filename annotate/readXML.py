from pathlib import Path
from xml.dom import minidom
import numpy as np

def collectBoxes(name, label):
  print(f'name: {name}, label: {label}')
  file = Path(name)
  labelXML = Path(label, file.stem + '.xml')
  if not labelXML.is_file():
    return np.array([])
  print(f'label path: {str(labelXML)}')

  doc = minidom.parse(str(labelXML))

  boxes = []
  objects = doc.getElementsByTagName("object")
  for cattle in objects:
    x = int(cattle.getElementsByTagName("xmin")[0].firstChild.data)
    y = int(cattle.getElementsByTagName("ymin")[0].firstChild.data)
    x1 = int(cattle.getElementsByTagName("xmax")[0].firstChild.data)
    y1 = int(cattle.getElementsByTagName("ymax")[0].firstChild.data)

    boxes.append([x, y, x1, y1])
  boxes = np.array(boxes)

  return boxes

if __name__ == "__main__":
  collectBoxes("/content/DJI_20230109105426_0030_Zenmuse-L1-mission.JPG", '/content/')
