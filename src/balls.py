import random as rnd

# Ball colors in RGB
balls_colors_rgb = {'white': [255, 255, 255],
          'red': [244, 72, 78],
          'blue': [14, 66, 170],
          'yellow': [239, 230, 64],
          'green': [67, 120, 110],
          'black': [0,0,0],
          'orange': [217, 136, 54],
          'carmine': [114, 42, 54],
          'indigo': [75, 75, 111],
          'fabric': [59, 181, 220]}

balls_colors_rgb = {'white': [255, 255, 255],
          'carmine': [114, 42, 54],
          'fabric': [59, 181, 220]}


# Ball colors in HSV
balls_colors_hsv = {'carmine': [175, 161, 114],
              'white': [0, 0, 255],
              'fabric': [97, 187, 220]}


# Determine if certain set of points are a ball
def is_ball(img, _x, _y, n_points, max_radio):

    # Create random points close to center in order to
    # verify with color if it's an image
    points = [(_x + rnd.randint(0, max_radio), _y + rnd.randint(0, max_radio)) for i in range(n_points)]

    # Number of correct points
    cnt_correct_points = 0

    # Check for each point
    for (x, y) in points:

        # Save best match score and name
        min_dst = 1e10
        min_dst_name = ''

        # Check for each color
        for name_color in balls_colors_hsv:
            color_hsv = balls_colors_hsv[name_color]
            cur_dst = sum(abs(img[x][y][i] - color_hsv[i]) for i in range(3))
            if min_dst > cur_dst:
                min_dst = cur_dst
                min_dst_name = name_color

        # It's correct if ball is over a common color
        if min_dst_name != 'fabric' and min_dst < 250:
            cnt_correct_points += 1

    return cnt_correct_points > n_points // 2


# Script for generate HSV color from RGB colors
'''
# Convert RGB color to HSV
for name in balls_colors_rgb:
    rgb = balls_colors_rgb[name]
    hsv = cv2.cvtColor(np.array([[rgb]], dtype=np.uint8), cv2.COLOR_RGB2HSV)
    print("'" + name + "': " + np.array2string(hsv[0][0], separator=', '))
'''