# -*- coding: utf-8 -*-
"""
Created on Sat May  1 20:05:32 2021

@author: asus

計算撞擊角度
註: 直線碰撞 alpha=0, 若 alpha=90則無法撞擊成功
"""
import numpy as np

def calculate_alpha(white, ball, hole): 
    # 撞球直徑
    # ball_d = 31.35
    ball_d = 100
    # 座標轉換: y 加負號 
    x_ball = ball[0]
    y_ball = -ball[1]
    
    x_hole = hole[0]
    y_hole = -hole[1]
    
    x_white = white[0]
    y_white = -white[1]
    
    ''' calculate beta: angle between hole and ball '''
    beta = np.arctan2((y_hole-y_ball), (x_hole-x_ball))
    
    
    ''' calculate target coordinates '''
    x_target = x_ball + ball_d * np.cos(beta+np.pi)
    y_target = y_ball + ball_d * np.sin(beta+np.pi)
    target = np.array([x_target, -y_target])
    ''' calculate theta: angle between white and ball '''
    theta = np.arctan2((y_target-y_white), (x_target-x_white))
    
    beta = beta/np.pi*180
    theta = theta/np.pi*180
    
    ''' calculate alpha '''
    alpha = np.abs(beta - theta)
    # alpha = beta - theta
    # if alpha < 0:
    #     alpha += 360
    
    return alpha, target
