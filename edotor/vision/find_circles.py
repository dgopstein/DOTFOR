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

orig_image = loadImage(card_regions[46]['file'])

image = imutils.resize(orig_image, width=600)

hue, sat_orig, val = hsv_img(image)

sat = cv2.blur(sat_orig,(3,3),0)

hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .5, 10,
                                    param1=9,
                                    param2=20,
                                    #minRadius=10,
                                    #maxRadius=35
                                    minRadius=2,
                                    maxRadius=15
)
circles = np.round(hough_circles[0, :]).astype("int")
print("finished detecting circles: ", len(circles))

displayCircles(sat, circles)
