# import the necessary packages
from get_perspective import four_point_transform
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
# load the image and grab the source coordinates (i.e. the list of
# of (x, y) points)
# NOTE: using the 'eval' function is bad form, but for this example
# let's just roll with it -- in future posts I'll show you how to
# automatically determine the coordinates without pre-supplying them
 
image = cv2.imread("../images/billiard/b10.jpg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img=mpimg.imread("../images/billiard/b10.jpg")
imgplot = plt.imshow(img)
plt.show()
pts = np.array([(430, 150), (950,150), (1300,730), (0, 730)], dtype = "float32")

# apply the four point tranform to obtain a "birds eye view" of
# the image
warped = four_point_transform(image, pts)

# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)