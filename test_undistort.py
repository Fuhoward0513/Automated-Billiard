'''
undistort 影像，以校正影像崎變
'''
import numpy as np
import cv2 as cv

def undistort():
    inner_matrix = np.loadtxt('eye_hand/config/L515/self_inner_matrix_charuco_1920_30張.txt')
    dist = np.loadtxt('eye_hand/config/L515/self_distortion_charuco_1920_30張.txt')

    fname = 'color.png'
    img = cv.imread(fname)
    depth_img = np.load('config/depth.npy')
    depth_img = depth_img.T
    print('distort: ', depth_img.shape)

    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(inner_matrix, dist, (w,h), 1, (w,h), True)
    inverse_inner_matrix = np.linalg.inv(newcameramtx)
    img = cv.undistort(img, inner_matrix, dist, None, newcameramtx)
    depth_img = cv.undistort(depth_img, inner_matrix, dist, None, newcameramtx)
    print('undistort: ', depth_img.shape)
    
    depth_img = depth_img.T
    cv.imwrite('color.png', img)
    np.save('config/depth', depth_img)


