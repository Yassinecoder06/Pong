import pygame

pygame.init()


class Paddle:
    MAX_VEL_PADDLE = 10

    def __init__(self, x, y, width, height, vel):
        self.width = width
        self.height = height
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.vel = self.velocity_control(vel)
        self.score = 0
    
    def init(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.score = 0

    def velocity_control(self, vel):
        if vel > self.MAX_VEL_PADDLE:
            vel = self.MAX_VEL_PADDLE
            return vel
        else:
            return vel

    def draw(self, win):
        pygame.draw.rect(win, "white", (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel
    
    def add_score(self):
        self.score += 1
