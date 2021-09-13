# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:39:09 2021

@author: fuhow
"""

''' pose estimation '''
import numpy as np
import cv2 as cv
import generate_T

def eye_hand_calibration_func(img_num):
    count = []    
    
    #mtx = np.loadtxt('config/20210331_best/self_inner_matrix_charuco_1280_30張.txt')
    #dist = np.loadtxt('config/20210331_best/self_distortion_charuco_1280_30張.txt')
    mtx = np.loadtxt('config/L515/self_inner_matrix_charuco_1920_30張.txt')
    dist = np.loadtxt('config/L515/self_distortion_charuco_1920_30張.txt')
##    mtx = np.loadtxt('config/L515/inMat1920.txt')
##    dist = np.loadtxt('config/L515/dist1920.txt')
    
    params = cv.aruco.DetectorParameters_create()
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    #chboard = cv.aruco_CharucoBoard.create(5, 7, 0.04, 0.02, dictionary)
    chboard = cv.aruco_CharucoBoard.create(5, 7, 0.029, 0.0145, dictionary)
    
    R_target2cam = np.array([])
    t_target2cam = np.array([])
    
    
    for i in range(img_num):
        # if i in ng_id:
        #     continue
        
        a = i
        fname = f'eye_hand_charuco_pic/20210711\{a}.png'
        img = cv.imread(fname)
        # undistort
        # h,  w = img.shape[:2]
        # newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h), True)
        # img = cv.undistort(img, mtx, dist, None, newcameramtx)
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        
        corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray, dictionary, parameters=params)
        if len(ids) > 0:
            #result = cv.aruco.drawDetectedMarkers(img.copy(), corners, ids)
            result = cv.aruco.drawDetectedMarkers(img.copy(), corners, ids)
            # charucoCorners, charucoIds
            retval, charucoCorners, charucoIds = cv.aruco.interpolateCornersCharuco(corners, ids, gray, chboard)
        
            if len(charucoCorners) > 0:
                result = cv.aruco.drawDetectedCornersCharuco(result, charucoCorners, charucoIds, (255,0,0))
                retval, rvec, tvec = cv.aruco.estimatePoseCharucoBoard(charucoCorners, charucoIds, chboard, mtx, dist, rvec=None, tvec=None)
                
                # 若成功就將pose結果儲存
                if retval == True:
                    dst, jacobian =	cv.Rodrigues(src=rvec) # 轉換rvec為矩陣型式
                    
                    # 換單位 公尺 --> 毫米
                    tvec = tvec * 1000
                    
                    # 儲存 pose 結果
                    R_target2cam = np.append(R_target2cam, dst)
                    t_target2cam = np.append(t_target2cam, tvec)
                    
                    print('pic: ', fname)
                    count.append(a)
                    
                    result = cv.aruco.drawAxis(result, mtx, dist, rvec, tvec, 100)
                    
                    # 顯示照片結果
                    result = cv.resize(result, (int(1280/2), int(720/2)))
                    cv.imshow(f'{i}', result)
                    cv.waitKey(500)
                    cv.destroyAllWindows()
    
    
    # reshape
    t_target2cam = t_target2cam.reshape((len(count),3,1))
    R_target2cam = R_target2cam.reshape((len(count),3,3))
    # print('t_target2cam: \n', t_target2cam)  
    # print('R_target2cam: \n', R_target2cam) 
    cv.destroyAllWindows()
    
    
    
    ''' hand eye calibration '''
    points = np.loadtxt('config/points20210428_new.txt')
    points= points[count]
    #print(points)
    
    R_gripper2base = np.array([])
    t_gripper2base = np.array([])
    for i in range(points.shape[0]):
        angle = points[i][3:]
        R = generate_T.generate_R(angle[0], angle[1], angle[2])
        R_gripper2base = np.append(R_gripper2base,R)
        
        t = points[i][0:3]
        t_gripper2base = np.append(t_gripper2base, t)
    R_gripper2base = R_gripper2base.reshape((points.shape[0],3,3))
    t_gripper2base = t_gripper2base.reshape((points.shape[0],3,1))
    # print(t_gripper2base)
    # print(R_gripper2base)
    
    R_cam2gripper, t_cam2gripper = cv.calibrateHandEye(R_gripper2base, t_gripper2base, R_target2cam, t_target2cam, method=cv.CALIB_HAND_EYE_HORAUD)
    print('R_cam2gripper: \n', R_cam2gripper)
    print('t_cam2gripper: \n', t_cam2gripper)
    
    T = np.c_[R_cam2gripper,t_cam2gripper]
    T = np.r_[T,np.array([[0,0,0,1]])]
    np.savetxt('config/20210711/eye_hand_charuco_mtx_0711.txt', T)
    print(T)

# eye_hand_calibration_func(37)
