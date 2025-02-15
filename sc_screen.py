import pygame

# Colors
WHITE = (255, 255, 255)

class scscreen:
    def __init__(self, title):
        self.title = title

    def draw(screen):
        screen.blit(backgroundimg)
        options_text = datafont.render(title, True, WHITE)
        screen.blit(options_text, (100,100))
        pass

    def processInput():
        pass
