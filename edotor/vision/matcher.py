#!/usr/bin/env python3

import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img_path = '/Users/dgopstein/dotfor/edotor/vision/button_imgs/20181216_150752.jpg'

img1 = cv2.imread(img_path,0)          # queryImage
img2 = cv2.imread('color_template.jpg',0) # trainImage

# Initiate SIFT detector
orb = cv2.ORB_create(edgeThreshold=5, patchSize=13, nlevels=8, fastThreshold=2, scaleFactor=2.2, WTA_K=2,scoreType=cv2.ORB_HARRIS_SCORE, firstLevel=0, nfeatures=5000)

kp2 = orb.detect(img2)
img2_kp = cv2.drawKeypoints(img2, kp2, None, color=(0,255,0), \
        flags=cv2.DrawMatchesFlags_DEFAULT)

plt.figure()
plt.imshow(img2_kp)
plt.show()





# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)


matches = flann.knnMatch(np.float32(des1),np.float32(des2),k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)


if len(good)>=MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,0,30, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

outImg = None
img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,outImg,**draw_params)

plt.imshow(img3, 'gray'),plt.show()
