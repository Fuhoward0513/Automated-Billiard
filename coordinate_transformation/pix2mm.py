# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 19:20:23 2021

@author: fuhow

影像座標轉為世界座標(機械手臂基座座標)
"""

import numpy as np
import cv2 as cv
import glob
import pyrealsense2 as rs


def pix2mm(ball_x, ball_y):
    
    #load inner matrix and inverse
    
    #inner_matrix = np.loadtxt('eye_hand/config/20210331_best/self_inner_matrix_charuco_1280_30張.txt')
    #dist = np.loadtxt('eye_hand/config/20210331_best/self_distortion_charuco_1280_30張.txt')
    inner_matrix = np.loadtxt('eye_hand/config/L515/self_inner_matrix_charuco_1920_30張.txt')
    dist = np.loadtxt('eye_hand/config/L515/self_distortion_charuco_1920_30張.txt')
    T_cam2gripper = np.loadtxt('eye_hand/config/20210710/eye_hand_charuco_mtx_0710.txt')
##    inverse_inner_matrix = np.linalg.inv(inner_matrix)
    
    # 考慮 undistortion
    h = 1080
    w = 1920
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(inner_matrix, dist, (w,h), 1, (w,h), True)
    inverse_inner_matrix = np.linalg.inv(newcameramtx) 
    
    # 讀取深度影像
    depth_image = np.load('config/depth.npy')
    depth_image = depth_image.T
    # print(depth_image.shape)
    
    white_center = np.array([ball_x, ball_y, 1])
    
        
    #找出深度值
    z_depth = depth_image[int(round(white_center[0])), int(round(white_center[1]))]
    if(z_depth==0):
        z_depth = 444
    z_depth = 442
    print('depth: ', z_depth)
    
    
    #影像座標到camera座標
    final_translation = np.dot(inverse_inner_matrix, np.matrix.transpose(white_center))
    #print(final_translation)
        
    #以深度值Z: scaling
    final_translation = final_translation * (z_depth / final_translation[2])
    final_translation = np.append(final_translation, np.array([1]))
    # print(final_translation)
        
        
    final_translation = np.dot(T_cam2gripper, final_translation)
        
    #gripper to arm base
    T = np.array([[0, 1, 0, 0], [1, 0, 0, 360], [0, 0, -1, 364], [0, 0, 0, 1]])
    
    arm_translation = np.dot(T, final_translation)
    # print("arm_translation: \n", arm_translation)
    
    return arm_translation
    
    
