#!/usr/bin/env python3

import numpy as np
import cv2

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
showImage(sat)
destroyWindowOnKey()


# find circles

def detectCircles():
    hough_circles = cv2.HoughCircles(sat, cv2.HOUGH_GRADIENT, .8, 25,
                            param1=5,
                            param2=50,
                            minRadius=3,
                            maxRadius=50)
    circles = np.round(hough_circles[0, :]).astype("int")
    output = sat.copy()

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 5, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    print("finished detecting circles: ", len(circles))

    # show the output image
    showImage(np.hstack([sat, output]))
    destroyWindowOnKey()

    print("closed window")

def detectRect():
    ret,thresh = cv2.threshold(sat,127,255,1)

    img,contours,h = cv2.findContours(thresh,1,2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        print(len(approx))
        if len(approx)==5:
            print("pentagon")
            cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            print("triangle")
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            print("square")
            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx) == 9:
            print("half-circle")
            cv2.drawContours(img,[cnt],0,(255,255,0),-1)
        elif len(approx) > 15:
            print("circle")
            cv2.drawContours(img,[cnt],0,(0,255,255),-1)

    showImage(np.hstack([sat, img]))
    destroyWindowOnKey()

detectRect()

1 + 3
