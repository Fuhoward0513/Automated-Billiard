# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 17:31:51 2021

@author: fuhow
利用教導器上的x, y, z, a, b, c 來計算座標轉換

"""
import numpy as np

def generate_R(A, B, C):
    RotX = np.array([[1, 0, 0],
                     [0, np.cos(np.deg2rad(A)), -np.sin(np.deg2rad(A))],
                     [0, np.sin(np.deg2rad(A)), np.cos(np.deg2rad(A))]])
    RotY = np.array([[np.cos(np.deg2rad(B)), 0, np.sin(np.deg2rad(B))],
                     [0, 1, 0],
                     [-np.sin(np.deg2rad(B)), 0, np.cos(np.deg2rad(B))]])
    RotZ = np.array([[np.cos(np.deg2rad(C)), -np.sin(np.deg2rad(C)), 0],
                     [np.sin(np.deg2rad(C)), np.cos(np.deg2rad(C)), 0],
                     [0, 0, 1]])
    R = np.dot(RotY, RotX)
    R = np.dot(RotZ, R)
    #print(R)
    return R

print(generate_R(180, 0, 180))