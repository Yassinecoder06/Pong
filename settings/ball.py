import pygame
from random import randrange
from .constants import *

pygame.init()


class Ball:
    MAX_VEL_BALL = 10

    def __init__(self, x, y, radius, vel):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = radius
        self.vel = self.velocity_control(vel)
        self.x_vel = self.vel
        self.y_vel = randrange(1, max(1, self.vel - 1))

    def init(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.x_vel *= -1 
        self.y_vel = randrange(1, self.MAX_VEL_BALL)
    
    def velocity_control(self, vel):
        if vel > self.MAX_VEL_BALL:
            vel = self.MAX_VEL_BALL
            return vel
        else:
            return vel
    
    def draw(self, win):
        pygame.draw.circle(win, "white", (self.x, self.y), BALL_RADIUS)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
