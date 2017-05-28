import numpy as np
import cv2
import balls
import simulator
from enum import Enum
import math


def get_pool_table(img):
    # Bounds of image
    height, width, deep = img.shape

    # Load image in BGR
    img = cv2.medianBlur(img, 5)

    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color range for masking in HSV
    lower = np.array([0, 0, 0])
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
    cv2.drawContours(pool_table, contours, index, (255, 255, 255), 3)

    # Fill background
    pool_table_ff = pool_table.copy()

    # Mask used to flood filling.
    mask = np.zeros((height + 2, width + 2), np.uint8)

    # Floodfill from center's point
    cv2.floodFill(pool_table_ff, mask, (width // 2, height // 2), 255)

    return pool_table_ff


# Get circles from Image
def get_circles(img):
    # Apply filters
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    img = gray
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Get circles from Hough Circles transform
    # 1) Makes a Edge detection
    # 2) Filter circles with radios between 5 and 35
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 90,
                               param1=130, param2=15, minRadius=5, maxRadius=35)

    # If there're circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # Draw circles in gray image
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    return circles


# Filter circles based on table and color
def filter_circles(pool_table_bgr, pool_table_gray, circles):
    circles_filtered = []

    # Convert image in HSV space (better for color comparisons)
    pool_table_hsv = cv2.cvtColor(pool_table_bgr, cv2.COLOR_BGR2HSV)

    # Get size of image
    height, width = pool_table_gray.shape

    # Try to filter each circle
    for i in range(len(circles[0])):
        # Get position and radio
        y, x, r = circles[0][i]

        # Is inside pool table and
        # Has a typical ball's color
        is_ball = x in range(height) and y in range(width) \
                  and pool_table_gray[x][y] != pool_table_gray[0][0] \
                  and balls.is_ball(pool_table_hsv, x, y, 10, 5)

        # Add to filtered circles and draw circle in gray image
        if is_ball:
            circles_filtered.append(circles[0][i])
            cv2.circle(pool_table_gray, (y, x), r, (255 // 2, 255 // 2, 255 // 2), 2)

    # Sort circles for radio
    circles_filtered = sorted(circles_filtered, key=lambda x: x[2])
    print('\n'.join(str(x) for x in circles_filtered))
    circles_filtered = np.array(circles_filtered)
    # print("Number of balls: " + str(len(circles_filtered)))

    return circles_filtered


# Aims to manage directions in bound detector
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# Found bound in specified direction with binary search O(log(n))
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


# Find bound specified direction
def find_bound(pool_table, x, y, direction):
    p = 0
    if direction == Direction.UP:
        p = find_bound_bs(pool_table[:x, y].flatten(), direction)
    elif direction == Direction.DOWN:
        p = find_bound_bs(pool_table[x:, y].flatten(), direction)
        p += x
    elif direction == Direction.LEFT:
        p = find_bound_bs(pool_table[x, :y], direction)
    elif direction == Direction.RIGHT:
        p = find_bound_bs(pool_table[x, y:], direction)
        p += y
    return p


# Get position based on table
def find_position(pool_table, balls):
    HEIGHT_TABLE = simulator.table_height
    WIDTH_TABLE = simulator.table_width

    balls_pos = []

    # For each ball
    for ball in balls:
        y, x, r = ball

        up = find_bound(pool_table, x, y, Direction.UP)
        down = find_bound(pool_table, x, y, Direction.DOWN)
        left = find_bound(pool_table, x, y, Direction.LEFT)
        right = find_bound(pool_table, x, y, Direction.RIGHT)

        # Compute position based on bounds
        row = ((x - up) * HEIGHT_TABLE) // (down - up)
        col = ((y - left) * WIDTH_TABLE) // (right - left)

        # balls_pos.append([HEIGHT_TABLE - row - , col])
        balls_pos.append([row, WIDTH_TABLE - col - 1])
        '''
        print([row, col])
        row, col = solve_pers([x, col, up, down])
        print([row, col])
        '''

    balls_pos = np.array(balls_pos)

    return balls_pos


# Solver perspective problem in position
# [Not working]
def solve_pers(point):
    x, y, up, down = point
    s12 = down - up
    s13 = 1250
    s23 = math.sqrt(s13 * s13 - s12 * s12)
    b = x - up
    c = (b * s23) / s12
    _x = math.hypot(b, c)
    return _x, y


# Script for show an image with OpenCV
'''
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
