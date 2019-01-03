#!/usr/bin/env python3

import numpy as np
import cv2
import imutils
import sklearn
import math
import itertools
import scipy

from sklearn.cluster import MeanShift
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

def drawPoints(in_img, points):
    out_image=in_img.copy()
    for pt in points:
        cv2.circle(out_image,(int(pt[0]),int(pt[1])),7,[255,0,0],thickness=7)

    return out_image

def drawLines(in_img, lines, labels=[]):
    img = in_img.copy()
    idx = -1
    for rho,theta in lines:
        idx += 1
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
            label = labels[idx]
            off = 50*label
            color = [int((0+off)%255), int((100+2*off)%255), int((200+3*off)%255)]

        cv2.line(img,(x1,y1),(x2,y2),color=color,thickness=2)
    return img


###########################################################################
# https://stackoverflow.com/questions/2992264/extracting-a-quadrilateral-image-to-a-rectangle
###########################################################################

def warpImage(image, corners, target):
    mat = cv2.CreateMat(3, 3, cv2.CV_32F)
    cv2.GetPerspectiveTransform(corners, target, mat)
    out = cv2.CreateMat(height, width, cv2.CV_8UC3)
    cv2.WarpPerspective(image, out, mat, cv2.CV_INTER_CUBIC)
    return out

###########################################################################


###########################################################################
# https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
###########################################################################
def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1
###########################################################################

#img_path = '/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150759.jpg'
img_path = '/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150752.jpg'

image = imutils.resize(cv2.imread(img_path), width=1000)

def lines_with_label_in(lines, labels, desired_labels):
    return np.array([line for (line, label) in zip(lines, labels) if label in desired_labels])

def eval_parametric(rho, theta, xs):
    ys = -(np.array(xs)*np.cos(theta) - rho) / np.sin(theta)
    return  np.array([list(pair) for pair in zip(xs, ys)]).reshape(-1,2)

def card_corners(image):
    hue, sat, val = hsv_img(image)
    val_sat = np.array((1.0*invert(sat)/255.0*val/255.0)*255*1, np.uint8)
    showImage(val)

    # Noise removal with iterative bilateral filter
    # (removes noise while preserving edges)
    gray = cv2.bilateralFilter(sat, 11, 17, 17)

    # Find Edges of the grayscale image
    edged = cv2.Canny(gray, 170, 200)
    showImage(edged)

    # Turn the observed edges into inferred lines
    lines = cv2.HoughLines(edged,rho=1,theta=np.pi/180,threshold=120)
    flat_lines = lines.reshape(lines.shape[0], lines.shape[2])

    #showImage(drawLines(image, flat_lines))

    # only look at theta (angle) and mod by the quadrant to search for
    # rectangular things. This works since parallel lines already have
    # the same angle, and perpendicular lines will have the same angle
    # once modded by 90 degrees (pi/2 radians)
    quad_angles = flat_lines[:,1].reshape(-1,1) % (math.pi/2)
    quad_clustering = MeanShift(bandwidth=(.05)).fit(quad_angles)

    # select the lines that form the best box
    # (assumes the 0th cluster is the strongest)
    quad_lines = lines_with_label_in(flat_lines, quad_clustering.labels_, [0])

    showImage(drawLines(image, quad_lines))

    #line_dists = quad_lines[:,0].reshape(-1,1)
    #line_dists
    #dist_clustering = MeanShift(bandwidth=(25)).fit(line_dists)
    #showImage(drawLines(image, dist_lines, dist_clustering.labels_))

    # make sure the angles and intercepts are comparable
    # (normally they have very different domains)
    boundary_scaler = sklearn.preprocessing.MinMaxScaler(copy=True, feature_range=(0, 1))
    scaled_boundaries = boundary_scaler.fit(quad_lines).transform(quad_lines)

    # we already have all the boundary lines
    # now determine which ones are for which edge
    cardinal_clustering = MeanShift(bandwidth=.05).fit(scaled_boundaries)
    boundaries = boundary_scaler.inverse_transform(cardinal_clustering.cluster_centers_)

    showImage(drawLines(image, boundaries))

    boundary_end_pts = [eval_parametric(boundary[0], boundary[1], [0, image.shape[1]]) for boundary in boundaries]

    boundary_end_pts

    segment_pairs = [(a,b) for (a,b) in
                    itertools.combinations(boundary_end_pts, 2)
                    if not (np.array_equal(a,b))]

    all_corners = [seg_intersect(a[0],a[1],b[0],b[1]) for (a,b) in segment_pairs]

    bounded_corners = [pt for pt in all_corners if np.all(pt >= np.array([0,0])) and np.all(pt < np.array([image.shape[1], image.shape[0]]))]

    #out_image=image.copy()
    #for pt in bounded_corners:
    #    cv2.circle(out_image,(int(pt[0]),int(pt[1])),7,[255,0,0],thickness=7)

    #showImage(out_image)
    showImage(drawLines(image, boundaries))
    #destroyWindowOnKey()

    return np.array(bounded_corners).reshape(-1,2)

corners = card_corners(image)

showImage(drawPoints(image, corners))

width, height = 660, 250
#width, height = 990, 325
target = [(0,0),(width,0),(width,height),(0,height)]


C = scipy.spatial.distance.cdist(corners, target)
_, assignment = scipy.optimize.linear_sum_assignment(C)
ordered_target = [target[i] for i in assignment]


M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(ordered_target))
out = cv2.warpPerspective(image.copy(),M,(width,height))

showImage(image)
showImage(out)
destroyWindowOnKey()

out
