#!/usr/bin/env python3

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity
from sklearn.metrics import mean_squared_error
import scipy
import scipy.signal
import math
import imutils

import img_util


def loadImage(path):
    return cv2.imread(path, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)

card_regions = loadCardRegions()

orig_image = loadImage(card_regions[13]['file'])

image = imutils.resize(orig_image, width=400)
height, width, depth = image.shape

blurred = cv2.blur(image,(3,3),0)

hue, sat, val = hsv_img(blurred)

hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .5, 10,
                                    param1=10,
                                    param2=20,
                                    minRadius=2,
                                    maxRadius=15)
circles = np.round(hough_circles[0, :]).astype("int")
print("finished detecting circles: ", len(circles))

displayCircles(image, circles)
destroyWindowOnKey()

radius_mode = radiiMode(circles)
#hist(circles[:,2], 100)

# make a binary image in which each pixel indicates
# if it's within the radius of a circle
def circleBinImage(circles):
    bw = np.zeros((height,width,1), np.uint8)
    for c in circles:
        cv2.circle(bw,(c[0],c[1]),1,255,thickness=cv2.FILLED)
    return bw

angle_mode = angleMode(circles)

sized_cs = circles[np.where(np.logical_and(circles[:,2]>=.7*radius_mode, circles[:,2]<=1.3*radius_mode))]

len(circles)
len(sized_cs)
displayCircles(sat, circles)
displayCircles(sat, sized_cs)
destroyWindowOnKey()

def buttonPos(col, row, radius):
    x = (col + int(col/3)) * 2*radius
    y = row * 2*radius
    return np.array([x, y], np.uint32)

def grid_dist(scale_xoff_yoff):
    print(scale_xoff_yoff)
    transformed_grid = transform_grid(*scale_xoff_yoff)
    #displayCircles(image, transformed_grid.astype(np.uint32), ring=False)

    nearest_points = np.array(correspondence(transformed_grid, sized_cs[:,0:2]))
    a, b = zip(*nearest_points)
    return math.sqrt(mean_squared_error(a, b))

def transform_grid(scale, xoff, yoff):
    basic_grid = np.array([buttonPos(col, row, radius_mode) for col in list(range(0, 12)) for row in range(0, 6)])

    rot_grid = np.inner(basic_grid, rotation2d(0))

    transformed_grid = rot_grid * scale + [xoff, yoff]
    return transformed_grid



min_x, min_y, min_radius = np.amin(sized_cs, 0)

(min_x, min_y)
scipy.optimize.minimize(grid_dist, [0, min_x, min_y])
displayCircles(image, transform_grid(affine_mat).astype(np.uint32), ring=False)


grid_dist([-.04, 1.65, min_x, min_y])
displayCircles(image, sized_cs)
displayCircles(image, transform_grid( 12.04206595,   1.88847251,  92.13644901, 126.09508901).astype(np.int), ring=False)
