import cv2
import recognizer as rc
import simulator as sm
import base64
from matplotlib import pyplot as plt
import io
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import cv2
from StringIO import StringIO


def data_uri_to_cv2_img(base64_string):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

class Game():

    def __init__(self, img_str):
        #img = data_uri_to_cv2_img(img_str)
        image_path = "../images/billiard/b10.jpg"
        img = cv2.imread(image_path)
        pool_table = rc.get_pool_table(img.copy())
        circles = rc.get_circles(img)
        circlesf = rc.filter_circles(img.copy(), pool_table.copy(), circles.copy())
        balls_pos = rc.find_position(pool_table, circlesf)
        self.angles = sm.solve(balls_pos)
        print(self.angles)

    def get_angles(self):
        return self.angles
'''
    pool_table = rc.get_pool_table(img.copy())
    circles = rc.get_circles(image_path)
    circlesf = rc.filter_circles(img.copy(), pool_table.copy(), circles.copy())
    balls_pos = rc.find_position(pool_table, circlesf)
    angles = sm.solve(balls_pos)
'''

'''
    img = cv2.imread()

for i in range(10,11):
    print("Image: " + str(i))
    image_path = "../images/billiard/b" + str(i) + ".jpg"
    img = cv2.imread(image_path)
'''