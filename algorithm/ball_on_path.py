# -*- coding: utf-8 -*-
"""
Created on Sat May  1 21:47:15 2021

@author: asus

1. 計算白球至普通球的軌跡上是否有障礙物
2. 計算普通球至洞口的軌跡上是否有障礙物

"""


def ball_on_path(white, ball, hole, ball_list, target):
    from algorithm import get_distance_from_point_to_line
    
    distance1, distance2 = 1000, 1000
    # ball_d = 31.35
    ball_d = 100
    offset = ball_d*2/3 # 判斷球是否在路徑上，考慮求半徑所以擴大搜索範圍
    flag = True
    for block in ball_list:
        if(block[0]!=ball[0] and block[1]!=ball[1]):
            if (block[0] <= max(ball[0], hole[0])+offset and block[0] >= min(ball[0], hole[0])-offset and block[1] <= max(ball[1], hole[1])+offset and block[1] >= min(ball[1], hole[1])-offset): 
                ''' block to line between hole and ball '''
                distance1 = get_distance_from_point_to_line.point_to_line_distance(block, ball, hole)
            if (block[0] <= max(white[0], target[0])+offset and block[0] >= min(white[0], target[0])-offset and block[1] <= max(white[1], target[1])+offset and block[1] >= min(white[1], target[1])-offset):
                ''' block to line between white and ball '''
                distance2 = get_distance_from_point_to_line.point_to_line_distance(block, white, target)
            
            ''' distance > ball_d ? '''
            if(distance1<=ball_d or distance2<=ball_d):
                flag = False
                break
        else:
            continue
    
    return flag
