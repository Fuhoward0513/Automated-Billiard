# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:35:42 2021

@author: fuhow
"""

"""### Imports"""

import numpy as np
from PIL import Image
import os
import cv2 as cv
"""Import the object detection module."""

from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util

""" Import function file . """

from ball_detection import run_inference_for_single_image

current_dir = os.getcwd()
PATH_TO_LABELS = current_dir + '/ball_detection/labelmap.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def show_inference(model, image_path, pic_num):
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  image_np = np.array(Image.open(image_path))
  # Actual detection.
  output_dict = run_inference_for_single_image.run_inference_for_single_image(model, image_path)
  # output_dict = run_inference_for_single_image.run_inference_for_single_image(model, image_np)
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks_reframed', None),
      use_normalized_coordinates=True,
      line_thickness=4)
  Image.fromarray(image_np).save(current_dir + f'/AI/{pic_num}.png')
  img = cv.imread(f'AI/{pic_num}.png')
  cv.imshow('img', cv.resize(img, (1280, 720)))
  cv.waitKey(0)
  cv.destroyAllWindows()
  print('save pictue:', pic_num)
  
  return 0

  count = 0
  for j in output_dict['detection_scores']:
      if(j >= 0.7):
          print("score{}: ".format(count), j)
          print("cordinate{}: ".format(count), output_dict['detection_boxes'][count])
          
          if(output_dict['detection_classes'][count] == 1):
              print("type: ball")
          elif(output_dict['detection_classes'][count] == 2):
              print("type: white-ball")
          elif(output_dict['detection_classes'][count] == 3):
              print("type: nine-ball")