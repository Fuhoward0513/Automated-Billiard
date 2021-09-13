# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:35:41 2021

@author: fuhow

計算機械手臂 C軸 要選轉多少
"""

import numpy as np
import cv2 as cv
import glob
import pyrealsense2 as rs


def calculate_C(white_x, white_y, hitten_x, hitten_y, hole_x, hole_y):
    from coordinate_transformation import pix2mm
    ball_d = 31.35
    # ball_d = 100
    
    if(hitten_x==hole_x and hitten_y==hole_y):
        white = pix2mm.pix2mm(white_x, white_y)
        hitten = pix2mm.pix2mm(hitten_x, hitten_y)
        white_x, white_y = white[0], white[1]
        hitten_x, hitten_y = hitten[0], hitten[1]
        theta2 =  np.arctan2(hitten_y-white_y, hitten_x-white_x) / np.pi * 180
        return theta2
        
    # calculate theta1
    y = (hitten_y-hole_y)
    x = (hitten_x-hole_x)
    # 成像座標->機械座標 y 加負號
    theta1 = np.arctan2(-y, x)

    print('theta1: ', theta1 / np.pi * 180)
    
    white = pix2mm.pix2mm(white_x, white_y)
    hitten = pix2mm.pix2mm(hitten_x, hitten_y)
    white_x, white_y = white[0], white[1]
    hitten_x, hitten_y = hitten[0], hitten[1]
    
    
    # calculate theta2
    # target_x = hitten_x + ball_d * np.cos(theta1)
    # target_y = -hitten_y + ball_d * np.sin(theta1)
    # theta2 =  np.arctan2(-white_y-target_y, white_x-target_x) / np.pi * 180
    # print('theta2: ', theta2)
    
    # 轉世界座標
    target_x = hitten_x + ball_d * np.cos(theta1)
    target_y = hitten_y + ball_d * np.sin(theta1)
    # theta2 =  np.arctan2(white_y-target_y, white_x-target_x) / np.pi * 180
    theta2 =  np.arctan2(target_y-white_y, target_x-white_x) / np.pi * 180
    print('theta2: ', theta2)
    
    return theta2







 
