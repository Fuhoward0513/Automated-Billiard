# -*- coding: utf-8 -*-
"""
Created on Mon May 17 21:44:56 2021

@author: asus
1. 以綠色遮罩與原始照片做差集，只保留球的部分
2. 用 Hough circle 找出所有球的圓心
3. 計算每個球的 hsv值，hsv值最大的為白球，其餘則為普通的球
"""
import numpy as np
import cv2 as cv
from pathlib import Path

def findBall():
    """# Hough Circles"""
    def hough(org_img, img, minDist, p1, p2, minR, maxR, boundary, hole):
        cimg = img
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.medianBlur(img,5)
        # cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        
        # minDist = 50 # 任兩圓之圓心的最小距離
        # param1 = 35 # Canny edge detector的threshhold
        # param2 = 15 # 0到100，越大找到的圓越完美(越圓)
        # minR = 22 # 圓的最小半徑
        # maxR = 28 # 圓的最大半徑
        circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,minDist=minDist
                      ,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)
        circles = np.uint16(np.around(circles))
        RGB = 0
        white_pix = 0
        print(cimg.shape)
        txtname_white = 'config/white_pixel.txt'
        txtname_ball = 'config/ball_pixel.txt'
        with open(txtname_white, 'w') as f:
            f.write('')
        with open(txtname_ball, 'w') as f:
            f.write('')
            
        ''' 找RGB最大(白球) '''
        ball_distance = 40 # 離洞口多近要排除
        remove = False
        remove_list = []
        white_pix = [0,0]
        for index, i in enumerate(circles[0,:]):
            remove = False
            for j in range(6):
                if np.sqrt((i[0] - hole[j][0])**2+(i[1] - hole[j][1])**2) < ball_distance:
                    remove = True
                    remove_list.append(index)
                    break
                if i[0]<boundary[0][0] or i[0]>boundary[1][0] or i[1]<boundary[0][1] or i[1]>boundary[1][1]:
                    remove = True
                    remove_list.append(index)
                    break
            if remove:
                continue
            offset = 40
            ball_RGB = [sum(cimg[i[1]][i[0]])]
            temp = sum(cimg[i[1]][i[0]+offset])
            if temp!= 0:
                ball_RGB.append(temp)
            temp = sum(cimg[i[1]][i[0]-offset])
            if temp!= 0:
                ball_RGB.append(temp)
            temp = sum(cimg[i[1]+offset][i[0]])
            if temp!= 0:
                ball_RGB.append(temp)
            temp = sum(cimg[i[1]-offset][i[0]])
            if temp!= 0:
                ball_RGB.append(temp)
            print(sum(ball_RGB))
            ball_RGB = float(sum(ball_RGB))/len(ball_RGB)
            
            if ball_RGB > RGB:
                RGB = ball_RGB
                white_pix = i
            print(sum(cimg[i[1]][i[0]]))
            
        
        ''' 寫檔 '''
        for index, i in enumerate(circles[0,:]):
            if index in remove_list:
                continue
            else:
                if white_pix[0]==i[0] and white_pix[1]==i[1]:
                    X = white_pix[0] + crop_size
                    Y = white_pix[1] + crop_size
                    cv.circle(cimg, (X, Y), i[2], (0,0,255), 3)
                    cv.circle(cimg, (X, Y), 3, (0,0,255), -1)
                    with open(txtname_white, 'a') as f:
                        f.write(f'{X}\t{Y}\n')
                else:
                    X = i[0] + crop_size
                    Y = i[1] + crop_size
                    cv.circle(cimg, (X, Y), i[2], (0,255,0), 3)
                    cv.circle(cimg, (X, Y), 3, (0,255,0), -1)
                    with open(txtname_ball, 'a') as f:
                        f.write(f'{X}\t{Y}\n')
            
        #畫boundary
        cv.line(cimg, (boundary[0][0], boundary[0][1]), (boundary[0][0], boundary[1][1]), (255, 0, 0), 5) 
        cv.line(cimg, (boundary[0][0], boundary[0][1]), (boundary[1][0], boundary[0][1]), (255, 0, 0), 5) 
        cv.line(cimg, (boundary[1][0], boundary[1][1]), (boundary[0][0], boundary[1][1]), (255, 0, 0), 5) 
        cv.line(cimg, (boundary[1][0], boundary[1][1]), (boundary[1][0], boundary[0][1]), (255, 0, 0), 5) 

        cv.imshow('ball', cv.resize(cimg, (1280,720)))
        cv.waitKey(0)
        cv.destroyAllWindows()

    txtname = 'config/ball_hough.txt'
    
    with open(txtname, 'w') as f:
        f.write('')
        
    ''' Load hole pixel '''
    with open('config/hole.txt', 'r') as f:
       hole = list()
       for i in f:
          hole.append(i.split())
       hole = np.array(hole).astype(int)
    
    ''' find boundary '''
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
    boundary = np.asarray([[hole_x_min, hole_y_min], [hole_x_max, hole_y_max]])
    
    """# Find table using green filter"""
    img = cv.imread('color.png')
    img_resize = cv.resize(img,(1280,720))
    cv.imshow("pic", img_resize)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
