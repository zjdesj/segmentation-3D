# a component for normalisation.
import numpy as np

def rotate(cattle, direction, arc):

  if direction == '0':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, -abs(arc)))
  elif direction == '3':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, abs(arc)))
  #elif direction == '1':
  #  R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi + abs(arc)))
  #elif direction == '2':
  #  R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi - abs(arc)))

 
  #R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, 0.75 * np.pi ))
  cattle.pcd = cattle.pcd.rotate(R1)
  #cattle.visual()
  return cattle

def rotateSpe(cattle, direction):
  if direction == '4':
    return cattle

  if direction == '5':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, -np.pi/2))
  elif direction == '6':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi/2))
  elif direction == '7':
    R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi))

  cattle.pcd = cattle.pcd.rotate(R1)
  return cattle

def rotateReverse(cattle):
  R1 = cattle.pcd.get_rotation_matrix_from_xyz((0, 0, np.pi))

  cattle.pcd = cattle.pcd.rotate(R1)
  return cattle