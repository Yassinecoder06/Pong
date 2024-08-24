import pygame
from .constants import *

pygame.init()


class AI:
    MAX_LEVEL = 5
    EDGE = 2

    def __init__(self, paddle, ball, level):
        self.paddle = paddle
        self.ball = ball
        self.level = self.ai_level_control(level)

    def ai_level_control(self, ai_level):
        if ai_level > self.MAX_LEVEL:
            return self.MAX_LEVEL
        elif ai_level < 1:
            return 1
        return ai_level

    def ai_movement(self, left=True):
        condition = self.paddle.y <= self.ball.y <= self.paddle.y + PADDLE_HEIGHT
        if left:
            condition1 = 0 <= self.ball.x <= WIDTH // 2
        else:
            condition1 = WIDTH // 2 <= self.ball.x <= WIDTH

        if not condition and condition1:
            if self.ball.y < self.paddle.y and self.paddle.y - self.paddle.vel - self.ai_outline() >= 0:
                self.paddle.move(up=True)
            elif self.ball.y > self.paddle.y and self.paddle.y + self.paddle.vel + PADDLE_HEIGHT + self.ai_outline() <= HEIGHT:
                self.paddle.move(up=False)

    def ai_adaptation_to(self, player_paddle):
        score_difference = self.paddle.score - player_paddle.score
        score_adaptation = (1 - score_difference / WINNER_SCORE)
        level_adaptation = (self.level / self.MAX_LEVEL)

        if score_difference >= 0:
            self.paddle.vel = player_paddle.MAX_VEL_PADDLE * level_adaptation * score_adaptation
        if score_difference < 0:
            self.paddle.vel = player_paddle.MAX_VEL_PADDLE * level_adaptation

    def ai_outline(self):
        outline = ((self.ball.radius + self.EDGE) * 2) * (self.level / self.MAX_LEVEL)
        return outline
    
    def add_level(self):
        self.level += 1

    def subtract_level(self):
        self.level -= 1
