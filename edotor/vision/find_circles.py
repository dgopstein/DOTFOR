#!/usr/bin/env python3

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity
import scipy
import scipy.signal
import math

import img_util


def loadImage(path):
    return cv2.imread(path, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)

card_regions = loadCardRegions()

orig_image = loadImage(card_regions[16]['file'])

image = imutils.resize(orig_image, width=400)
height, width, depth = image.shape

hue, sat_orig, val = hsv_img(image)

sat = cv2.blur(sat_orig,(3,3),0)

hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .5, 10,
                                    param1=10,
                                    param2=20,
                                    minRadius=2,
                                    maxRadius=15)
circles = np.round(hough_circles[0, :]).astype("int")
print("finished detecting circles: ", len(circles))

displayCircles(sat, circles)

radius_mode = radiiMode(circles)
#hist(circles[:,2], 100)

# make a binary image in which each pixel indicates
# if it's within the radius of a circle
def circleBinImage(circles):
    bw = np.zeros((height,width,1), np.uint8)
    for c in circles:
        cv2.circle(bw,(c[0],c[1]),1,255,thickness=cv2.FILLED)
    return bw

angleMode(circles)

sized_cs = circles[np.where(np.logical_and(circles[:,2]>=.8*radius_mode, circles[:,2]<=1.2*radius_mode))]

len(circles)
len(sized_cs)
displayCircles(sat, circles)
displayCircles(sat, sized_cs)
destroyWindowOnKey()

circle_bin = circleBinImage(sized_cs)
showImage(circle_bin)

lines = cv2.HoughLines(circle_bin,1,np.pi/180,9).reshape(-1, 2)
showImage(drawLines(image, lines))

line_angle_clusters = MeanShift(bandwidth=0.02).fit(lines[:,1].reshape(-1,1) % (math.pi/2))

cardinal_lines = lines_with_label_in(lines, line_angle_clusters.labels_, [0])

clustered_lines = cluster_2d(cardinal_lines, 0.02)

showImage(drawLines(image, clustered_lines))

print(lines)
print('done')
