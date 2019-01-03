#!/usr/bin/env python3

import numpy as np
import cv2
import imutils
import sklearn
import math

# https://github.com/Aqsa-K/Car-Number-Plate-Detection-OpenCV-Python/blob/master/CarPlateDetection.py

def scale(oriimg, imgScale):
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv2.resize(oriimg,(int(newX),int(newY)))
    return newimg

def imshow(title, img):
    cv2.waitKey(1)
    cv2.imshow(title, img)

def showImage(img):
    imshow('img', img)

def destroyWindowOnKey():
    cv2.destroyAllWindows()
    cv2.waitKey(1)

def hsv_img(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_channels = cv2.split(hsv);
    return hsv_channels

def invert(gray):
    return 255-gray

def dilate_erode(img, kern = (2,2), iters=10):
    kernel = np.ones(kern,np.uint8)
    dilated = cv2.dilate(img,kernel,iterations = iters)
    eroded = cv2.erode(dilated,kernel,iterations = iters)
    return eroded

def blur(img):
    return cv2.GaussianBlur(img, (9, 9), 0)

def drawLines(in_img, lines, labels=[]):
    img = in_img.copy()
    idx = -1
    for rho,theta in lines:
        idx += 1
        label = labels[idx]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2000*(-b))
        y1 = int(y0 + 2000*(a))
        x2 = int(x0 - 2000*(-b))
        y2 = int(y0 - 2000*(a))

        color = [0,0,255]
        if len(labels) == len(lines):
            off = 50*label
            color = [int((0+off)%255), int((100+2*off)%255), int((200+3*off)%255)]

        print("color: ", color)
        cv2.line(img,(x1,y1),(x2,y2),color=color,thickness=2)
    return img


###########################################################################
# https://stackoverflow.com/questions/2992264/extracting-a-quadrilateral-image-to-a-rectangle
###########################################################################

def warpImage(image, corners, target):
    mat = cv.CreateMat(3, 3, cv.CV_32F)
    cv.GetPerspectiveTransform(corners, target, mat)
    out = cv.CreateMat(height, width, cv.CV_8UC3)
    cv.WarpPerspective(image, out, mat, cv.CV_INTER_CUBIC)
    return out

if __name__ == '__main__':
    width, height = 400, 250
    corners = [(171,72),(331,93),(333,188),(177,210)]
    target = [(0,0),(width,0),(width,height),(0,height)]
    image = cv.LoadImageM('fries.jpg')
    out = warpImage(image, corners, target)
    cv.SaveImage('fries_warped.jpg', out)

###########################################################################





img_path = '/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150759.jpg'
sat = loadScaledSat('/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150759.jpg')

destroyWindowOnKey()
showImage(sat)

image = imutils.resize(cv2.imread(img_path), width=1000)

# Display the original image
#imshow("Original Image", image)
#destroyWindowOnKey()

hue, sat, val = hsv_img(image)
val_sat = np.array((invert(sat)/255.0*val/255.0)*255, np.uint8)
val_sat_thresh = cv2.threshold(val_sat,100,255,cv2.THRESH_BINARY)[1]
showImage(val_sat)
showImage(val_sat_thresh)
destroyWindowOnKey()
# black (low) sat
# white (val) sat


# RGB to Gray scale conversion
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray=val_sat.copy()
#imshow("1 - Grayscale Conversion", gray)
#destroyWindowOnKey()

# Noise removal with iterative bilateral filter(removes noise while preserving edges)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
#imshow("2 - Bilateral Filter", gray)
#destroyWindowOnKey()

# Find Edges of the grayscale image
edged = cv2.Canny(gray, 170, 200)
imshow("4 - Canny Edges", edged)
destroyWindowOnKey()

lines = cv2.HoughLines(edged,rho=1,theta=np.pi/180,threshold=150)
flat_lines = lines.reshape(lines.shape[0], lines.shape[2])

# only look at theta (angle) and mod by the quadrant to search for
# rectangular things. This works since parallel lines already have
# the same angle, and perpendicular lines will have the same angle
# once modded by 90 degrees (pi/2 radians)
quad_angles = flat_lines[:,1].reshape(-1,1) % (math.pi/2)
quad_clustering = sklearn.cluster.MeanShift(bandwidth=(math.pi/40)).fit(quad_angles)

# select the lines that form the best box
# (assumes the 0th cluster is the strongest)
boundary_lines = np.array([line for (line, label) in zip(flat_lines, quad_clustering.labels_) if label == 0])

# make sure the angles and intercepts are comparable
# (normally they have very different domains)
scaled_boundaries = sklearn.preprocessing.MinMaxScaler(copy=True, feature_range=(0, 1)).fit(boundary_lines).transform(boundary_lines)

# we already have all the boundary lines
# now determine which ones are for which edge
cardinal_clustering = sklearn.cluster.MeanShift(bandwidth=.05).fit(scaled_boundaries)
boundaries = cardinal_clustering.cluster_centers_
showImage(drawLines(image, boundary_lines, labels=cardinal_clustering.labels_))
destroyWindowOnKey()
