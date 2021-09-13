# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:45:50 2020

@author: fuhow
將 align_depth2color.py 拍出的照片，計算出棋盤格座標的位置(以機械手臂基座座標)


"""
import numpy as np
import cv2 as cv
import glob
import pyrealsense2 as rs
import align_depth2color

align_depth2color.take_pic()


#load inner matrix and inverse

#inner_matrix = np.loadtxt('coordinate_transformation/config/20210331_best/self_inner_matrix_charuco_1280_30張.txt')
#dist = np.loadtxt('coordinate_transformation/config/20210331_best/self_distortion_charuco_1280_30張.txt')
inner_matrix = np.loadtxt('coordinate_transformation/config/L515/self_inner_matrix_charuco_1920_30張.txt')
dist = np.loadtxt('coordinate_transformation/config/L515/self_distortion_charuco_1920_30張.txt')
##inner_matrix = np.loadtxt('coordinate_transformation/config/L515/inMat1920.txt')
##dist = np.loadtxt('coordinate_transformation/config/L515/dist1920.txt')
#dist = np.array([0,0,0,0,0])
T_cam2gripper = np.loadtxt('coordinate_transformation/config/20210428/eye_hand_charuco_mtx_0428_less.txt')


# 讀取棋盤格座標
fname = 'color.png'
img = cv.imread(fname)
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(inner_matrix, dist, (w,h), 1, (w,h), True)
inverse_inner_matrix = np.linalg.inv(newcameramtx)
img = cv.undistort(img, inner_matrix, dist, None, newcameramtx)
img_dist = cv.resize(img, (1280, 720))
cv.imshow('img', img_dist)
cv.waitKey(0)
cv.destroyAllWindows()
#inverse_inner_matrix = np.linalg.inv(inner_matrix)

# print(newcameramtx)
# print(inner_matrix)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 棋盤大小
ch_X = 9
ch_Y = 6

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Find the chess board corners
ret, corners = cv.findChessboardCorners(gray, (ch_X, ch_Y), None)

corners2 = cv.cornerSubPix(gray,corners, (7,7), (-1,-1), criteria)

# id  = [45+i*2 for i in range(5)]
# id2 = [0, 2, 4, 6, 8, 9, 18, 27, 36, 17, 26, 35, 44]
# id = id+id2
# id = [0,46,2,48,4,50,6,52,8]
#id = [8]
#id = [9*i for i in range(6)]
id = [0, 8, 45, 53, 31]
# id = [31]
X_list = []
Y_list = []
# Z = -270
A = -180
B = 0
C = 90
F = 75
txtname = 'config/my_test_0428.txt'
depth_image = np.load('config/depth.npy')
depth_image = depth_image.T
print(depth_image.shape)

with open(txtname, 'w') as f:
    f.write('')
 
    
corner0 = corners2[46,0,:]
center0 = np.array([corner0[0], corner0[1], 1])
#z_depth = depth_image[int(round(center0[0])), int(round(center0[1]))]

for i,j in enumerate(id):
    # Draw the corner on the image
    corner2 = corners2[j,0,:]
    corner2_tup = tuple(corner2)
    ##cv.circle(img,corner1,10,(255,0,0),-1)
    cv.circle(img,corner2_tup,5,(0,255,0),-1)
    imS = cv.resize(img, (1280, 720))
    cv.imshow('img', imS)
    cv.waitKey(500)
    cv.destroyAllWindows()
    
    #找出影像座標
    white_center = np.array([corner2[0], corner2[1], 1])
    #print("white_center: \n", white_center)
    
    #找出深度值
    z_depth = depth_image[int(round(white_center[0])), int(round(white_center[1]))]
    print(z_depth)
    if z_depth == 0:
        continue    

    #影像座標到camera座標
    #final_translation = np.dot(inverse_inner_matrix, np.matrix.transpose(white_center))
    final_translation = np.dot(inverse_inner_matrix, np.matrix.transpose(white_center))
    #print(final_translation)
    
    #以深度值Z: scaling
    final_translation = final_translation * (z_depth / final_translation[2])
    final_translation = np.append(final_translation, np.array([1]))
    # print(final_translation)
    
    
    final_translation = np.dot(T_cam2gripper, final_translation)
    
    #gripper to arm base
    #T = np.array([[0, 1, 0, 0], [1, 0, 0, 470], [0, 0, -1, 293.5], [0, 0, 0, 1]])
    T = np.array([[0, 1, 0, 0], [1, 0, 0, 397.5], [0, 0, -1, 364], [0, 0, 0, 1]])
    # T = np.array([[-1, 0, 0, 0], [0, 1, 0, 397.5], [0, 0, -1, 415], [0, 0, 0, 1]])
    # print("T: \n", T)
    
    arm_translation = np.dot(T, final_translation)
    # print("arm_translation: \n", arm_translation)
    
    
    
    
    X = arm_translation[0]#+1
    Y = arm_translation[1]#-2.5
    #Z = arm_translation[2] + 110+2+1.3;
    # Z = 24.5
    Z = -21
    # X_list.append(X)
    # Y_list.append(Y)

    
    with open(txtname, 'a') as f:
        f.write('MOVE\tL\t')
        f.write(f'X {X}\tY {Y}\tZ {Z}\t')
        f.write(f'A {A}\tB {B}\tC {C}\t')
        f.write(f'F {F}\n')
        f.write('SLEEP\t2000\n')
    #print(X, Y)
    



