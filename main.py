from data.window import Window
from data.game import Game
from data.ball import Ball
from data.paddle import Paddle
from data.ai import AI
from data.constants import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("Pong")
pygame.display.set_icon(ICON)
pygame.mixer.music.load(BACKROUND_SONG)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


def calculate_direction(paddle, ball):
    max_distance = paddle.get_height() / 2
    centre_paddle = paddle.y + max_distance
    distance = centre_paddle - ball.y
    constant = max_distance / ball.MAX_Y_VEL_BALL
    y_vel = distance / constant
    ball.y_vel = -1 * y_vel


def ball_movement(win, ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= win.height:
        HIT_SOUND.play()
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        HIT_SOUND.play()
        ball.y_vel *= -1
        
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.get_height():
            if left_paddle.x + left_paddle.get_width() >= ball.x - ball.radius:
                HIT_SOUND.play()
                ball.x_vel *= -1
                calculate_direction(left_paddle, ball)
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.get_height():
            if right_paddle.x <= ball.x + ball.radius:
                HIT_SOUND.play()
                ball.x_vel *= -1
                calculate_direction(right_paddle, ball)          

    ball.move()


def paddle_movement(win, left_paddle, right_paddle, game):
    keys = pygame.key.get_pressed()
    if game.choice == 2:
        if keys[pygame.K_s] and left_paddle.y - left_paddle.vel >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_w] and left_paddle.y + left_paddle.vel + left_paddle.get_height() <= win.height:
            left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + right_paddle.get_height() <= win.height:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    win = Window()
    game = Game(win, "Yassine Jemmali", "1.5.0")
    left_paddle = Paddle(win, left=True)
    right_paddle = Paddle(win, left=False)
    ball = Ball(win)
    ai1 = AI(win, left_paddle, ball, AI_LEVEL)
    game.start([left_paddle, right_paddle], ball)
    game.set_level(ai1, right_paddle, ball)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.VIDEORESIZE:
                    win.resize(event)
                    game.init([left_paddle, right_paddle], ball, False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_p:
                    game.pause([left_paddle, right_paddle], ball)
                if event.key == pygame.K_ESCAPE:
                    game.init([left_paddle, right_paddle], ball, True)
                    game.start([left_paddle, right_paddle], ball)
                    game.set_level(ai1, right_paddle, ball)
                
        if game.choice == 1 or game.choice == 3:
            ai1.ai_movement()
            ai1.ai_adaptation_to(right_paddle)
        if game.choice == 3:
            game.tournament_check(ai1, right_paddle, ball)
        else:
            game.check_winner(left_paddle, right_paddle, ball)

        if ball.x - ball.radius >= win.width:
            ball.restart()
            left_paddle.add_score()
        elif ball.x + ball.radius <= 0:
            ball.restart()
            right_paddle.add_score()

        game.draw([left_paddle, right_paddle], ball, left_paddle.score, right_paddle.score)
        paddle_movement(win, left_paddle, right_paddle, game)
        ball_movement(win, ball, left_paddle, right_paddle)

        print(ball.x_vel, ball.y_vel, right_paddle.vel)

    pygame.quit()


if __name__ == "__main__":
    main()
