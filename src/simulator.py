import math
from PIL import Image, ImageDraw
import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing as mp


# Without bounds
table_height = 1000
table_width = 500
ball_radio = 10
balls_number = 3
friction = 0.1
initial_speed = 20
time_steep = 1
image = Image.new("RGB", (table_height, table_width))
draw = ImageDraw.Draw(image)

balls_position = []
colors = [(255,0,0),(0,255,0),(0,0,255)]

class BallS:

    def __init__(self, x, y, color, a, speed):
        self.x = x
        self.y = y
        self.color = color
        self.a = math.radians(a)
        self.speed = speed
        self.vx = speed * math.cos(self.a)
        self.vy = speed * math.sin(self.a)

    def move(self):
        image.putpixel((int(self.x), int(self.y)), self.color)

        self.update_velocity(self.vx, self.vy)

        self.speed -= friction

        self.vx = self.speed * math.cos(self.a)
        self.vy = self.speed * math.sin(self.a)

        xnew = self.x + self.vx * time_steep
        ynew = self.y + self.vy * time_steep


        # reflection from the walls
        if xnew < 0 or xnew > table_height - 1:
            self.vx = -self.vx
            xnew = self.x
        if ynew < 0 or ynew > table_width - 1:
            self.vy = -self.vy
            ynew = self.y

        draw.line([(self.x, self.y), (xnew,ynew)], fill=self.color)

        self.x = xnew
        self.y = ynew


    def is_moving(self):
        return self.speed > 1e-5

    @staticmethod
    def is_collision(ba, bb):
       dst = math.hypot(ba.x - bb.x, ba.y - bb.y)
       return True if dst <= ball_radio * 2 else False

    def update_velocity(self, vx, vy):
        self.a = math.atan2(vy, vx)
        self.speed = math.hypot(vx, vy)
        self.vx = vx
        self.vy = vy

    @staticmethod
    def update_velocities(b1, b2):
        n = np.array([b2.x - b1.x, b2.y - b1.y])
        un = n / math.hypot(n[0], n[1])
        ut = np.array([-un[1], un[0]])
        v1n = un[0] * b1.vx + un[1] * b1.vy
        v2n = un[0] * b2.vx + un[1] * b2.vy
        v1t = ut[0] * b1.vx + ut[1] * b1.vy
        v2t = ut[0] * b2.vx + ut[1] * b2.vy
        _v1t = v1t
        _v1n = v2n
        _v2t = v2t
        _v2n = v1n
        V1n = _v1n * un
        V2n = _v2n * un
        V1t = _v1t * ut
        V2t = _v2t * ut
        _V1 = V1n + V1t
        _V2 = V2n + V2t
        b1.update_velocity(_V1[0], _V1[1])
        b2.update_velocity(_V2[0], _V2[1])


def simulation(angle):
    global balls_position, colors

    draw.rectangle([(0,0), (table_height - 1, table_width - 1)], fill=(0,0,0))

    #balls_position = [(20, 20), (130, 40), (280, 450)]

    velocity = [initial_speed, 0, 0]
    angles = [angle, 0, 0]

    balls = []

    # Draw balls
    for ball_id in range(balls_number):
        x, y = balls_position[ball_id]
        balls.append(BallS(x, y, colors[ball_id], angles[ball_id], velocity[ball_id]))
        draw.ellipse([(x - ball_radio, y - ball_radio),  (x + ball_radio, y + ball_radio)])

    #plt.imshow(image)
    #plt.show()

    touches = [None, False, False]

    is_there_any_moving = True
    while is_there_any_moving:
        is_there_any_moving = False

        for b1_id in range(balls_number):
            b1 = balls[b1_id]
            if b1.is_moving():
                is_there_any_moving = True
                b1.move()
            for b2_id in range(balls_number):
                b2 = balls[b2_id]
                if b1 != b2 and BallS.is_collision(b1, b2):
                    # Update v1 and v2
                    BallS.update_velocities(b1, b2)
                    _b1_id, _b2_id = sorted([b1_id, b2_id])
                    if _b1_id == 0:
                        if (_b2_id == 1 and touches[2]) \
                                or (_b2_id == 2 and touches[1]):
                            plt.imshow(image)
                            plt.show()
                            return angle
                        touches[b2_id] = True
                    else:
                        return -1

        if not is_there_any_moving:
            break

    return -1


def solve(bp):
    global balls_position
    balls_position = bp
    angles = []
    for i in range(len(balls_position)):
        aux = balls_position[0].copy()
        balls_position[0] = balls_position[i].copy()
        balls_position[i] = aux
        pool = mp.Pool(processes=mp.cpu_count())
        r = pool.map(simulation, range(0, 360))
        r = [v for v in r if v >= 0]
        #print(r)
        if len(r) > 0:
            angles.append(r[0])

    return angles



#solve([])

#plt.imshow(image)
#plt.show()

#image = Image.new("RGB", (table_height, table_width))
#draw = ImageDraw.Draw(image)