#!/usr/bin/env python3

import numpy as np
import cv2
import imutils

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

def drawLines(in_img, lines, top_n=-1):
    img = in_img.copy()
    for line in lines[0:top_n]:
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 2000*(-b))
            y1 = int(y0 + 2000*(a))
            x2 = int(x0 - 2000*(-b))
            y2 = int(y0 - 2000*(a))
            print(((x1,y1),(x2,y2)))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    return img

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

showImage(edged)
showImage(drawLines(image, lines))

#kernel = np.ones((2,2),np.uint8)
#dilated = cv2.dilate(edged,kernel,iterations = 30)
#eroded = cv2.erode(dilated,kernel,iterations = 30)
#imshow("dilate", eroded)
dilated = edged

# Find contours based on Edges
(new, cnts, _) = cv2.findContours(val_sat_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
NumberPlateCnt = None #we currently have no Number plate contour

# loop over our contours to find the best possible approximate contour of number plate
allPolys = []
for c in cnts:
    #peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .001, False) #0.0002 * peri, True)
    allPolys.append(approx)
    if len(approx) == 4:  # Select the contour with 4 corners
        NumberPlateCnt = approx #This is our approx Number Plate Contour
        break

contour_image = image.copy()
cv2.drawContours(contour_image, allPolys, -1, (0,255,0), 3)

# Drawing the selected contour on the original image
#cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
imshow("Final Image With Number Plate Detected", contour_image)
destroyWindowOnKey()

showImage(img)
destroyWindowOnKey()
