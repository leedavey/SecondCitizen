import requests
import re
import pygame
import time
from dataclasses import dataclass

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
BLUE_UI = (100, 100, 255)
hoffset = 60
voffset = 95

@dataclass
class UIButton:
    title: str
    type: int
    imgsrc: str
    action: str
    datainfo: str
    x: int
    y: int

# testButton = UIButton("Lorville", 1, "lorville_sm.png", "", "100", 400, 200)

@dataclass
class ScreenConfig:
    title: str
    type: int
    z: float = 0.0

p = ScreenConfig("Menu", 1)

# Popup modal
POPUPACTIVE = False
popupimg = pygame.image.load('SCBackground.png')

# Initialize Pygame
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound('ComputerBeep.wav')

# Set up the display
width, height = 800, 480
screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption('Test Screen Display')

image = pygame.image.load('DisplayTest.png')
basicButton = pygame.image.load('BasicButtonTrans.png')
# Scale the image to fit the window if necessary
image = pygame.transform.scale(image, (width, height))

main_menu_data = [
    ("Locations", "10,800"),
    ("Mining", "8,500"),
    ("Salvage", "8,500"),
    ("Ship Sales", "8,500")
]

salvage_data = [
    ("Terra Mills (Cellin)", "11,746"),
    ("Orison", "10,800"),
    ("Grim Hex", "9,265"),
    ("Major Cities", "8,500"),
]

ship_data = [
    ("Corsair", "6,666K"),
    ("Freelancer MAX", "4,252K"),
    ("Cutlass Black", "2,116K"),
    ("Hull A", "1,701K"),
    ("Cutter", "635K")
]

ore_data = [
    ("Gold", "2672"),
    ("Beryl", "1148"),
    ("Copper", "145"),
    ("Laranite", "1172"),
    ("Hadanite", "437k")
]

# Font setup
titlefont = pygame.font.Font(None, 60)
datafont = pygame.font.Font(None, 48)
optionsfont = pygame.font.Font(None, 32)

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
drawscreen = 4
blackscreen = False

animAngle = 3.0

menuShowPic = False

def initPopup():
    global popupimg
    global POPUPACTIVE
    popupimg = pygame.image.load('Area18Map700.png')
    POPUPACTIVE = True

def showPopup():
    global screen
    screen.blit(popupimg, (50,20))

def popupClick(x,y):
    global POPUPACTIVE
    POPUPACTIVE = False

def processClickMenu(x, y):
    rect = pygame.Rect(hoffset + 10, voffset + 40, 200, 150)
    if rect.collidepoint(x,y):
        sound.play()
        initPopup()

def processClick(x,y):
    global drawscreen
    global running
    global blackscreen

    # always process top clicks quit on top right
    if y < 100 and x > 500:
        running = False
    elif y < 100 and x < 100:
        blackscreen = not(blackscreen)

    # process click events in different ways if there is a popup
    if POPUPACTIVE:
        popupClick(x,y)
    else:
        # bottom right click
        if y > 400 and x > 700:
            sound.play()
            drawscreen += 1
            if drawscreen > 4:
                drawscreen = 1
        else:
            if drawscreen == 4:
                processClickMenu(x,y)

def drawButton(xpos, ypos, title, datainfo, imgsrc):
    # start with the img
    if (imgsrc != ""):
        butimg = pygame.image.load(imgsrc)
        screen.blit(butimg, (xpos, ypos))
    # draw txt
    if (title != ""):
        button_text = optionsfont.render(title, True, WHITE)
        screen.blit(button_text, (xpos+15,ypos+15))
    if (datainfo != ""):
        button_text = optionsfont.render(datainfo, True, WHITE)
        screen.blit(button_text, (xpos+15,ypos+110))
    # button overlay
    screen.blit(basicButton, (xpos, ypos))

def menuScreen():
    textoffset = 15
    price_text = titlefont.render("Locations", True, BLUE)
    screen.blit(price_text, (hoffset,voffset-50))

    drawButton(hoffset, voffset, "Area 18", "", "Area18.png")
    drawButton(hoffset, voffset+160, "Orison", "", "Orison.png")

    #column 2
    drawButton(hoffset+210, voffset, "New Babbage", "", "NewBabbage_sm.png")
    drawButton(hoffset+210, voffset+160, "Lorville", "", "Lorville_sm.png")

    # column 3
    drawButton(hoffset+210+210, voffset, "Grim Hex", "", "")
    drawButton(hoffset+210+210, voffset+160, "Pyro Gateway", "", "")

    if POPUPACTIVE:
        showPopup()

def displayValuePairScreen(title, names_values):
    price_text = titlefont.render(title, True, BLUE)
    screen.blit(price_text, (hoffset,voffset-50))

    # Display names and values
    for i, (name, value) in enumerate(names_values):
        # Render text for name
        name_text = datafont.render(name, True, BLUE)
        # Render text for value
        value_text = datafont.render(value, True, BLUE)

        # Position the texts on the screen
        screen.blit(name_text, (hoffset, voffset + i * 50))  # Names on the left
        screen.blit(value_text, (400, voffset + i * 50))  # Values on the right

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
        screen.blit(image, (0, 0))
        if drawscreen == 1:
            displayValuePairScreen("Ship Prices", ship_data)
        elif drawscreen == 2:
            displayValuePairScreen("Salvage", salvage_data)
        elif drawscreen == 3:
            displayValuePairScreen("Mining Prices", ore_data)
        elif drawscreen == 4:
            menuScreen()

        # FLAIR!!!!
        # Increase alpha for fade effect
        alpha -= fade_speed
        if alpha < -255:  # Once we've faded out completely
            alpha = 255  # Cap it at 255
        # Set the alpha of the fade surface
        square_surface.set_alpha(abs(alpha))
        # Draw the fade surface over the screen
        screen.blit(square_surface, square_rect)
        screen.blit(square_surface, square_surface.get_rect(center=(252,473)))
#        pygame.draw.arc(screen, BLUE, [750,400,50,50], animAngle, animAngle+1, 4)
#        pygame.draw.rect(screen, GREEN, [200,100,10,10])
        animAngle += 0.1

    else:
        pygame.mouse.set_visible(False)
        screen.fill(BLACK)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # 60 FPS
# Quit Pygame
pygame.quit()
