import requests
import re
import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 480
screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption('Test Screen Display')

image = pygame.image.load('DisplayTest.png')
# Scale the image to fit the window if necessary
image = pygame.transform.scale(image, (width, height))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
BLUE_UI = (100, 100, 255)

# Font setup
titlefont = pygame.font.Font(None, 60)
datafont = pygame.font.Font(None, 48)

# Last update time
last_update = time.time()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create a surface for the square with alpha
square_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

pygame.draw.rect(square_surface, GREEN, (0, 0, 16, 16))  # Green square
# Position the square in the middle of the screen

square_rect = square_surface.get_rect(center=(308,473))

# Fade variables
fade_speed = 5  # How quickly to fade out (0-255 per frame)
alpha = 255  # Start with fully transparent

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # When mouse is clicked, set last_update to 10 minutes in the past
            last_update = time.time() - 600  # 600 seconds = 10 minutes    for event in pygame.event.get():
            running = False

    # Check if 5 minutes have passed
    if time.time() - last_update > 600:  # 300 seconds = 5 minutes
        last_update = time.time()

    # Drawing
#    pygame.mouse.set_visible(False)
    hoffset = 60
    voffset = 55
    screen.blit(image, (0, 0))
    price_text = titlefont.render(f"Ship Prices", True, BLUE)
    screen.blit(price_text, (hoffset,voffset))
    price_text = datafont.render(f"Cutlass Black 2.17M", True, BLUE)
    screen.blit(price_text, (hoffset,voffset*2))
    price_text = datafont.render(f"Hull A 1.82M", True, BLUE)
    screen.blit(price_text, (hoffset,voffset*3))
    price_text = datafont.render(f"Cutter 0.62M", True, BLUE)
    screen.blit(price_text, (hoffset,voffset*4))

    # Increase alpha for fade effect
    alpha -= fade_speed
    if alpha < -255:  # Once we've faded out completely
        alpha = 255  # Cap it at 255

    # Set the alpha of the fade surface
    square_surface.set_alpha(abs(alpha))

    # Draw the fade surface over the screen
    screen.blit(square_surface, square_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # 60 FPS
# Quit Pygame
pygame.quit()
