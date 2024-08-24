import pygame
from settings.game import Game
from settings.ball import Ball
from settings.paddle import Paddle
from settings.ai import AI
from settings.constants import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("Pong")
pygame.mixer.music.load('assets/background_sound.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


def calculate_direction(paddle, ball):
    max_distance = PADDLE_HEIGHT / 2
    centre_paddle = paddle.y + max_distance
    distance = centre_paddle - ball.y
    constant = max_distance / ball.MAX_VEL_BALL
    y_vel = distance / constant
    ball.y_vel = -1 * y_vel


def ball_movement(ball, left_paddle, right_paddle):
    if ball.y + BALL_RADIUS >= HEIGHT:
        HIT_SOUND.play()
        ball.y_vel *= -1
    elif ball.y - BALL_RADIUS <= 0:
        HIT_SOUND.play()
        ball.y_vel *= -1
        
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + PADDLE_HEIGHT:
            if left_paddle.x + PADDLE_WIDTH >= ball.x - BALL_RADIUS:
                HIT_SOUND.play()
                ball.x_vel *= -1
                calculate_direction(left_paddle, ball)
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + PADDLE_HEIGHT:
            if right_paddle.x <= ball.x + BALL_RADIUS:
                HIT_SOUND.play()
                ball.x_vel *= -1
                calculate_direction(right_paddle, ball)          

    ball.move()


def paddle_movement(left_paddle, right_paddle, game):
    keys = pygame.key.get_pressed()
    if game.choice == 2:
        if keys[pygame.K_s] and left_paddle.y - left_paddle.vel >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_w] and left_paddle.y + left_paddle.vel + PADDLE_HEIGHT <= HEIGHT:
            left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + PADDLE_HEIGHT <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(OUTLINE, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)
    right_paddle = Paddle(WIDTH - OUTLINE - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_VEL)
    game = Game(WIN)
    ai1 = AI(left_paddle, ball, AI_LEVEL)
    game.start()
    game.set_level(ai1)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_p:
                    game.pause()
                if event.key == pygame.K_ESCAPE:
                    game.start()
                    game.set_level(ai1)
                    ball.init()
                    right_paddle.init()
                    left_paddle.init()

        if game.choice == 1 or game.choice == 3:
            ai1.ai_movement(left=True)
            ai1.ai_adaptation_to(right_paddle)

        if game.choice == 3:
            game.tournament_check(ai1, right_paddle, ball)
        else:
            game.check_winner(left_paddle, right_paddle, ball)
        
        if ball.x - BALL_RADIUS >= WIDTH:
            left_paddle.add_score()
            ball.init()
        elif ball.x + BALL_RADIUS <= 0:
            right_paddle.add_score()
            ball.init()

        game.draw([left_paddle, right_paddle], ball, left_paddle.score, right_paddle.score)
        paddle_movement(left_paddle, right_paddle, game)
        ball_movement(ball, left_paddle, right_paddle)
        print(left_paddle.vel, right_paddle.vel)

    pygame.quit()


if __name__ == "__main__":
    main()
