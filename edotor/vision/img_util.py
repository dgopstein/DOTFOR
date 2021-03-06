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

def yuv_img(img):
    yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    yuv_channels = cv2.split(yuv);
    return yuv_channels

def invert(gray):
    return 255-gray

def dilate_erode(img, kern = (2,2), iters=10):
    kernel = np.ones(kern,np.uint8)
    dilated = cv2.dilate(img,kernel,iterations = iters)
    eroded = cv2.erode(dilated,kernel,iterations = iters)
    return eroded

def blur(img):
    return cv2.GaussianBlur(img, (9, 9), 0)

def drawPoints(in_img, points, colors=[]):
    out_image=in_img.copy()
    i = -1
    for pt in points:
        i += 1
        color = [255, 0, 0]
        if len(colors) == len(points):
            color = colors[i]

        cv2.circle(out_image,(int(pt[0]),int(pt[1])),7,color,thickness=7)

    return out_image

def polar2seg(rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 2000*(-b))
    y1 = int(y0 + 2000*(a))
    x2 = int(x0 - 2000*(-b))
    y2 = int(y0 - 2000*(a))

    return [np.array([x1, y1]), np.array([x2, y2])]

def drawLines(in_img, lines, labels=[]):
    img = in_img.copy()
    idx = -1
    for rho,theta in lines:
        idx += 1
        (x1, y1), (x2, y2) = polar2seg(rho, theta)

        color = [0,0,255]
        if len(labels) == len(lines):
            label = labels[idx]
            off = 50*label
            color = [int((0+off)%255), int((100+2*off)%255), int((200+3*off)%255)]

        cv2.line(img,(x1,y1),(x2,y2),color=color,thickness=1)
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

def loadCardRegions():
    csv_dict = pd.read_csv("button_imgs.csv").T.to_dict()

    for k in csv_dict:
        csv_dict[k]['file'] = "button_imgs/"+csv_dict[k]['file'] + '.jpg'

    return [csv_dict[v] for v in csv_dict]

def cluster_1d(lines, bw=0.02):
    return MeanShift(bandwidth=bw).fit(lines.reshape(-1,1))

def cluster_2d(lines, bw=0.05):
    line_scaler = sklearn.preprocessing.MinMaxScaler(copy=True, feature_range=(0, 1))
    scaled_lines = line_scaler.fit(lines).transform(lines)

    clustered_lines_trans = MeanShift(bandwidth=bw).fit(scaled_lines)
    clustered_lines = line_scaler.inverse_transform(clustered_lines_trans.cluster_centers_)
    return clustered_lines

# Find assign one group of points to another
def correspondence(domain, target):
    C = scipy.spatial.distance.cdist(domain, target)
    rows, cols = scipy.optimize.linear_sum_assignment(C)
    ordered_target = [(domain[r], target[c]) for (r, c) in zip(rows, cols)]
    return ordered_target

# https://stackoverflow.com/questions/18152445/get-the-values-in-a-given-radius-from-numpy-array
def n_closest(x,n,d=1):
    return x[n[0]-d:n[0]+d+1,n[1]-d:n[1]+d+1]

def displayCircles(image, circles, ring=True):
    output = image.copy()

    # loop over the (x, y) coordinates and radius of the circles
    for circle in circles:
        x, y = circle[0:2]
        r = 5
        if len(circle) == 3:
            r = circle[2]

        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        if ring:
            cv2.circle(output, (x, y), r, (0, 5, 0), 4)
        rect_size = 2
        cv2.rectangle(output, (x - rect_size, y - rect_size), (x + rect_size, y + rect_size), (0, 128, 255), -1)

    showImage(output)
    #showImage(np.hstack([output, image]))

def rotation2d(theta):
    #theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c,-s), (s, c)))
    return R
