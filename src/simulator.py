import math
import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# Game constraints
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
# Path simulation color
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


# Aims to manage physics of balls
class BallS:
    def __init__(self, x, y, color, a, speed):
        self.x = x
        self.y = y
        # Path simulation color
        self.color = color
        # Velocity vector polar coordinates
        self.a = math.radians(a)
        self.speed = speed
        # Velocity vector cartesian coordinates
        self.vx = speed * math.cos(self.a)
        self.vy = speed * math.sin(self.a)

    # Move ball based on his velocity vector
    def move(self):
        # Draw path
        image.putpixel((int(self.x), int(self.y)), self.color)

        # Update speeds
        self.update_velocity(self.vx, self.vy)

        self.speed -= friction

        self.vx = self.speed * math.cos(self.a)
        self.vy = self.speed * math.sin(self.a)

        # Get new position in a specified time steep
        xnew = self.x + self.vx * time_steep
        ynew = self.y + self.vy * time_steep

        # Reflection from the walls
        if xnew < 0 or xnew > table_height - 1:
            self.vx = -self.vx
            xnew = self.x
        if ynew < 0 or ynew > table_width - 1:
            self.vy = -self.vy
            ynew = self.y

        draw.line([(self.x, self.y), (xnew, ynew)], fill=self.color)

        # Update positions
        self.x = xnew
        self.y = ynew

    # Check if a ball can move
    def is_moving(self):
        return self.speed > 1e-5

    # Detects collision between two balls
    @staticmethod
    def is_collision(ba, bb):
        dst = math.hypot(ba.x - bb.x, ba.y - bb.y)
        return True if dst <= ball_radio * 2 else False

    # Update velocity polar vector
    def update_velocity(self, vx, vy):
        self.a = math.atan2(vy, vx)
        self.speed = math.hypot(vx, vy)
        self.vx = vx
        self.vy = vy

    # Manage velocities in a collision
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


# Simulates a hit with a specified angle
def simulation(angle):
    global balls_position, colors

    # Draw bounds of table
    draw.rectangle([(0, 0), (table_height - 1, table_width - 1)], fill=(0, 0, 0))

    # Only for testing
    # balls_position = [(20, 20), (130, 40), (280, 450)]

    # Only one balls has a initial speed and angle
    velocity = [initial_speed, 0, 0]
    angles = [angle, 0, 0]

    balls = []

    # Draw balls
    for ball_id in range(balls_number):
        x, y = balls_position[ball_id]
        balls.append(BallS(x, y, colors[ball_id], angles[ball_id], velocity[ball_id]))
        draw.ellipse([(x - ball_radio, y - ball_radio), (x + ball_radio, y + ball_radio)])

    # Manage ball touches
    touches = [None, False, False]

    # Still simulation until a ball has move or detects a win
    is_there_any_moving = True
    while is_there_any_moving:
        is_there_any_moving = False

        # For each ball update his position and speed
        for b1_id in range(balls_number):
            b1 = balls[b1_id]
            # If ball can make a move
            if b1.is_moving():
                is_there_any_moving = True
                b1.move()
            # Detect if the ball has a collision with other ball
            for b2_id in range(balls_number):
                b2 = balls[b2_id]
                if b1 != b2 and BallS.is_collision(b1, b2):
                    # Update v1 and v2
                    BallS.update_velocities(b1, b2)
                    _b1_id, _b2_id = sorted([b1_id, b2_id])
                    # If first hit ball is in the collision
                    if _b1_id == 0:
                        # Detect if makes a win touch
                        if (_b2_id == 1 and touches[2]) \
                                or (_b2_id == 2 and touches[1]):
                            plt.imshow(image)
                            plt.show()
                            return angle
                        # Save touch
                        touches[b2_id] = True
                    else:
                        # Non first hit ball touch
                        return -1

        if not is_there_any_moving:
            break

    # Not is an angle win move
    return -1


# Find suggestions from ball positions
def solve(bp):
    global balls_position
    balls_position = bp
    angles = []
    # Starting from each ball
    for i in range(len(balls_position)):
        # Puts hit ball in first position
        aux = balls_position[0].copy()
        balls_position[0] = balls_position[i].copy()
        balls_position[i] = aux
        # Makes simulation with parallel programming
        pool = mp.Pool(processes=mp.cpu_count())
        r = pool.map(simulation, range(0, 360))
        # Filter winner angles
        r = [v for v in r if v >= 0]
        # Get first winner angle
        if len(r) > 0:
            angles.append(r[0])

    return angles
