# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 16:41:50 2020

@author: fuhow
以 Faster RCNN 所訓練出來的模型進行 Object Detection
註: 較不穩定
"""
"""### Imports"""
import numpy as np
import tensorflow as tf

"""Import the object detection module."""

from object_detection.utils import ops as utils_ops

""" Import function file . """

from ball_detection import show_inference
from ball_detection import find_ball_center
from ball_detection import run_inference_for_single_image
import cv2
import os
import pathlib


def detect_ball(detection_model):
    
    
    # """Patches:"""
    
    # # patch tf1 into `utils.ops`
    # utils_ops.tf = tf.compat.v1
    
    # # Patch the location of gfile
    # tf.gfile = tf.io.gfile
    
    # #抓當前資料夾
    # current_dir = os.getcwd()
    # #print(current_dir)
    
    # """# Detection
    
    # Load an object detection model:
    # """
    # detection_model = tf.saved_model.load(current_dir + '/ball_detection/saved_model')
    # print("load weight sucessfully")
    
    # In[]
    
    # If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
    PATH_TO_TEST_IMAGES_DIR = pathlib.Path('')
    TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.png")))
    print("load detection pics sucessfully!")
    
##    """Check the model's input signature, it expects a batch of 3-color images of type uint8:"""
##    
##    print(detection_model.signatures['serving_default'].inputs)
##    
##    """And returns several outputs:"""
##    
##    detection_model.signatures['serving_default'].output_dtypes
##    
##    detection_model.signatures['serving_default'].output_shapes
    
    """Run it on each test image and show the results:"""    
    
    
    """主程式 """
    
    """ write file """
    txtname_white = 'config/white_pixel.txt'
    txtname_ball = 'config/ball_pixel.txt'
    
    with open(txtname_white, 'w') as f:
        f.write('')
    with open(txtname_ball, 'w') as f:
        f.write('')
    
    """ read image """
    pic_num = 0
    image_path = 'color.png'
    # for image_path in TEST_IMAGE_PATHS:
        
    # 辨識結果存取路徑
    result_path = f'result/result_{pic_num}.png'
    cv2.imwrite(result_path, cv2.imread(str(image_path)))
    
    
    # 辨識第幾張照片
    print("picture{}: ".format(pic_num))
    
    # 找出Faster RCNN 分數、類別
    output_dict = run_inference_for_single_image.run_inference_for_single_image(detection_model, image_path)
    
    # FasterRCNN 視覺化
    show_inference.show_inference(detection_model, image_path, pic_num)
    
    # 若分數高於 50 進行霍夫找圓
    ball_count = 0
    center_result = np.array([])
    white_center = np.array([])
    
    for j in output_dict['detection_scores']:
        if(j >= 0.7):
            print("score{}: ".format(ball_count), j)
            print("cordinate{}: ".format(ball_count), output_dict['detection_boxes'][ball_count])
            ball_class = output_dict['detection_classes'][ball_count]
            if(ball_class == 1):
                print("type: ball")
                #用hough circle找球心座標
                center = find_ball_center.find_ball_center(ball_class, output_dict['detection_boxes'][ball_count], image_path, result_path, ball_count, pic_num)
                center_result = np.append(center_result, center, axis=0)
                # 寫txt
                X = center[0]
                Y = center[1]
                with open(txtname_ball, 'a') as f:
                    f.write(f'{X}\t{Y}\n')
                    
            elif(ball_class == 2):
                continue
            
                print("type: white-ball")
                #用hough circle找球心座標
                center = find_ball_center.find_ball_center(ball_class, output_dict['detection_boxes'][ball_count], image_path, result_path, ball_count, pic_num)
                white_center = np.append(white_center, center, axis=0)
                # 寫txt
                X = center[0]
                Y = center[1]
                with open(txtname_white, 'a') as f:
                    f.write(f'{X}\t{Y}\n')
            
        ball_count = ball_count + 1
    
    center_result = center_result.reshape(int(len(center_result)/2), 2)
    # print("ball: \n", center_result)
##        print("white ball: \n", white_center)
    # pic_num = pic_num + 1
