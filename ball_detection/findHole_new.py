# -*- coding: utf-8 -*-
'''
找出撞球檯的洞口
1. 以綠色遮罩保留綠色範桌面範圍
2. opening 降躁
3. 用 Hough circle 找出洞口 pixel 座標
'''

import numpy as np
import cv2 as cv
from pathlib import Path

def findHole():
  
  """# Hough Circles"""
  def hough(img, minDist, p1, p2, minR, maxR):
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
    for i in circles[0,:]:
      # draw the outer circle
      cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),5)
      # draw the center of the circle
      cv.circle(cimg,(i[0],i[1]),5,(0,0,255),-1)
      # 寫洞txt
      X = i[0]
      Y = i[1]
      with open(txtname, 'a') as f:
        f.write(f'{X}\t{Y}\n')
    img_resize = cv.resize(cimg,(1280,720))
    cv.imshow('hole', img_resize)
    cv.waitKey(0)
    cv.destroyAllWindows()

  txtname = 'config/hole.txt'
  if Path(txtname).exists():
    return
  
  with open(txtname, 'w') as f:
      f.write('')
      
  """# Find table using green filter"""
  img = cv.imread('color.png')
  img_resize = cv.resize(img,(1280,720))
  cv.imshow("pic", img_resize)
  cv.waitKey(0)
  cv.destroyAllWindows()
  hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
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
  lower_green = np.array([base_hsv[0]-25, base_hsv[1]-80, base_hsv[2]-75]) #50,70,0
  higher_green = np.array([base_hsv[0]+25, base_hsv[1]+80, base_hsv[2]+75]) #200,255,255
  mask = cv.inRange(hsv, lower_green, higher_green)
  # cv2_imshow(mask)
  result = cv.bitwise_and(img,img,mask=mask)
  # print(result)
  img_resize = cv.resize(result,(1280,720))
  cv.imshow('green filter', img_resize)
  cv.waitKey(0)
  cv.destroyAllWindows()


  # """# Detect table edge"""
  # im = cv.imread('0_Color.png')
  imgray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
  ret, thresh = cv.threshold(imgray, 0, 100, 0)
  # cv2_imshow(thresh)
  contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[-2:]
  con = cv.drawContours(result.copy(), contours, -1, (255,255,255), -1)
  img_resize = cv.resize(con,(1280,720))
  cv.imshow('result', img_resize)
  cv.waitKey(0)
  cv.destroyAllWindows()
  kernel = np.ones((5,5),np.uint8)
  opening = cv.morphologyEx(con.copy(), cv.MORPH_OPEN, kernel)
  cv.imwrite('mask.png',opening)
  img_resize = cv.resize(opening,(1280,720))
  print(opening.shape)
  print(img.shape)
  cv.imshow('result', img_resize)
  cv.waitKey(0)
  cv.destroyAllWindows()
  # final = cv.bitwise_and(img, opening)
  # # cv.drawContours(result, contours, -1, 255, 3)
  # img_resize = cv.resize(final,(1280,720))
  # cv.imshow('final', img_resize)
  # cv.waitKey(0)
  # cv.destroyAllWindows()

  """# Find 6 holes"""
  hough(opening, 200, 30, 5, 60, 70)
##  hough(img, 50, 100, 20, 40, 60)

## findHole()
