# -*- coding: utf-8 -*-
"""
Created on Sat May  1 21:52:22 2021

@author: asus

計算點到值線的距離

"""

import numpy as np

def point_to_line_distance(point, line_point1, line_point2):
    # 計算直線的三個參數
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + (line_point2[0] - line_point1[0]) * line_point1[1]
    # 計算點到線距離
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    # print(distance)
    return distance
