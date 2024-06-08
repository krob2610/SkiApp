import math
from ast import literal_eval

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygame
from moviepy.editor import VideoClip
from mpl_toolkits.mplot3d import Axes3D
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

print("hi")
df = pd.read_csv("/Users/kuba/SkiApp/HONOR_8X_smoothed_scaled.csv")
df["time"] = pd.to_datetime(df["time"], unit="ns")
df.set_index("time", inplace=True)
start_time = pd.to_datetime("12:46:50").time()
end_time = pd.to_datetime("12:47:50").time()
df = df.between_time(start_time, end_time)

df["Orientation"] = df["Orientation"].apply(
    lambda x: literal_eval(x) if isinstance(x, str) else x
)
df[["qz", "qy", "qx", "qw", "roll", "pitch", "yaw"]] = df["Orientation"].apply(
    pd.Series
)


# Load data into Pandas DataFrame
data = df.copy()  # Assuming your data is stored in a CSV file
# create a apandas dataframe with example pitch roll and yaw cols
# data = pd.DataFrame(
#     {
#         "pitch": [0, 0, 0, 0.5],
#         "roll": [0, 0, 0.5, 0],
#         "yaw": [0, 0.5, 0, 0],
#     }
# )


def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("PyTeapot IMU orientation visualization")
    resizewin(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    clock = pygame.time.Clock()  # Create a Clock object
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        yaw, pitch, roll = read_data()
        if yaw is not None and pitch is not None and roll is not None:
            yaw_deg = math.degrees(yaw)
            pitch_deg = math.degrees(pitch)
            roll_deg = math.degrees(roll)

            draw(1, yaw_deg, pitch_deg, roll_deg)
            pygame.display.flip()
            frames += 1
            print(f"yaw: {yaw_deg}, pitch: {pitch_deg}, roll: {roll_deg}")
        clock.tick(10)  # Limit the updates to 10 per second
    print("fps: %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks)))


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    # Set up the camera view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        7, 0, 0, 0, 0, 0, 0, 0, 1  # Eye position (x, y, z)  # Look at point (x, y, z)
    )  # Up vector (x, y, z)


def read_data():
    if read_data.frame >= len(data):
        print("End of data reached")
        return None, None, None
    # Assuming your DataFrame has columns 'pitch', 'yaw', and 'roll'
    current_frame = read_data.frame
    yaw = data["yaw"][current_frame]
    pitch = data["pitch"][current_frame]
    roll = data["roll"][current_frame]
    read_data.frame += 1
    return yaw, pitch, roll


read_data.frame = 0  # Initialize frame counter


def draw(w, nx, ny, nz):

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)
    glRotatef(-90, 0.0, 0.0, 1.0)
    glRotatef(-90, 1.0, 0.0, 0.0)

    yaw = nx
    pitch = ny
    roll = nz

    glRotatef(roll, 1.00, 0.00, 0.00)
    glRotatef(pitch, 0.00, 0.00, 1.00)
    glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()

    # Draw the axes
    glBegin(GL_LINES)
    # x-axis (roll) in red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-2.0, 0.0, 0.0)
    glVertex3f(2.0, 0.0, 0.0)

    # y-axis (pitch) in green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -2.0, 0.0)
    glVertex3f(0.0, 2.0, 0.0)

    # z-axis (yaw) in blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -2.0)
    glVertex3f(0.0, 0.0, 2.0)
    glEnd()


if __name__ == "__main__":
    # draw(1, 0, 0, 0)
    main()
