import cv2
import recognizer as rc

for i in range(10,11):
    print("Image: " + str(i))
    image_path = "../images/billiard/b" + str(i) + ".jpg"
    img = cv2.imread(image_path)

    pool_table = rc.get_pool_table(img.copy())
    circles = rc.get_circles(image_path)
    circlesf = rc.filter_circles(img.copy(), pool_table.copy(), circles.copy())
    balls_pos = rc.find_position(pool_table, circlesf)

