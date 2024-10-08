from random import randrange
from .constants import *

pygame.init()


class Ball:

    def __init__(self, win):
        self.win = win
        self.init()
        
    def init(self):
        self.x, self.y = self.win.width / 2, self.win.height / 2
        self.radius = self.win.height / 62.5
        self.MAX_X_VEL_BALL = (self.win.width + self.radius * 2) / TIMES[0]
        self.MAX_Y_VEL_BALL = (self.win.height + self.radius * 2) / TIMES[1]
        self.constant = int(self.MAX_Y_VEL_BALL)
        self.x_vel = self.MAX_X_VEL_BALL
        self.y_vel = randrange(min(-self.constant // 2, -self.constant + self.constant // 2),
                               max(self.constant // 2, self.constant - self.constant // 2))
        
    def restart(self):
        self.x, self.y = self.win.width // 2, self.win.height // 2
        self.x_vel *= -1 
        self.y_vel = randrange(min(-self.constant // 2, -self.constant + self.constant // 2),
                               max(self.constant // 2, self.constant - self.constant // 2))
        
    def draw(self, color):
        pygame.draw.circle(self.win.window, color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
