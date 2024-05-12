from OpenGL.GL import *  # Import OpenGL functions
from OpenGL.GLUT import *  # Import GLUT functions
from OpenGL.GLU import *  # Import GLU functions

# Vertex data for cube
"""
Colored Cube Renderer

This program renders a simple colored cube using OpenGL.

Controls:
- W/S: Rotate the camera up/down
- A/D: Rotate the camera left/right
- ESC: Close the window
"""

import glfw
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Camera parameters
camera_pos = [3, 3, 3]  # Initial position of the camera
camera_yaw = 0  # Initial yaw angle of the camera
camera_pitch = 0  # Initial pitch angle of the camera
camera_speed = 0.001  # Camera movement speed
camera_rotation_speed = 0.1  # Camera rotation speed

# Define vertex data for cube (x, y, z, r, g, b)
vertices = [
    # Front face
    -1.0, -1.0,  1.0, 1.0, 0.0, 0.0,  # Bottom left
     1.0, -1.0,  1.0, 0.0, 1.0, 0.0,  # Bottom right
     1.0,  1.0,  1.0, 0.0, 0.0, 1.0,  # Top right
    -1.0,  1.0,  1.0, 1.0, 1.0, 0.0,  # Top left

    # Back face
    -1.0, -1.0, -1.0, 1.0, 0.0, 0.0,  # Bottom left
     1.0, -1.0, -1.0, 0.0, 1.0, 0.0,  # Bottom right
     1.0,  1.0, -1.0, 0.0, 0.0, 1.0,  # Top right
    -1.0,  1.0, -1.0, 1.0, 1.0, 0.0,  # Top left

    # Top face
    -1.0,  1.0, -1.0, 1.0, 0.0, 0.0,  # Top left
     1.0,  1.0, -1.0, 0.0, 1.0, 0.0,  # Top right
     1.0,  1.0,  1.0, 0.0, 0.0, 1.0,  # Bottom right
    -1.0,  1.0,  1.0, 1.0, 1.0, 0.0,  # Bottom left

    # Bottom face
    -1.0, -1.0, -1.0, 1.0, 0.0, 0.0,  # Top left
     1.0, -1.0, -1.0, 0.0, 1.0, 0.0,  # Top right
     1.0, -1.0,  1.0, 0.0, 0.0, 1.0,  # Bottom right
    -1.0, -1.0,  1.0, 1.0, 1.0, 0.0,  # Bottom left

    # Right face
     1.0, -1.0, -1.0, 1.0, 0.0, 0.0,  # Bottom right
     1.0,  1.0, -1.0, 0.0, 1.0, 0.0,  # Top right
     1.0,  1.0,  1.0, 0.0, 0.0, 1.0,  # Top left
     1.0, -1.0,  1.0, 1.0, 1.0, 0.0,  # Bottom left

    # Left face
    -1.0, -1.0, -1.0, 1.0, 0.0, 0.0,  # Bottom left
    -1.0,  1.0, -1.0, 0.0, 1.0, 0.0,  # Top left
    -1.0,  1.0,  1.0, 0.0, 0.0, 1.0,  # Top right
    -1.0, -1.0,  1.0, 1.0, 1.0, 0.0   # Bottom right
]


def draw_cube():
    """
    Draw the cube using OpenGL.

    This function iterates over the vertex data and draws each face of the cube.
    """
    glBegin(GL_QUADS)  # Begin drawing quads
    for i in range(0, len(vertices), 24):  # Iterate over each face of the cube
        for j in range(4):  # Iterate over vertices of each face
            # Set color for the vertex
            glColor3f(*vertices[i+j*6+3:i+j*6+6])  
            # Define vertex for the face
            glVertex3f(*vertices[i+j*6:i+j*6+3])  
    glEnd()  # End drawing quads

