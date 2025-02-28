import requests
import re
import pygame
import time
import sc_data
from dataclasses import dataclass

class AppState:
    def __init__(self):
        self.screen = 4  # drawscreen
        self.popup_active = False
        self.blackscreen = False
        self.running = True
        self.last_update = 0
        self.last_rotate = 0

state = AppState()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
BLUE_UI = (100, 100, 255)
hoffset = 60
voffset = 95

# Initialize Pygame
pygame.init()
pygame.mixer.init()

helper_buttons_data = [
    # top row
    ("Lights", ""),
    ("VTOL", "Trans"),
    ("Scan", "Guns"),
    ("SCM", "NAV"),
    # right side row
    ("Mine", "Salv"),
    ("ATC", ""),
    ("Thruster", "Engine"),
    # left side row
    ("blank", ""),
    ("blank", ""),
    ("blank", "")
]

assets = {
    'area18': pygame.image.load('Area18.png'),
    'orison': pygame.image.load('Orison.png'),
    'basic_button_hollow': pygame.image.load('BasicButtonTrans.png'),
    'background_image_full': pygame.image.load('SCBackground.png'),
    'basic_sm_button': pygame.image.load('BasicSmSqButton.png'),
    'basic_sm_label': pygame.image.load('BasicSmSqLabel.png'),
    'popupimg': pygame.image.load('Area18Map700.png'),
    'click_sound': pygame.mixer.Sound('ComputerBeep.wav')
}

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

#sound = pygame.mixer.Sound('ComputerBeep.wav')

# Set up the display
width, height = 800, 480
pygamescreen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption('Test Screen Display')

# Font setup
titlefont = pygame.font.Font(None, 60)
datafont = pygame.font.Font(None, 48)
optionsfont = pygame.font.Font(None, 32)

# Last update time
last_update = time.time()
last_rotate = time.time()

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

drawscreen = 6

menuShowPic = False

def initPopup():
    global popupimg
    global POPUPACTIVE
#    popupimg = pygame.image.load('Area18Map700.png')
    POPUPACTIVE = True

def showPopup():
    global pygamescreen
    pygamescreen.blit(popupimg, (50,20))

def popupClick(x,y):
    global POPUPACTIVE
    POPUPACTIVE = False

def next_screen():
    state.screen += 1
    if state.screen > 6:
        state.screen = 1

def processClickMenu(x, y):
    rect = pygame.Rect(hoffset + 10, voffset + 40, 200, 150)
    if rect.collidepoint(x,y):
        assets["click_sound"].play()
        initPopup()

def processClick(x,y):
    state.blackscreen = False
    state.last_update = time.time()
    state.last_rotate = time.time()

    # always process top clicks quit on top right
    if y < 100 and x > 500:
        state.running = False
    elif y < 100 and x < 100:
        state.blackscreen = True

    # process click events in different ways if there is a popup
    if POPUPACTIVE:
        popupClick(x,y)
    else:
        # bottom right click
        if y > 400 and x > 700:
            assets["click_sound"].play()
            next_screen()
        else:
            if drawscreen == 4:
                processClickMenu(x,y)

def drawSmallAsset(item, xpos, ypos, title, datainfo, color):
    textoffset = 15
    newlineoff = 26
    # button overlay
    pygamescreen.blit(item, (xpos, ypos))
    # draw txt
    if (title != ""):
        button_text = optionsfont.render(title, True, color)
        pygamescreen.blit(button_text, (xpos+textoffset,ypos+textoffset))
    if (datainfo != ""):
        button_text = optionsfont.render(datainfo, True, color)
        pygamescreen.blit(button_text, (xpos+textoffset,ypos+textoffset+newlineoff))

def drawSmallButton(xpos, ypos, title, datainfo, color):
    drawSmallAsset(assets["basic_sm_button"], xpos, ypos, title, datainfo, color)

def drawSmallLabel(xpos, ypos, title, datainfo, color):
    drawSmallAsset(assets["basic_sm_label"], xpos, ypos, title, datainfo, color)

def drawButton(xpos, ypos, title, datainfo, imgsrc):
    textoffset = 15
    # start with the img
    if (imgsrc != ""):
        butimg = pygame.image.load(imgsrc)
        pygamescreen.blit(butimg, (xpos, ypos))
    # draw txt
    if (title != ""):
        button_text = optionsfont.render(title, True, WHITE)
        pygamescreen.blit(button_text, (xpos+textoffset,ypos+textoffset))
    if (datainfo != ""):
        button_text = optionsfont.render(datainfo, True, WHITE)
        pygamescreen.blit(button_text, (xpos+170-button_text.get_width(),ypos+110))
    # button overlay
    pygamescreen.blit(assets["basic_button_hollow"], (xpos, ypos))

def menuScreen2():
    pygamescreen.blit(assets["background_image_full"], (0, 0))
    price_text = titlefont.render("Locations", True, BLUE)
    pygamescreen.blit(price_text, (hoffset,voffset-50))

    drawButton(hoffset, voffset, "Area 18", "Test asdf", "Area18.png")
    drawButton(hoffset, voffset+160, "Orison", "", "Orison.png")

    #column 2
    drawButton(hoffset+210, voffset, "New Babbage", "", "NewBabbage_sm.png")
    drawButton(hoffset+210, voffset+160, "Lorville", "", "Lorville_sm.png")

    # column 3
    drawButton(hoffset+210+210, voffset, "Grim Hex", "", "")
    drawButton(hoffset+210+210, voffset+160, "Pyro Gateway", "", "")

    if POPUPACTIVE:
        showPopup()

