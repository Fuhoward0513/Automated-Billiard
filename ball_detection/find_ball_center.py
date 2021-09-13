# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 16:08:25 2021

@author: fuhow
"""
import math
import os
import cv2
from ball_detection import image_preprocessing
import numpy as np

current_dir = os.getcwd()


def find_ball_center(ball_class, cordinate, image_path, result_path, count, pic_num):
    
    """ [y_min, x_min, y_max, x_max] """
    pic_width = 1920
    pic_height = 1080
    
    """ 稍微放大框框 """
    expansion = 5
    y_min = int(cordinate[0] * pic_height)-expansion
    x_min = int(cordinate[1] * pic_width)-expansion
    y_max = math.ceil(cordinate[2] * pic_height)+expansion
    x_max = math.ceil(cordinate[3] * pic_width)+expansion
    
    """ crop """
    image_path = str(image_path)
    image = cv2.imread(image_path)
    result = cv2.imread(result_path)
    
    ball_crop = image[y_min:y_max, x_min:x_max]
    #cv2.imwrite("D:/ball_detection\test_cordinate\result2\crop_{}.png".format(count), ball_crop)
    # cv2.imshow("my_crop",ball_crop)
    # cv2.waitKey(300)
    # cv2.destroyAllWindows()
    
    """ image preprocessing """
    pic = image_preprocessing.image_preprocess(ball_crop)
    
    """ hough circle """
    pic = cv2.medianBlur(pic, 5)
    # pic = cv2.GaussianBlur(pic, (1, 1), 0)
    rows = pic.shape[0]
    center_result = np.array([0, 0]);
    circles = cv2.HoughCircles(pic, cv2.HOUGH_GRADIENT, 1, rows, param1=100, param2=10, minRadius=40, maxRadius=50)
    print(circles.shape)
    print(rows)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0]+x_min, i[1]+y_min)
            center_result = np.asarray(center)
            # print(center)
            # circle center
            cv2.circle(result, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            
            if ball_class == 1:
                cv2.circle(result, center, radius, (255, 0, 255),3)
            else:
                cv2.circle(result, center, radius, (255, 0, 0),3)
            
    temp = cv2.resize(result, (1280, 720))
    cv2.imwrite(result_path, result)
    cv2.imshow('detected circles', temp)
    cv2.waitKey(300)
    cv2.destroyAllWindows()
    
    return center_result
    
    
    
    
    
    
