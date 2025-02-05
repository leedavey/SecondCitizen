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

salvage_data = [
    ("RMC - Orison", "10,800"),
    ("RMC - Area 18", "8,500"),
    ("RMC - Lorville", "8,500"),
    ("RMC - New Babbage", "8,500")
]

ship_data = [
    ("Freelancer MAX", "4.252M"),
    ("Cutlass Black", "2.116M"),
    ("Hull A", "1.701M"),
    ("Cutter", "0.635M")
]

ore_data = [
    ("Gold", "102"),
    ("Beryl", "50"),
    ("Copper", "40"),
    ("Laranite", "120")
]

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
drawscreen = 1
blackscreen = False

def processClick(x,y):
    global drawscreen
    global running
    global blackscreen

#    print(f"Touch down at: {x}, {y}")
    if y < 100 and x > 500:
        running = False
    elif y < 100 and x < 100:
        blackscreen = not(blackscreen)
    else:
        drawscreen += 1
        if drawscreen > 3:
            drawscreen = 1

def displayValuePairScreen(title, names_values):
    price_text = titlefont.render(title, True, BLUE)
    screen.blit(price_text, (hoffset,voffset))

    # Display names and values
    for i, (name, value) in enumerate(names_values):
        # Render text for name
        name_text = datafont.render(name, True, BLUE)
        # Render text for value
        value_text = datafont.render(value, True, BLUE)

        # Position the texts on the screen
        screen.blit(name_text, (hoffset, voffset + voffset + i * 50))  # Names on the left
        screen.blit(value_text, (400, voffset + voffset + i * 50))  # Values on the right

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            processClick(event.x*width, event.y*height)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            processClick(mousex, mousey)

    # Check if 5 minutes have passed
    if time.time() - last_update > 600:  # 300 seconds = 5 minutes
        last_update = time.time()

    # Drawing
#    pygame.mouse.set_visible(False)
    if not(blackscreen):
        pygame.mouse.set_visible(True)
        hoffset = 60
        voffset = 55
        screen.blit(image, (0, 0))
        if drawscreen == 1:
            displayValuePairScreen("Ship Prices", ship_data)
        elif drawscreen == 2:
            displayValuePairScreen("Salvage", salvage_data)
        elif drawscreen == 3:
            displayValuePairScreen("Mining Prices", ore_data)


        # Increase alpha for fade effect
        alpha -= fade_speed
        if alpha < -255:  # Once we've faded out completely
            alpha = 255  # Cap it at 255

        # Set the alpha of the fade surface
        square_surface.set_alpha(abs(alpha))

        # Draw the fade surface over the screen
        screen.blit(square_surface, square_rect)
    else:
        pygame.mouse.set_visible(False)
        screen.fill(BLACK)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # 60 FPS
# Quit Pygame
pygame.quit()