##    inner_matrix = np.loadtxt('coordinate_transformation/config/L515/self_inner_matrix_charuco_1920_30張.txt')
##    dist = np.loadtxt('coordinate_transformation/config/L515/self_distortion_charuco_1920_30張.txt')
##    h,  w = img.shape[:2]
##    newcameramtx, roi = cv.getOptimalNewCameraMatrix(inner_matrix, dist, (w,h), 1, (w,h), True)
##    img = cv.undistort(img, inner_matrix, dist, None, newcameramtx)
    
##    img_resize = cv.resize(img,(1280,720))
##    cv.imshow("pic", img_resize)
##    cv.waitKey(0)
##    cv.destroyAllWindows()
    
    ''' crop '''
    crop_size = 0
    crop = img.copy()
##    crop = crop[hole_y_min+crop_size:hole_y_max-crop_size, hole_x_min+crop_size:hole_x_max-crop_size]
    # crop_resize = cv.resize(crop,(1280,720))
    # cv.imshow("pic", crop_resize)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.cvtColor(crop, cv.COLOR_BGR2HSV)
    
    base_hsv = []
    hsv_txt = 'config/hsv.txt'
    if not Path(hsv_txt).exists():
      center = hsv[360][640]
      with open(hsv_txt, 'w') as f:
        for i in range(len(center)):
          base_hsv.append(center[i])
          f.write(f'{base_hsv[i]}\n')
    else:
      with open(hsv_txt, 'r') as f:
        lines = f.readlines()
        for i in range(3):
          base_hsv.append(int(lines[i].strip('\n')))
          
    print(base_hsv)
    lower_green = np.array([base_hsv[0]-25, base_hsv[1]-80, base_hsv[2]-100]) #50,70,0
    higher_green = np.array([base_hsv[0]+25, base_hsv[1]+80, base_hsv[2]+100]) #200,255,255
    mask = cv.inRange(hsv, lower_green, higher_green)
    # cv2_imshow(mask)
    result = cv.bitwise_and(crop, crop, mask=mask)
    result = crop - result
    # print(result)
    # img_resize = cv.resize(result,(1280,720))
    # cv.imshow('green filter', img_resize)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    mask = cv.imread('mask.png')
    final = cv.bitwise_and(img, mask)
    img_resize = cv.resize(final,(1280,720))
    cv.imshow('final', img_resize)
    cv.waitKey(500)
    cv.destroyAllWindows()
    """# Find 6 holes"""
    hough(img, final, 95, 90, 10, 45, 55, boundary, hole)
##    hough(img, result, 100, 200, 10, 45, 55, boundary, hole)

#findBall()
