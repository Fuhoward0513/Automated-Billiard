# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:20:49 2021

@author: asus

主程式 --> 輸入 c 重複執行程式，輸入其他字元則停止程式

"""

import align_depth2color
from ball_detection import detect_ball
from ball_detection import findHole_new
from ball_detection import hough_circle_test
from algorithm import hit_ball_strategy
from coordinate_transformation import coordinate_transformation
import test_undistort

"""### Imports"""
import numpy as np
import tensorflow as tf

"""Import the object detection module."""

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util

""" Import function file . """
import cv2
import os
import pathlib

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
"""Patches:"""
# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

#抓當前資料夾
current_dir = os.getcwd()
#print(current_dir)

"""# Detection

Load an object detection model:
"""
PATH_TO_FROZEN_GRAPH = current_dir + '/ball_detection/saved_model/frozen_inference_graph.pb'
PATH_TO_LABELS = current_dir + '/ball_detection/saved_model/labelmap.pbtxt'

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.compat.v1.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

print("load model sucessfully!")

'''Loading label map'''
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

print("load label map sucessfully!")
#detection_model = tf.saved_model.load(current_dir + '/ball_detection/saved_model')

# In[]
while True:
    flag = input("Continue: press c\n")
    if(flag == 'c'):
        ''' take color img align with depth img '''
        align_depth2color.take_pic()
        print('save img successfully !')

        ''' undistort color img and depth img '''
        test_undistort.undistort()
        print('undistort successfully !')

        ''' hole detection '''
        findHole_new.findHole()
        print('find holes successfully !')
        
        ''' ball detection '''
        # detect_ball.detect_ball(detection_graph) # apply AI object dectection
        hough_circle_test.findBall()
        print('ball coordinates detected !')

        ''' hit ball strategy '''
        num_ball, isConvex = hit_ball_strategy.hit_ball_strategy()
        print('Apply strategy Successfully')

        ''' coordinates transformation '''
        if num_ball:
            coordinate_transformation.coordinate_transformation(num_ball, isConvex)
            print('Result get !!!!')
    else:
        break
    
