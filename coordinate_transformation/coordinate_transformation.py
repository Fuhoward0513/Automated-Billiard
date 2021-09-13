# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 16:00:03 2021

@author: fuhow

1. 讀取白球、球、洞 pixel 值，並將其自影像座標轉為世界座標(機械手臂基座座標)
2. 計算機械手臂 C軸 選轉角度
3. 將機械手臂擊球位置寫入 'C:/RobotStateMachine/SM_ON_OFF_File.txt'
"""

import numpy as np
import cv2 as cv
import glob
import pyrealsense2 as rs

def coordinate_transformation(num_ball, isConvex):
    from coordinate_transformation import pix2mm
    from coordinate_transformation import calculate_angle
    # 讀取照片
    fname = 'color.png'
    img = cv.imread(fname)
    
    # 讀取白球、球、洞 pixel 值
    with open('config/result.txt') as f:
        white = f.readline()
        white = white.split()
        white = np.array(white).astype(int)
        white_x = white[0]
        white_y = white[1]
        # print(white)
        hitten = f.readline()
        hitten = hitten.split()
        hitten = np.array(hitten).astype(int)
        hitten_x = hitten[0]
        hitten_y = hitten[1]
        # print(hitten)
        hole = f.readline()
        hole = hole.split()
        hole = np.array(hole).astype(int)
        hole_x = hole[0]
        hole_y = hole[1]
        
        target = f.readline()
        target = target.split()
        target = np.array(target).astype(float)
        target = np.array(target).astype(int)
        target_x = target[0]
        target_y = target[1]
        
        flag = f.readline()
        flag = int(flag.strip())
        
    ''' 擊球軌跡視覺化 '''    
    # 畫出pixel點在照片上
    # 畫點
    cv.circle(img,(white_x, white_y),10,(0,0,255),-1) # 劃出白球的點
    cv.circle(img,(white_x, white_y),50,(0,0,255),5) # 劃出白球的半徑
    
    cv.circle(img,(hitten_x, hitten_y),10,(255,0,0),-1) #畫出被打的球的點
    cv.circle(img,(hitten_x, hitten_y),50,(255,0,0),5) #畫出被打的球的半徑
    
    cv.circle(img,(hole_x, hole_y),10,(0,255,0),-1) #畫出洞的點
    
    cv.circle(img,(target_x, target_y),5,(0,255,255),-1) #畫出白球預計打位置
    cv.circle(img,(target_x, target_y),50,(0,255,255),5) #畫出target半徑
    
    #畫線
    cv.line(img, (white_x, white_y), (target_x, target_y), (0, 0, 0), 3) #白球到target
    cv.line(img, (hole_x, hole_y), (target_x, target_y), (0, 0, 0), 3) #洞到target
    
    imS = cv.resize(img, (1280, 720))
    cv.imshow('img', imS)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    ''' 影像座標轉為世界座標(機械手臂基座座標)'''
    # 計算 世界座標 x, y
    arm_translation = pix2mm.pix2mm(white_x, white_y)
    
    ''' 計算機械手臂C軸要轉幾度'''
    # 計算氣壓缸要轉幾度 
    C_gripper = calculate_angle.calculate_C(white_x, white_y, hitten_x, hitten_y, hole_x, hole_y)  
    if num_ball == 1 and isConvex:
        print('偏')
        C_gripper += 3
    print("C_gripper", C_gripper)
    
    ''' 寫入檔案 '''
    txtname = 'C:/RobotStateMachine/HIWIN ROBOT NC CODE.txt'
    with open(txtname, 'w') as f:
        f.write('')
    
    X = arm_translation[0] #+1
    Y = arm_translation[1]#-1#-2.5
    Z = 50
    A = -180
    B = 0
    C = C_gripper + 90
    F = 80
    
    with open(txtname, 'a') as f:
        f.write('MOVE\tL\t')
        f.write(f'X {X}\tY {Y}\tZ {Z}\t')
        f.write(f'A {A}\tB {B}\tC {C}\t')
        f.write(f'F {F}\n')
        f.write('SLEEP\t2000\n')
        
    X = X - 80*np.cos(C_gripper/180*np.pi)
    Y = Y - 80*np.sin(C_gripper/180*np.pi)
    with open(txtname, 'a') as f:
        f.write('MOVE\tL\t')
        f.write(f'X {X}\tY {Y}\tZ {Z}\t')
        f.write(f'A {A}\tB {B}\tC {C}\t')
        f.write(f'F {F}\n')
        f.write('SLEEP\t2000\n')
     
    # Z = 36
    #Z = 50.695
    # 距離撞球檯高度
    if(flag==0):
        Z = 12
    elif(flag==1):
        Z = 12+20  #看要調高多少
    with open(txtname, 'a') as f:
        f.write('MOVE\tL\t')
        f.write(f'X {X}\tY {Y}\tZ {Z}\t')
        f.write(f'A {A}\tB {B}\tC {C}\t')
        f.write(f'F {F}\n')
        f.write('SLEEP\t2000\n')

        # 氣壓打球
        f.write('IO\t17\t1\t2000\n')
        f.write('IO\t17\t0\t2000\n')

    X = 0
    Y = 360
    Z = 364
    A = -180
    B = 0
    C = 90
    F = 100
    # 回拍照姿態    
    with open(txtname, 'a') as f:
        f.write('MOVE\tL\t')
        f.write(f'X {X}\tY {Y}\tZ {Z}\t')
        f.write(f'A {A}\tB {B}\tC {C}\t')
        f.write(f'F {F}\n')
        f.write('SLEEP\t2000\n')

    SM_ON_OFF_File = 'C:/RobotStateMachine/SM_ON_OFF_File.txt'
    with open(SM_ON_OFF_File, 'w') as f:
        f.write('1')
    
