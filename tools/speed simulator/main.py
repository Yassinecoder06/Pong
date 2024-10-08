import pygame
#this app is for time calculation u put the wanted velocity 
#and u get the time of it which u can use 
#to get the same experience at all screen dimensions
pygame.init()

FPS = 60
TIMES = [(1.3*FPS), (1.1*FPS), (0.7*FPS)]  #[time_for_ball_x_vel, time_for_ball_y_vel, time_for_paddle_vel]


class Paddle:

    def __init__(self, win):
        self.win = win
        self.x, self.y = 0, 0
        self.paddle_width = self.win.get_width() / 50
        self.paddle_height = self.win.get_height() / 6.25
        self.vel = 10 #(self.win.get_height()-self.paddle_height) / TIMES[2]
        
    def draw(self, color):
        pygame.draw.rect(self.win, color, (self.x, self.y, self.paddle_width, self.paddle_height))

    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel


class Ball:

    def __init__(self, win):
        self.win = win
        self.x, self.y = 0, 0
        self.radius = self.win.get_height() / 62.5
        self.MAX_Y_VEL_BALL = 8.5 #(self.win.get_height() + self.radius * 2) / TIMES[1]
        self.MAX_X_VEL_BALL = 12.5 #(self.win.get_width() + self.radius * 2) / TIMES[0]

    def draw(self, color):
        pygame.draw.circle(self.win, color, (self.x, self.y), self.radius)

    def move_y(self):
        self.y += self.MAX_Y_VEL_BALL

    def move_x(self):
        self.x += self.MAX_X_VEL_BALL


def get_time_paddle(paddle, window, time):
    window.fill("black")
    paddle.draw("white")
    paddle.move(False)
    pygame.display.update()
    if paddle.y + paddle.paddle_height >= window.get_height():
        print(time)
        pygame.quit()


def get_time_ball_y(ball, window, time):
    window.fill("black")
    ball.draw("white")
    ball.move_y()
    pygame.display.update()
    if ball.y - ball.radius >= window.get_height():
        print(time)
        pygame.quit()


def get_time_ball_x(ball, window, time):
    window.fill("black")
    ball.draw("white")
    ball.move_x()
    pygame.display.update()
    if ball.x - ball.radius >= window.get_width():
        print(time)
        pygame.quit()


def main():
    run = True
    clock = pygame.time.Clock()
    time = 0
    window = pygame.display.set_mode((1000, 500))
    ball = Ball(window)
    paddle = Paddle(window)
    while run:
        clock.tick(FPS)
        time += 1 / FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        #get_time_paddle(paddle, window, time)
        #get_time_ball_x(ball, window, time)
        get_time_ball_y(ball, window, time)


if __name__ == "__main__":
    main()
