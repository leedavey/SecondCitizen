import requests
import re
import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 320, 240
screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption('NVIDIA Stock Price Display')

image = pygame.image.load('DisplayTest.png')
# Scale the image to fit the window if necessary
#image = pygame.transform.scale(image, (width, height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
nvidia_ticker = "NVDA"

# Font setup
font = pygame.font.Font(None, 36)

# Last update time
last_update = time.time()

# Initial price
current_price = 101.34
current_price2 = 342.21

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
    screen.blit(image, (0, 0))
    price_text = font.render(f"NVDA: ${current_price:.2f}", True, BLUE)
    screen.blit(price_text, (50,50))
    price_text = font.render(f"TSLA: ${current_price2:.2f}", True, BLUE)
    screen.blit(price_text, (50,100))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