def display():
    """
    Display function called by OpenGL to render the scene.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluPerspective(45, 800 / 600, 0.1, 50.0)
    gluLookAt(*camera_pos, 0, 0, 0, 0, 1, 0)

    draw_cube()

    glfw.swap_buffers(window)

def update_camera():
    global camera_pos, camera_yaw, camera_pitch

    # Calculate forward vector based on yaw and pitch
    forward = np.array([
        math.cos(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch)),
        math.sin(math.radians(camera_pitch)),
        math.sin(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch))
    ])

    # Normalize forward vector
    forward = forward / np.linalg.norm(forward)

    # Calculate right vector (cross product of forward and up)
    up = np.array([0, 1, 0])  # Assuming the camera's up vector is always (0, 1, 0)
    right = np.cross(forward, up)

    # Move camera based on keyboard input
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera_pos += camera_speed * forward
    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera_pos -= camera_speed * forward
    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera_pos += camera_speed * right
    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera_pos -= camera_speed * right

    # Print camera position for debugging
    print("Camera Position:", camera_pos)


def key_callback(window, key, _, action, mods):
    """
    Callback function for handling key events.

    This function adjusts the camera yaw and pitch based on user input.
    """
    global camera_yaw, camera_pitch

    print("Key:", key, "Action:", action)  # Add this line to check key and action

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_W and action == glfw.PRESS:
        camera_pitch -= camera_rotation_speed
    elif key == glfw.KEY_S and action == glfw.PRESS:
        camera_pitch += camera_rotation_speed
    elif key == glfw.KEY_A and action == glfw.PRESS:
        camera_yaw -= camera_rotation_speed
    elif key == glfw.KEY_D and action == glfw.PRESS:
        camera_yaw += camera_rotation_speed



def main():
    """
    Main function to initialize OpenGL and start the rendering loop.
    """
    global window

    if not glfw.init():  # Initialize GLFW
        return

    window = glfw.create_window(800, 600, "Colored Cube", None, None)  # Create a window
    if not window:  # If window creation fails
        glfw.terminate()  # Terminate GLFW
        return

    glfw.make_context_current(window)  # Make the window's context current
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering

    glfw.set_key_callback(window, key_callback)  # Set key callback function

    while not glfw.window_should_close(window):  # Main rendering loop
        glfw.poll_events()  # Poll events
        update_camera()  # Update camera position
        display()  # Render the scene


    glfw.terminate()  # Terminate GLFW when window is closed

if __name__ == "__main__":
    main()  # Start the main function


def draw_cube():

    glBegin(GL_QUADS)  # Begin drawing quadrilaterals

    for i in range(0, len(vertices), 6):  # Iterate over vertices
        glColor3f(vertices[i+3], vertices[i+4], vertices[i+5])  # Set color for the quad
        glVertex3f(*vertices[i:i+3])  # Define vertex 1 of quad
        glVertex3f(*vertices[i+6:i+9])  # Define vertex 2 of quad
        glVertex3f(*vertices[i+12:i+15])  # Define vertex 3 of quad
        glVertex3f(*vertices[i+18:i+21])  # Define vertex 4 of quad

    glEnd()  # End drawing quads

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear color and depth buffer
    glLoadIdentity()  # Load identity matrix
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Set up the camera position
    draw_cube()  # Draw the cube
    glutSwapBuffers()  # Swap buffers to display the result


def reshape(width, height):
    glViewport(0, 0, width, height)  # Set the viewport
    glMatrixMode(GL_PROJECTION)  # Select the projection matrix
    glLoadIdentity()  # Load identity matrix
    gluPerspective(45, width/height, 0.1, 50.0)  # Set perspective projection
    glMatrixMode(GL_MODELVIEW)  # Select the modelview matrix
    glLoadIdentity()  # Load identity matrix


def main():
    glutInit()  # Initialize GLUT
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Set display mode
    glutInitWindowSize(800, 600)  # Set window size
    glutCreateWindow(b"Colored Cube")  # Create a window with title

    glEnable(GL_DEPTH_TEST)  # Enable depth testing

    glutDisplayFunc(display)  # Set display callback function
    glutReshapeFunc(reshape)  # Set reshape callback function

    glutMainLoop()  # Start the main loop


if __name__ == "__main__":
    main()  # Call main function when the script is executed
