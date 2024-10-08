from .constants import *

pygame.init()


class Paddle:

    def __init__(self, win, left=True):
        self.win = win
        self.left = left
        self.paddle_width = self.win.width / 50
        self.paddle_height = self.win.height / 6.25
        self.MAX_VEL_PADDLE = (self.win.height - self.paddle_height) / TIMES[2]
        self.vel = self.MAX_VEL_PADDLE
        self.score = 0
        if left:
            self.x, self.y = OUTLINE, self.win.height / 2 - self.paddle_height / 2
        else:
            self.x, self.y = self.win.width - OUTLINE - self.paddle_width, self.win.height / 2 - self.paddle_height / 2

    def init(self):
        self.paddle_width = self.win.width / 50
        self.paddle_height = self.win.height / 6.25
        self.MAX_VEL_PADDLE = (self.win.height - self.paddle_height) / TIMES[2]
        self.vel = self.MAX_VEL_PADDLE
        if self.left:
            self.x, self.y = OUTLINE, self.win.height/2 - self.paddle_height/2
        else:
            self.x, self.y = self.win.width - OUTLINE - self.paddle_width, self.win.height/2 - self.paddle_height/2

    def init_score(self):
        self.score = 0
        if self.left:
            self.x, self.y = OUTLINE, self.win.height/2 - self.paddle_height/2
        else:
            self.x, self.y = self.win.width - OUTLINE - self.paddle_width, self.win.height/2 - self.paddle_height/2

    def get_width(self):
        return self.paddle_width
    
    def get_height(self):
        return self.paddle_height

    def draw(self, color):
        pygame.draw.rect(self.win.window, color, (self.x, self.y, self.paddle_width, self.paddle_height))

    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel
    
    def add_score(self):
        self.score += 1
