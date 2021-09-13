# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 19:03:24 2021

@author: fuhow
跟機械手臂教導器的程式進行溝通
SM_ON_OFF 檔為0時，進行拍照; 為1時，手臂進行移動

"""

import numpy as np
import pyrealsense2 as rs
import cv2
import eye_hand_calibration_func

#讀取點
points = np.loadtxt('config/points20210428_new.txt')

# 照片儲存的資料夾名稱
date = '20210711'

# 第一個姿態
count = 0
HIWIN_ROBOT_NC_CODE = 'C:/RobotStateMachine/HIWIN ROBOT NC CODE.txt'
SM_ON_OFF_File = 'C:/RobotStateMachine/SM_ON_OFF_File.txt'
p = points[count]
X = p[0]
Y = p[1]
Z = p[2]
A = p[3]
B = p[4]
C = p[5]
F = 100
with open(HIWIN_ROBOT_NC_CODE, 'w') as f:
    f.write('MOVE\tL\t')
    f.write(f'X {X}\tY {Y}\tZ {Z}\t')
    f.write(f'A {A}\tB {B}\tC {C}\t')
    f.write(f'F {F}\n')
    f.write('SLEEP\t200\n')
    
with open(SM_ON_OFF_File, 'w') as f:
    f.write('1')



#相機串流
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Stack both images horizontally
        images = cv2.resize(color_image,(int(1280/2),int(720/2)))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)
        
        
        #讀取0或1
        with open('C:/RobotStateMachine/SM_ON_OFF_File.txt', 'r') as f:
            isOn = f.readline().strip()
        
        if isOn == '0':
            # 0就拍照
            cv2.imwrite(f'./eye_hand_charuco_pic/{date}/{count}.png', color_image)
            #cv2.imwrite(f'./innermatrix_calibration/1280_720/{count}.png', color_image)
            #cv2.imwrite(f'{count}.png', images)
            cv2.imshow(f'{count}', images)
            cv2.waitKey(200)
            cv2.destroyAllWindows()
           
            count = count + 1
            print(count)
            if count < points.shape[0]: 
                 # 更新姿態
                 p = points[count]
                 X = p[0]
                 Y = p[1]
                 Z = p[2]
                 A = p[3]
                 B = p[4]
                 C = p[5]
                 with open(HIWIN_ROBOT_NC_CODE, 'w') as f:
                     f.write('MOVE\tL\t')
                     f.write(f'X {X}\tY {Y}\tZ {Z}\t')
                     f.write(f'A {A}\tB {B}\tC {C}\t \n')
                     f.write('SLEEP\t200\n')
                     
                 # 更新0 or 1
                 with open(SM_ON_OFF_File, 'w') as f:
                     f.write('1')
                        
            else:
                break
        

finally:
    eye_hand_calibration_func.eye_hand_calibration_func(count)
    # Stop streaming
    pipeline.stop()
    

#def write_NC_code()


    

    





