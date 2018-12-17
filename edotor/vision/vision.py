#!/usr/bin/env python3

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity

# https://medium.com/@manivannan_data/resize-image-using-opencv-python-d2cdbbc480f0
def scale(oriimg, imgScale):
    height, width, depth = oriimg.shape
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv2.resize(oriimg,(int(newX),int(newY)))
    return newimg

def showImage(img):
    cv2.waitKey(0)
    cv2.imshow('image', img)

def destroyWindowOnKey():
    cv2.destroyAllWindows()
    cv2.waitKey(1)

orig_img = cv2.imread('/Users/dgopstein/dotfor/edotor/vision/shadowy_buttons.jpg')
img = scale(orig_img, .3)

hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

hsv_channels = cv2.split(hsv);

sat = hsv_channels[1]
cv2.imshow('image', img)
showImage(sat)
destroyWindowOnKey()


# find circles

def findCircles():
    hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .8, 25,
                            param1=5,
                            param2=50,
                            #minRadius=10,
                            #maxRadius=35
                            minRadius=10,
                            maxRadius=40
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

circles = findCircles()
displayCircles(circles)
destroyWindowOnKey()

# most common radius (plus or minus a gaussian kernel)
def radiiMode(circles):
    estimated_radius = 25
    max_radius_px = estimated_radius * 4
    bandwidth = estimated_radius / 5
    radii = circles[:, 2]
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth).fit(radii[:, np.newaxis])
    x_grid = np.linspace(0, max_radius_px, radii.shape[0])
    pdf = np.exp(kde.score_samples(x_grid[:, np.newaxis]))
    #fig, ax = plt.subplots()
    #ax.plot(x_grid, pdf, label="hello")
    #plt.show()
    return x_grid[np.argmax(pdf)]

def distMode(circles):
    estimated_dist = 150
    max_dist = estimated_dist * 5
    bandwidth = estimated_dist / 5
    crossproduct = [(c1, c2) for c1 in circles for c2 in circles]
    dists = np.array([circle_dist(c1, c2) for (c1, c2) in circle_crossproduct])
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth).fit(dists[:, np.newaxis])
    x_grid = np.linspace(0, max_dist, dists.shape[0])
    pdf = np.exp(kde.score_samples(x_grid[:, np.newaxis]))
    fig, ax = plt.subplots()
    ax.plot(x_grid, pdf, label="hello")
    plt.show()
    return x_grid[np.argmax(pdf)]

def circle_dist(c1, c2):
    return np.linalg.norm(c2-c1)

hist(circle_dists, 200)
