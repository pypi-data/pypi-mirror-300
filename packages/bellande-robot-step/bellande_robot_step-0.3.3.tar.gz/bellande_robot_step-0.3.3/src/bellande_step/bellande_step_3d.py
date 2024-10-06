#!/usr/bin/env python3

from header_imports import *

class Node3D:
    def __init__(self, x, y, z, parent=None):
        self.coord = (x, y, z)
        self.parent = parent

    @property
    def x(self):
        return self.coord[0]

    @property
    def y(self):
        return self.coord[1]

    @property
    def z(self):
        return self.coord[2]



def bellande_step_3d(node0, node1, limit=75):
    delta_x = node1.x - node0.x
    delta_y = node1.y - node0.y
    delta_z = node1.z - node0.z
    
    dist = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
    
    if dist < limit:
        return node1
    
    ratio = limit / dist
    step_x = node0.x + delta_x * ratio
    step_y = node0.y + delta_y * ratio
    step_z = node0.z + delta_z * ratio
    
    return Node3D(step_x, step_y, step_z)
