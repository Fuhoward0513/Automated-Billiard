# -*- coding: utf-8 -*-
"""
Created on Mon May 17 20:38:18 2021

@author: asus

計算機械手臂 Z 方向下降距離
狀況一: 若白球距離撞球檯邊 < table_offset，則 Z 方向須抬高，以免與手臂碰撞
狀況二: 若白球距離周圍普通球 < ball_offset，則 Z 方向須抬高，以免與手臂碰撞
"""
import numpy as np

def cal_height(white, ball, hole):
    flag = 0 # 高度是否要調高
    ''' 白球是否靠近邊緣 '''
    hole_x_min = 10000
    hole_y_min = 10000
    hole_x_max = -1
    hole_y_max = -1
    for i in range(len(hole)): # find the boundary of holes
        if(hole[i][0]<hole_x_min):
            hole_x_min = hole[i][0]
        if(hole[i][0]>hole_x_max):
            hole_x_max = hole[i][0]
        if(hole[i][1]<hole_y_min):
            hole_y_min = hole[i][1]
        if(hole[i][1]>hole_y_max):
            hole_y_max = hole[i][1]
    
    hole_boundary = np.asarray([[hole_x_min, hole_y_min], [hole_x_max, hole_y_max]])
    print("hole_boundary",hole_boundary)
    
    table_offset = 70
    if (white[0]-hole_x_min)<table_offset or (hole_x_max-white[0])<table_offset : # 靠近邊多少要設定
        flag = 1
        print('x太靠近')
    if (white[1]-hole_y_min)<table_offset or (hole_y_max-white[1])<table_offset :
        flag = 1
        print('y太靠近')
    
    ''' 白球附近是否有球很靠近 '''
    ball_offset = 150
    for i in range(len(ball)):
        dis = np.sqrt((white[0]-ball[i][0])**2 + (white[1]-ball[i][1])**2)
        if(dis<ball_offset): # 靠近球多少要設定
            print('球太靠近')
            flag = 1
            break
    return flag

