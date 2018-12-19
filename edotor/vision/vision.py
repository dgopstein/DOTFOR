#!/usr/bin/env python3

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity
import scipy.signal as signal
import math

# https://medium.com/@manivannan_data/resize-image-using-opencv-python-d2cdbbc480f0
def scale(oriimg, imgScale):
    height, width, depth = oriimg.shape
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv2.resize(oriimg,(int(newX),int(newY)))
    return newimg

def showImage(img):
    cv2.waitKey(1)
    cv2.imshow('image', img)

def destroyWindowOnKey():
    cv2.destroyAllWindows()
    cv2.waitKey(1)

def loadScaledSat(img_path):
    orig_img = cv2.imread(img_path)
    img = scale(orig_img, .3)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_channels = cv2.split(hsv);
    sat = hsv_channels[1]
    return sat

def findCircles(sat):
    hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .8, 25,
                            param1=5,
                            param2=50,
                            #minRadius=10,
                            #maxRadius=35
                            minRadius=5,
                            maxRadius=55
    )
    circles = np.round(hough_circles[0, :]).astype("int")
    print("finished detecting circles: ", len(circles))
    return circles

def displayCircles(circles):
    output = sat.copy()

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 5, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    showImage(np.hstack([sat, output]))
    print("closed window")

def hist(np_data, bins=20):
    hist = pd.DataFrame(np_data).plot.hist(grid=True, bins=bins, rwidth=0.9, color='#607c8e')
    hist.plot()
    plt.show()

# most common radius (plus or minus a gaussian kernel)
def radiiMode(circles):
    estimated_radius = 25
    max_radius_px = estimated_radius * 4
    bandwidth = estimated_radius / 5
    radii = circles[:, 2]
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth, atol=0.01, rtol=0.01).fit(radii[:, np.newaxis])
    x_grid = np.linspace(0, max_radius_px, radii.shape[0])
    pdf = np.exp(kde.score_samples(x_grid[:, np.newaxis]))
    #fig, ax = plt.subplots()
    #ax.plot(x_grid, pdf, label="hello")
    #plt.show()
    return x_grid[np.argmax(pdf)]

def angle(c1, c2):
    (x1, y1, r1) = c1
    (x2, y2, r3) = c2
    return math.degrees(math.atan2(y1-y2, x2-x1))

def angleMode(circles):
    bandwidth = 1
    crossproduct = [(c1, c2) for c2 in circles for c1 in circles if c2[1] < c1[1]]
    angles = np.array([angle(c1, c2) for (c1, c2) in crossproduct])
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth).fit(angles[:, np.newaxis])
    x_grid = np.linspace(0, 180, 200)
    pdf = np.exp(kde.score_samples(x_grid[:, np.newaxis]))

    peaks, props = signal.find_peaks(pdf)
    signal.peak_prominences(pdf, peaks)

    fig, ax = plt.subplots()
    ax.plot(x_grid, pdf, label="hello")
    plt.show()
    return x_grid[np.argmax(pdf)]

sat = loadScaledSat('/Users/dgopstein/dotfor/edotor/vision/shadowy_buttons.jpg')
tilted_sat = loadScaledSat('/Users/dgopstein/dotfor/edotor/vision/shadowy_buttons_tilted_35.jpg')

#showImage(np.hstack([sat, tilted_sat]))
#destroyWindowOnKey()

sat_circles = findCircles(sat)
tilted_circles = findCircles(tilted_sat)

radiiMode(sat_circles)
radiiMode(tilted_circles)

angleMode(sat_circles)
angleMode(tilted_circles)

#output = sat.copy()
#x1 = 100
#y1 = 200
#x2 = 10
#y2 = 300
#cv2.circle(output, (x1, y1), 10, (0, 5, 0), 4)
#cv2.circle(output, (x2, y2), 10, (100, 100, 100), 4)
#destroyWindowOnKey()
#showImage(output)

# Angles
#        90
#+/-180      0
#       -90
