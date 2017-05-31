import recognizer as rc
import simulator as sm
import base64
import numpy as np
from PIL import Image
import cv2
from StringIO import StringIO
from imag import generate_wrapped


# Get numpy image from Image base64 coding
def data_uri_to_cv2_img(base64_string):
    # Buffer for image
    sbuf = StringIO()
    # Decode image
    sbuf.write(base64.b64decode(base64_string))
    # Create image from buffer
    pimg = Image.open(sbuf)
    # Create Numpy image from Image
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


# Aims to manage table, balls and simulation
class Game:
    def __init__(self, img_str):
        # img = data_uri_to_cv2_img(img_str)
        image_sent = open("../images/billiard/image_sent.jpg","w")
        image_sent.write(base64.b64decode(img_str.split("base64")[1]))
        image_sent.close()
        image_path = generate_wrapped("../images/billiard/image_sent.jpg")
        #image_path = "../images/billiard/b10_wrapped.jpg"
        img = cv2.imread(image_path)
        # Segment table
        pool_table = rc.get_pool_table(img.copy())
        # Get circles
        circles = rc.get_circles(img)
        # Get balls based on image
        circlesf = rc.filter_circles(img.copy(), pool_table.copy(), circles.copy())
        # Get balls position based on table
        balls_pos = rc.find_position(pool_table, circlesf)
        # Get angles from simulation for each ball
        self.angles = sm.solve(balls_pos)
        print(self.angles)

    # Return angles
    def get_angles(self):
        return self.angles
