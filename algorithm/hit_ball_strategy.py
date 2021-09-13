# -*- coding: utf-8 -*-
"""
Created on Sat May  1 19:40:31 2021

@author: asus

1. 讀取白球、洞口、普通球的 pixel 座標值
2. 對每個求計算進洞路徑
3. 選取最佳路徑(考慮撞擊角度、普通球離洞口距離、白球與普通球距離)，並寫入 'config/result.txt'

"""
import numpy as np

def hit_ball_strategy():
    from algorithm import ball_on_path
    from algorithm import calculate_alpha
    from algorithm import convex_hull
    from algorithm import cal_height
    
    ''' load white ball pixel '''
    with open('config/white_pixel.txt', 'r') as f:
        white = f.readline()
        white = white.split()
        white = np.array(white).astype(int)
    
    
    ''' load ball pixel '''
    with open('config/ball_pixel.txt', 'r') as f:
        ball = list()
        for i in f:
            ball.append(i.split())
        ball = np.array(ball).astype(int)
    
    ''' Load hole pixel '''
    with open('config/hole.txt', 'r') as f:
        hole = list()
        for i in f:
            hole.append(i.split())
        hole = np.array(hole).astype(int)
    hole = sorted(hole, key = lambda Hole: Hole[0])
    left_offset = np.sign(hole[1][1] - hole[0][1]) * 40
    hole[0][0] += abs(left_offset) * np.cos(np.pi/4)
    hole[1][0] += abs(left_offset) * np.cos(np.pi/4)
    hole[0][1] += left_offset * np.cos(np.pi/4)
    hole[1][1] -= left_offset * np.cos(np.pi/4)
    
    right_offset = np.sign(hole[5][1] - hole[4][1]) * 40
    hole[4][0] -= abs(right_offset) * np.cos(np.pi/4)
    hole[5][0] -= abs(right_offset) * np.cos(np.pi/4)
    hole[4][1] += right_offset * np.cos(np.pi/4)
    hole[5][1] -= right_offset * np.cos(np.pi/4)
    
    mid_offset = np.sign(hole[3][1] - hole[2][1]) * 30
    hole[2][1] += mid_offset
    hole[3][1] -= mid_offset
    if(len(ball)==0):
        print("there is no ball")
        return 0, False
    
    ''' algorithm '''
    
    ''' 初步篩選可以打進的球 '''
    best_result = list() # [white, ball, hole, target]
    result = list()
    alpha_weight = -1.5
    distance_weight = -1    
    ''' 
    1.  找出最好的球 
        權重 -> alpha = -1, distance = -1
    2. 若找不到解，covex hull 找重心打
    '''
    for i in ball:
        for j in hole:
            # 算 alpha 與軌跡上是否有球
            alpha, target = calculate_alpha.calculate_alpha(white, i, j)
            # print('alpha', alpha)
            flag = ball_on_path.ball_on_path(white, i, j, ball, target)
            
            # 設定alpha要小於多少才可以算進去
            if(alpha<80 and flag==True):
                d_ball_to_hole = np.sqrt((i[0]-j[0])**2 + (i[1]-j[1])**2)
                d_white_to_ball = np.sqrt((i[0]-white[0])**2 + (i[1]-white[1])**2)
                temp = [white, i, j, target, alpha*alpha_weight + d_white_to_ball*distance_weight + d_ball_to_hole*distance_weight]
                result.append(temp)
    result = np.array(result)
    # print(result)
    
    isConvex = False
    if(len(result)!=0):
        result = sorted(result, key = lambda result: result[-1])
        best_result = result[-1]
        print("best result:", best_result)
    else:
        # center_result = list()
        cx, cy = convex_hull.convex_hull(ball)
        centroid = np.array([cx, cy])
        # print(centroid)
        # for i in hole:
        #     alpha, target = calculate_alpha.calculate_alpha(white, centroid, i)
        #     if(alpha<90):
        #         center_result.append([white, centroid, i, centroid, alpha])
        # center_result = sorted(center_result, key = lambda center_result: center_result[-1])
        # best_result = center_result[-1]
        best_result = [white, centroid, centroid, centroid]
        isConvex = True
        print("best result:", best_result)
    
    #calculate height
    flag_height = cal_height.cal_height(white, ball, hole)
    ''' write file '''
    txtname = 'config/result.txt'
    with open(txtname, 'w') as f:
        f.write('')
    for i in range(4): # [white, ball, hole, target]
        X = best_result[i][0]
        Y = best_result[i][1]
        with open(txtname, 'a') as f:
            f.write(f'{X}\t{Y}\n')
    with open(txtname, 'a') as f: # 是否抬高 flag
            f.write(f'{flag_height}')
    
    return len(ball), isConvex
    

        
        
