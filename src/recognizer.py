import numpy as np
import cv2
import balls
from enum import Enum

def get_pool_table(img):

    # Bounds of image
    height, width, deep = img.shape

    # Load image in BGR
    img = cv2.medianBlur(img,5)

    # Convert to HSV colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color range for masking in HSV
    lower = np.array([0, 0,  0])
    upper = np.array([70, 255, 255])

    # Apply the mask
    mask = 255 - cv2.inRange(hsv, lower, upper)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get contour of pool table
    areas = [cv2.contourArea(contour) for contour in contours]
    index = areas.index(max(areas))

    # Create gray scale for pool table
    pool_table = np.zeros(img.shape[:2], dtype=np.uint8)

    # Draw contour pool table's image
    cv2.drawContours(pool_table, contours, index, (255,255,255), 3)

    # Fill background
    pool_table_ff = pool_table.copy()

    # Mask used to flood filling.
    mask = np.zeros((height + 2, width + 2), np.uint8)

    # Floodfill from center's point
    cv2.floodFill(pool_table_ff, mask, (width // 2, height // 2), 255)

    '''
    cv2.imshow('pool_table_cc', pool_table_ff)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    return pool_table_ff


def get_circles(image_path):

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    img = cv2.imread(image_path, 0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(blurred,cv2.HOUGH_GRADIENT, 1, 90,
                               param1=130,param2=15,minRadius=5,maxRadius=35)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        '''
        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

    return circles


def filter_circles(pool_table_bgr, pool_table_gray, circles):
    circles_filtered = []

    pool_table_hsv = cv2.cvtColor(pool_table_bgr, cv2.COLOR_BGR2HSV)

    height, width = pool_table_gray.shape

    for i in range(len(circles[0])):
        y, x, r = circles[0][i]

        # Is inside pool table and
        # Has a typical ball's color
        is_ball = x in range(height) and y in range(width) \
                and pool_table_gray[x][y] != pool_table_gray[0][0] \
                and balls.is_ball(pool_table_hsv, x, y, 10, 5)

        if is_ball:
            print(circles[0][i])
            circles_filtered.append(circles[0][i])
            cv2.circle(pool_table_gray, (y, x), r, (255 // 2, 255 // 2, 255 // 2), 2)

    circles_filtered = np.array(circles_filtered)

    '''
    cv2.imshow('detected circles',pool_table_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    print("Number of balls: " + str(len(circles_filtered)))

    return circles_filtered



class Direction(Enum):
    UP  = 1
    DOWN  = 2
    LEFT = 3
    RIGHT = 4


def find_bound_bs(array, direction):
    l, h, m = 0, len(array) - 1, 0
    ans = 0
    while l <= h:
        m = (l + h) >> 1
        if array[m] != array[0]:
            if direction == Direction.UP or direction == Direction.LEFT:
                ans = m
            h = m - 1
        else:
            if direction == Direction.RIGHT or direction == Direction.DOWN:
                ans = m
            l = m + 1

    return ans


def find_bound(pool_table, x, y, direction):
    width, height = pool_table.shape

    if direction == Direction.UP:
        p = find_bound_bs(pool_table[:height // 2, y].flatten(), direction)
    elif direction == Direction.DOWN:
        p = find_bound_bs(pool_table[height // 2:, y].flatten(), direction)
    elif direction == Direction.LEFT:
        p = find_bound_bs(pool_table[x, :width // 2], direction)
    elif direction == Direction.RIGHT:
        p = find_bound_bs(pool_table[x, width // 2:], direction)

    #print(p)
    return p


def find_position(pool_table, balls):

    HEIGHT_TABLE = 4000
    WIDTH_TABLE = 1000

    balls_pos = []

    for ball in balls:
        y, x, r = ball

        up = x - find_bound(pool_table, x, y, Direction.UP)
        down = x - find_bound(pool_table, x, y, Direction.DOWN)
        left = y - find_bound(pool_table, x, y, Direction.LEFT)
        right = y - find_bound(pool_table, x, y, Direction.RIGHT)

        row = (up * HEIGHT_TABLE) // (down - up)
        col = (left * WIDTH_TABLE) // (right - left)

        balls_pos.append([row, col])
        #print([up, left])

    balls_pos = sorted(balls_pos, key=lambda x: x[0])
    for ball in balls_pos:
        print(ball)

    balls_pos = np.array(balls_pos)

    return balls_pos



#img = cv2.imread('./images/billiard/b15.jpg')
#get_pool_table(img)
