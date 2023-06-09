import numpy as np


x = np.arange(-56.3, 7.1, 0.05)
print(x.shape)
y = np.arange(0, 11, 0.05)
print(y.shape)

for i in x:
  x0 = x[i]
  x1 = x[i + 1]
  for j in y:
    y0 = y[j]
    y1 = y[j + 1]
    np.where()