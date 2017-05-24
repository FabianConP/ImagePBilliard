import numpy as np
import cv2

# Load image
bgr_image = cv2.imread('./images/billiard/b23.jpg')

height, width, deep = bgr_image.shape

bgr_image = cv2.medianBlur(bgr_image,5)
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Convert to HSV colorspace
hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Define color range for masking in HSV
lower = np.array([0, 0,  0])
upper = np.array([70, 255, 255])

# Apply the mask
mask = 255 - cv2.inRange(hsv, lower, upper)

#(source, destination, mask to apply)
#result = cv2.bitwise_and(bgr_image,bgr_image, mask=mask)

ret, thresh = cv2.threshold(mask, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


areas = [cv2.contourArea(contour) for contour in contours]
index = areas.index(max(areas))


cv2.drawContours(bgr_image, contours, index, (0,255,0), 3)

cv2.imshow('mask', bgr_image)
cv2.waitKey(0)
cv2.destroyAllWindows()