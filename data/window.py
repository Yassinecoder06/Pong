from .constants import *

pygame.init()


class Window:

    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def full_screen(self, full=True):
        if full:
            self.width, self.height = MONITOR[0], MONITOR[1]
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.width, self.height = WIDTH, HEIGHT
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def resize(self, event):
        self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        self.width = event.w
        self.height = event.h
