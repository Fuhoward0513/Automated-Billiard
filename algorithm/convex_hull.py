# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:14:32 2021

@author: asus

若出現沒有解的情況則會使用 convex_hull 功能
1. 找出檯面上普通球的 convex_hull
2. 找出 convex_hull 之重心位置，作為白球撞擊目標
"""

import cv2 as cv

def convex_hull(ball):
    hull = cv.convexHull(ball)
    print(hull)
    
    moment = cv.moments(hull)
    # print(moment)
    
    cx = moment['m10'] / (moment['m00'] + 1e-5)
    cy = moment['m01'] / (moment['m00'] + 1e-5)
    # print(cx)
    # print(cy)
    
    img = cv.imread('color.png')
    for i in ball:
        cv.circle(img,(i[0], i[1]),5,(0,0,255),-1)
    cv.circle(img, (int(cx), int(cy)),5,(0,255,0),-1)

    img_resize = cv.resize(img, (1280,720))
    cv.imshow('img', img_resize)
    cv.waitKey(500)
    cv.destroyAllWindows()
    if(len(ball)==1):
        return ball[0][0], ball[0][1]
    elif(len(ball)==2):
        return ball[0][0], ball[0][1]
    else:
        return int(cx), int(cy)
    
