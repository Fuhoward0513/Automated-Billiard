# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 19:22:57 2021

@author: fuhow
"""

import cv2

def image_preprocess(ball_crop):
    
    """ gray """
    gray_img = cv2.cvtColor(ball_crop, cv2.COLOR_BGR2GRAY)
    temp = cv2.resize(gray_img, (1280, 720))
    cv2.imshow('gray pic', temp)
    cv2.waitKey(200)
    cv2.destroyAllWindows()
    
    """equalizing the contrast """
    gray_img_eqhist=cv2.equalizeHist(gray_img)
    temp = cv2.resize(gray_img_eqhist, (1280, 720))
    cv2.imshow('gray_img_eqhist pic', temp)
    cv2.waitKey(200)
    cv2.destroyAllWindows()
    
    """ CLAHE """
    # clahe=cv2.createCLAHE(clipLimit=40)
    # gray_img_clahe=clahe.apply(gray_img_eqhist)
    # temp = cv2.resize(gray_img_clahe, (1280, 720))
    # cv2.imshow('gray_img_clahe pic', temp)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    """ optimal """
    # th=50
    # max_val = 255
    # ret, o3 = cv2.threshold(gray_img_clahe, th, max_val, cv2.THRESH_TOZERO)
    # temp = cv2.resize(o3, (1280, 720))
    # cv2.imshow('threshold pic', temp)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # o3 = gray_img
    
    o3 = gray_img_eqhist
    return o3
    
    




