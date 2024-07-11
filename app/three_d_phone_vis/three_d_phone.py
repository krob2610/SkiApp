import math

import cv2
import numpy as np
import pandas as pd
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


# Function to generate video from DataFrame
def generate_video_from_df(df, output_filename, fps=10, width=640, height=480):
    # Initialize Pygame and OpenGL
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((width, height), video_flags)
    pygame.display.set_caption("PyTeapot IMU orientation visualization")
    resizewin(width, height)
    init()

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    for index, row in df.iterrows():
        yaw, pitch, roll = row["yaw"], row["pitch"], row["roll"]
        draw(yaw, pitch, roll)
        pygame.display.flip()

        # Capture the screen as an image
        frame = capture_frame(width, height)
        video_writer.write(frame)
        print(f"Writing frame for time {index}: yaw={yaw}, pitch={pitch}, roll={roll}")

    video_writer.release()
    print(f"Video saved as {output_filename}")
    pygame.quit()


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


def draw(yaw, pitch, roll):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    drawText((-2.6, 1.8, 2), "PyTeapot", 18)
    drawText((-2.6, 1.6, 2), "Module to visualize Euler angles data", 16)
    drawText((-2.6, -2, 2), "Generating video, please wait...", 16)

    drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" % (yaw, pitch, roll), 16)
    glRotatef(-roll, 0.00, 0.00, 1.00)
    glRotatef(pitch, 1.00, 0.00, 0.00)
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


def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(
        textSurface.get_width(),
        textSurface.get_height(),
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        textData,
    )


def capture_frame(width, height):
    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape(height, width, 3)
    image = np.flipud(image)  # Flip vertically to match OpenGL's coordinate system
    return image


# Example usage
if __name__ == "__main__":
    # Create a sample DataFrame with yaw, pitch, roll data
    data = {
        "time": pd.date_range(start="1/1/2020", periods=100, freq="100ms"),
        "yaw": np.random.uniform(-180, 180, 100),
        "pitch": np.random.uniform(-90, 90, 100),
        "roll": np.random.uniform(-180, 180, 100),
    }
    df = pd.DataFrame(data)
    df.set_index("time", inplace=True)

    # Generate video from the DataFrame
    generate_video_from_df(df, "oooutput_video.avi", fps=10)
