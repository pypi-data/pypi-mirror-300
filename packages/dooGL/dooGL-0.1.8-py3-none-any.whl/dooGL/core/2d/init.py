import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

def init_window(width=800, height=600, icon="doGl_logo.png",text="DoGL Window"):
    pygame.init()
    
    # Load the icon image and set it as the window icon
    icon = pygame.image.load(icon)
    pygame.display.set_icon(icon)
    
    # Create the Pygame window with OpenGL rendering
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption(text)
    
    # Set up the OpenGL projection matrix (2D orthographic projection)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)  # Adjust for screen size
    glMatrixMode(GL_MODELVIEW)
    
    return screen

def magic(mouse_position=False):
    running = True
    width, height = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and mouse_position:  # Detect mouse click only if mouse_position is True
            x, y = event.pos  # Get x and y coordinates of the mouse click
            y = height - y  # Invert y-coordinate to start from the bottom
            print(f"Mouse clicked at: x={x}, y={y}")
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
    return running


def background(image="doGl_logo.png"):
    # Load the image
    width, height = pygame.display.get_surface().get_size()
    background_image = pygame.image.load(image)
    
    # Resize the image to fit the screen
    background_image = pygame.transform.scale(background_image, (width, height))
    
    # Convert the image to a string format that OpenGL can use
    image_data = pygame.image.tostring(background_image, "RGB", True)
    
    # Enable texture mapping
    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Load the texture data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    
    # Set color to white to prevent the background image from being tinted
    glColor3f(1.0, 1.0, 1.0)
    
    # Draw the background as a textured quad
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(width, 0)
    glTexCoord2f(1, 1); glVertex2f(width, height)
    glTexCoord2f(0, 1); glVertex2f(0, height)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)  # Disable texture mapping after drawing the background
