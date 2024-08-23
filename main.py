import pygame
from random import randrange


pygame.init()
pygame.font.init()
pygame.display.set_caption("Pong")
pygame.mixer.music.load('assets/Like a Dance.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 1000, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 80
BALL_VEL, PADDLE_VEL = 2000, 20000
BALL_RADIUS = 7
OUTLINE = 10
FPS = 60
WINNER_SCORE = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicans", 50)
HIT_SOUND = pygame.mixer.Sound('assets/ball_sound.wav')

class Ball():
    MAX_VEL_BALL = 10
    def __init__(self, x, y, radius, vel):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = radius
        self.vel = self.velocity_control(vel)
        self.x_vel = self.vel
        self.y_vel = randrange(1, self.vel)

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

class Paddle():
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

    def move(self, up = True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel
    
    def add_score(self):
        self.score += 1

class AI():
    MAX_LEVEL = 5
    EDGE = 2
    def __init__(self, paddle, ball, ai_level):
        self.paddle = paddle
        self.ball = ball
        self.ai_level = ai_level
        self.ai_level_control()

    def ai_level_control(self):
        if self.ai_level > self.MAX_LEVEL:
            self.ai_level = self.MAX_LEVEL

    def ai_movemment(self, left = True):
        condition = self.paddle.y <= self.ball.y <= self.paddle.y + PADDLE_HEIGHT
        if left:
            conditon1 = 0 <= self.ball.x <= WIDTH // 2
        else:
            conditon1 = WIDTH // 2 <= self.ball.x <= WIDTH

        if not condition and conditon1 :
            if self.ball.y < self.paddle.y and self.paddle.y - self.paddle.vel - self.ai_outline() >= 0:
                self.paddle.move(up = True)
            elif self.ball.y > self.paddle.y and self.paddle.y + self.paddle.vel + PADDLE_HEIGHT + self.ai_outline() <= HEIGHT:
                self.paddle.move(up = False)

    def ai_adaptation_to(self, player_paddle): #adpatation to the opponent
        score_diffrence = self.paddle.score - player_paddle.score
        score_adaptation = (1 - score_diffrence / WINNER_SCORE)
        level_addaptation = (self.ai_level / self.MAX_LEVEL)

        if score_diffrence >= 0:
            self.paddle.vel = player_paddle.MAX_VEL_PADDLE * level_addaptation * score_adaptation
        if score_diffrence < 0:
            self.paddle.vel = player_paddle.MAX_VEL_PADDLE * level_addaptation

    def ai_outline(self):
        outline = ((self.ball.radius + self.EDGE) * 2 ) * (self.ai_level / self.MAX_LEVEL)
        return outline

class Game():
    def __init__(self, win):
        self.win = win
        self.single_player = None

    def start(self):
        start = True
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.single_player = True
                break
            if keys[pygame.K_m]:
                self.single_player = False
                break
            start_text = FONT.render("Start", True, "white")
            single_text = FONT.render("press s to play", True, "green")
            multiplayer_text = FONT.render("press m to play multiplayer", True, 'red')
            self.win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3 - start_text.get_height() // 2))
            self.win.blit(single_text, (WIDTH // 2 - single_text.get_width() // 2,
                                HEIGHT // 3 - single_text.get_height() // 2 + start_text.get_height()))
            self.win.blit(multiplayer_text, (WIDTH // 2 - multiplayer_text.get_width() // 2,
                                        HEIGHT // 3 - multiplayer_text.get_height() // 2 + single_text.get_height() +
                                        start_text.get_height()))
            pygame.display.update()

    def winner(self, won):
        winner_text = FONT.render(f"The winner is {won}", True, "green")
        text = FONT.render(f"You can restart again in {5}s ", True, "red")
        self.win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height()))
        self.win.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - text.get_height() + winner_text.get_height()))
        pygame.display.update()
        pygame.time.delay(5000)

    def pause(self):
        paused = True
        pygame.mixer.music.pause()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                pygame.mixer.music.unpause()
                break
            pause_text = FONT.render("Pause", True, "red")
            continue_text = FONT.render("press c to continue", True, "green")
            self.win.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height()))
            self.win.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2,
                                    HEIGHT // 2 - continue_text.get_height() + pause_text.get_height()))
            pygame.display.update()

    def draw(self, paddles, ball, left_score, right_score):
        self.win.fill("black")

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, "white", (WIDTH // 2 - OUTLINE //2, i, 10, 20))

        for paddle in paddles:
            paddle.draw(self.win)
        ball.draw(self.win)

        left_score_img = FONT.render(str(left_score), True, "white")
        right_score_img = FONT.render(str(right_score), True, "white")
        self.win.blit(left_score_img, (WIDTH // 20, HEIGHT // 20))
        self.win.blit(right_score_img, 
                    (WIDTH - WIDTH // 20 - right_score_img.get_width(),
                    HEIGHT // 20))

        pygame.display.update()

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

def paddle_movement(left_paddle, right_paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and  left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up = True)
    if keys[pygame.K_w] and left_paddle.y + left_paddle.vel + PADDLE_HEIGHT <= HEIGHT:
        left_paddle.move(up = False)
    if keys[pygame.K_UP] and  right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + PADDLE_HEIGHT <= HEIGHT:
        right_paddle.move(up = False)

def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(OUTLINE, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)
    right_paddle = Paddle(WIDTH - OUTLINE - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_VEL)
    game = Game(WIN)
    ai1 = AI(left_paddle, ball, 4)
    game.start()

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
        
        if ball.x - BALL_RADIUS >= WIDTH:
            left_paddle.add_score()
            ball.init()
        elif ball.x + BALL_RADIUS <= 0:
            right_paddle.add_score()
            ball.init()

        game.draw([left_paddle, right_paddle], ball, left_paddle.score, right_paddle.score)
        if game.single_player:
            ai1.ai_movemment(left = True)
            ai1.ai_adaptation_to(right_paddle)
        paddle_movement(left_paddle, right_paddle)
        ball_movement(ball, left_paddle, right_paddle)

        w = False
        if right_paddle.score == WINNER_SCORE:
            won = "Right player"
            w = True
        elif left_paddle.score == WINNER_SCORE:
            won = "Left player"
            w = True

        if w:
            game.winner(won)
            ball.init()
            right_paddle.init()
            left_paddle.init()

        print(left_paddle.vel, right_paddle.vel)

    pygame.quit()


if __name__ == "__main__":
    main()
