import numpy as np
import cv2
import random
import operator
from numpy.linalg import lstsq

def find_line(img, imgc, points, dir):
    bound = []
    x = []
    y = []
    height, width = img.shape
    for p in points:
        while p[0] in range(height) and p[1] in range(width) \
                and img[p[0]][p[1]] != 0:
            p[0] += dir[0]
            p[1] += dir[1]
        p[0] = min(max(0, p[0]), height - 1)
        p[1] = min(max(0, p[1]), width - 1)
        bound.append([p[0],p[1]])
    bound = sorted(bound, key=operator.itemgetter(0, 1))
    for p in bound:
        x.append(p[1])
        y.append(p[0])

    A = np.vstack([x, np.ones(len(y))]).T
    m, c = lstsq(A, y)[0]
    print "Line Solution is y = {m}x + {c}".format(m=m, c=c)

    x0, x1, y0, y1 = 0, width - 1, int(c), int((width - 1) * m + c)
    imgc = cv2.line(imgc, (x0, y0), (x1, y1), (255, 0, 0), 3)
    return imgc


# Load image
bgr_image = cv2.imread('./images/billiard5.jpg')

height, width, deep = bgr_image.shape

bgr_image = cv2.medianBlur(bgr_image,5)
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Convert to HSV colorspace
hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Define color range for masking in HSV
lower = np.array([0, 0,  0])
upper = np.array([24, 182, 255])

# Apply the mask
mask = 255 - cv2.inRange(hsv, lower, upper)

#(source, destination, mask to apply)
#result = cv2.bitwise_and(bgr_image,bgr_image, mask=mask)
cv2.imshow('mask', mask)
#cv2.imwrite("./images/mask.jpg", mask)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


green = np.uint8([[[50, 180, 212]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_RGB2HSV)

points = np.array([[random.randint(0, 15) + (height // 4), random.randint(0, 95) + (width // 2)] for i in range(5)], dtype=np.int32)

bimg = find_line(mask, bgr_image.copy(), points, [-1, 0])
bimg = find_line(mask, bimg, points, [0, 1])
bimg = find_line(mask, bimg, points, [1, 0])
bimg = find_line(mask, bimg, points, [-1, 0])


cv2.imshow('img line', bimg)
cv2.waitKey(0)

