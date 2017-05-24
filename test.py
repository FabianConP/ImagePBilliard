import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./images/blackandwhite.jpg', 0)
img = np.float32(img)

corners = cv2.cornerHarris(img, 2, 3, 0.04)

plt.subplot(2, 1, 1), plt.imshow(corners, cmap='jet')
plt.title('Harris Corner Detection'), plt.xticks([]), plt.yticks([])

img2 = cv2.imread('./images/blackandwhite.jpg')
corners2 = cv2.dilate(corners, None, iterations=3)
img2[corners2 > 0.01 * corners2.max()] = [55]

plt.subplot(2, 1, 2), plt.imshow(img2, cmap='gray')
plt.title('Canny Edge Detection'), plt.xticks([]), plt.yticks([])

plt.show()