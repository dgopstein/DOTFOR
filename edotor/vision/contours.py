#!/usr/bin/env python3

import numpy as np
import cv2
import imutils
import sklearn
import math
import itertools
import scipy

import img_util

# https://stackoverflow.com/questions/36982736/how-to-crop-biggest-rectangle-out-of-an-image

img_path = '/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150752.jpg'
image = scale(cv2.imread(img_path),.3)


showImage(image)
destroyWindowOnKey()

#image_y,_,_ = yuv_img(image)

_, image_y, _ = hsv_img(image)

image_blurred = cv2.GaussianBlur(image_y,(3,3),0)
edges = cv2.Canny(image_blurred,100,300,apertureSize = 3)
cnt_img,contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#for cnt in contours[0:1]:
#    hull = cv2.convexHull(cnt)
#    simplified_cnt = cv2.approxPolyDP(hull,0.001*cv2.arcLength(hull,True),True)
#    print(simplified_cnt)

out_img = image.copy()
for cnt in contours:
    hull = cv2.convexHull(cnt)
    simplified_cnt = cv2.approxPolyDP(hull,0.0001*cv2.arcLength(hull,True),True)
    cv2.drawContours(out_img, simplified_cnt, -1, (0, 255, 0), thickness=4)

showImage(out_img)
showImage(image)
destroyWindowOnKey()
