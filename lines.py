import cv2
import numpy as np
import math


def filter_lines(lines):
    nlines, _,_ = lines.shape
    linesh = horizontal_lines(lines)
    lineh1, lineh2 = horizontal_bounds(linesh)
    print(lineh1[0],math.degrees(lineh1[1]))
    print(lineh2[0], math.degrees(lineh2[1]))
    return lineh1, lineh2

def horizontal_lines(lines):
    nlines, _, _ = lines.shape
    linesh = []
    for i in range(nlines):
        if abs(lines[i][0][1] - math.pi / 2) < math.radians(2):
            linesh.append((lines[i][0][0],lines[i][0][1]))
    return linesh


def horizontal_bounds(lines):
    lines = sorted(lines, key=lambda l: l[0])
    for i in range(0, len(lines)):
        if abs(lines[i][0] - lines[i - 1][0]) > 100:
            return lines[i >> 1], lines[(len(lines) + i - 1) >> 1]
    return None, None

imagePath = "./images/billiard5.jpg"

image1 = cv2.imread(imagePath)
gray=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
dst = cv2.Canny(gray, 50, 200)

#lines= cv2.HoughLines(dst, 1, math.pi/180.0, 100, np.array([]), 0, 0)
lines= cv2.HoughLines(dst, 1, math.pi/180.0, 100)

a,b,c = lines.shape
flines = filter_lines(lines)

for l in flines:
    rho = l[0]
    theta = l[1]
    a = math.cos(theta)
    b = math.sin(theta)
    x0, y0 = a * rho, b * rho
    pt1 = (int(x0 + 10000 * (-b)), int(y0 + 10000 * (a)))
    pt2 = (int(x0 - 10000 * (-b)), int(y0 - 10000 * (a)))
    cv2.line(gray, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imshow('image1',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
for i in range(a):
    if flines[i]:
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0, y0 = a*rho, b*rho
        pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
        pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
        cv2.line(image1, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

cv2.imshow('image1',image1)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''