def drawHelperButtonScreen(left, right):
    hmod = 200
    sideoff = 120
    vmod = 120
    pygamescreen.fill(BLACK)
    for i, (name1, name2) in enumerate(helper_buttons_data):
        # across the top
        if i < 4:
            drawSmallButton(hoffset+hmod*i, 0, name1, name2, WHITE)
        # down the right side
        elif i > 3 and i < 7:
            if right > 0:
                drawSmallButton(800 - sideoff, vmod * (i-3), name1, name2, WHITE)
        # down the left side
        else:
            if left > 0:
                drawSmallButton(0, vmod * (i-6), name1, name2, WHITE)

    smallback = pygame.transform.scale(assets["background_image_full"], (800-left-right, 400))
    pygamescreen.blit(smallback, (left, 75))

def menuScreen():
    drawHelperButtonScreen(0,120)

    yy = 15

    drawButton(hoffset-25, voffset+yy, "Area 18", "Test asdf", "Area18.png")
    drawButton(hoffset-25, voffset+160+yy, "Orison", "", "Orison.png")

    #column 2
    drawButton(hoffset+210-25, voffset+yy, "New Babbage", "", "NewBabbage_sm.png")
    drawButton(hoffset+210-25, voffset+160+yy, "Lorville", "", "Lorville_sm.png")

    # column 3
    drawButton(hoffset+210+210-25, voffset+yy, "Grim Hex", "", "")
    drawButton(hoffset+210+210-25, voffset+160+yy, "Pyro Gateway", "", "")

    if POPUPACTIVE:
        showPopup()

def displayValuePairScreen(title, names_values):
    drawHelperButtonScreen(0,120)
    # Display names and values
    for i, (name, value) in enumerate(names_values):
        # Render text for name
        name_text = datafont.render(name, True, BLUE)
        # Render text for value
        value_text = datafont.render(value, True, BLUE)

        # Position the texts on the screen
        pygamescreen.blit(name_text, (hoffset, voffset +20+ i * 50))  # Names on the left
        pygamescreen.blit(value_text, (400, voffset + 20+ i * 50))  # Values on the right

def drawValuesScreen():
    drawHelperButtonScreen(0, 120)
    vinc = 80
    drawSmallLabel(hoffset,voffset+20+vinc*0,"Gold","2672",WHITE)
    drawSmallLabel(hoffset,voffset+20+vinc*1,"Laranite","1294",WHITE)
    drawSmallLabel(hoffset,voffset+20+vinc*2,"Agriculm","1294",WHITE)
    drawSmallLabel(hoffset,voffset+20+vinc*3,"Beryl","1294",WHITE)

    drawSmallLabel(hoffset+125,voffset+20+vinc*0,"Gold","2672",WHITE)
    drawSmallLabel(hoffset+125,voffset+20+vinc*1,"Laranite","1294",WHITE)
    drawSmallLabel(hoffset+125,voffset+20+vinc*2,"Agriculm","1294",WHITE)
    drawSmallLabel(hoffset+125,voffset+20+vinc*3,"Beryl","1294",WHITE)

    for i, (name, value) in enumerate(sc_data.ship_data2):
        drawSmallLabel(hoffset+250,voffset+20+vinc*i, name, value, WHITE)

    for i, (name, value) in enumerate(sc_data.ship_data2):
        drawSmallLabel(hoffset+375,voffset+20+vinc*i, name, value, WHITE)

state.last_update = time.time()
state.last_rotate = time.time()

while state.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
        elif event.type == pygame.FINGERDOWN:
            processClick(event.x*width, event.y*height)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            processClick(mousex, mousey)

    # Check if 5 minutes have passed
    if time.time() - state.last_update > 300:  # 300 seconds = 5 minutes
        # black screen every 5 mins
        state.blackscreen = True
        # would like this to rotate screens eventually
    if time.time() - state.last_rotate > 5:  # 300 seconds = 5 minutes
        # do not rotate screen on buttonhelper
        if state.screen != 5:
            state.last_rotate = time.time()
            next_screen()

    # Drawing
    if not(state.blackscreen):
        pygame.mouse.set_visible(True)
        if state.screen == 1:
            displayValuePairScreen("Ship Prices", sc_data.ship_data)
        elif state.screen == 2:
            displayValuePairScreen("Salvage", sc_data.salvage_data)
        elif state.screen == 3:
            displayValuePairScreen("Mining Prices", sc_data.ore_data)
        elif state.screen == 4:
            menuScreen()
        elif state.screen == 5:
            drawValuesScreen()
        elif state.screen == 6:
            # change to 120 if need left side
            drawHelperButtonScreen(0, 120);

        # FLAIR!!!!
        # Increase alpha for fade effect
        alpha -= fade_speed
        if alpha < -255:  # Once we've faded out completely
            alpha = 255  # Cap it at 255
        # Set the alpha of the fade surface
        square_surface.set_alpha(abs(alpha))
        # Draw the fade surface over the screen
        pygamescreen.blit(square_surface, square_rect)
        pygamescreen.blit(square_surface, square_surface.get_rect(center=(252,473)))

    else:
        pygame.mouse.set_visible(False)
        pygamescreen.fill(BLACK)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # 60 FPS
# Quit Pygame
pygame.quit()
