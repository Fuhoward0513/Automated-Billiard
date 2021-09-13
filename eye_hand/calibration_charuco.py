# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:55:41 2021

@author: fuhow

用 fname 資料夾中的 charaurco 照片來校正相機"內部參數矩陣"
"""
import cv2 as cv
import numpy as np

params = cv.aruco.DetectorParameters_create()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
#chboard = cv.aruco_CharucoBoard.create(5, 7, 0.04, 0.02, dictionary)
chboard = cv.aruco_CharucoBoard.create(5, 7, 0.029, 0.0145, dictionary)
img_num = 34
all_corners = []
all_ids = []

for i in range(img_num):
    a = i
    # image read
    fname = f'innermatrix_calibration/L515_1920_20210515\{a}_Color.png'
    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    # detect corners, ids
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray, dictionary, parameters=params)
    
    # calibration
    if len(ids) > 0:
        # charucoCorners, charucoIds
        retval, charucoCorners, charucoIds = cv.aruco.interpolateCornersCharuco(corners, ids, gray, chboard)
        if len(charucoCorners)>0:
            all_corners.append(charucoCorners)
            all_ids.append(charucoIds)
            print(i)
# In[]    
# inner_matrix = np.loadtxt('config/inMat_1280.txt')
# dist = np.loadtxt('config/CameraDistortion.txt')     
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(all_corners, all_ids, chboard, gray.shape[::-1], None, None)
print(cameraMatrix)
print(distCoeffs)
# In[]
np.savetxt("config/L515/self_inner_matrix_charuco_1920_30張.txt", cameraMatrix)
np.savetxt("config/L515/self_distortion_charuco_1920_30張.txt", distCoeffs)
    
