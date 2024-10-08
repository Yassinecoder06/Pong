import pygame

pygame.init()
pygame.font.init()

MONITOR = [pygame.display.Info().current_w, pygame.display.Info().current_h]
WIDTH, HEIGHT = 1000, 500
FPS = 60
TIMES = [(1.3*FPS), (1.0*FPS), (0.7*FPS)]  # [time_for_ball_x_vel, time_for_ball_y_vel, time_for_paddle_vel]
AI_LEVEL = 4
OUTLINE = 10
TIME_PADDLE, TIME_BALL = 1, 1
WINNER_SCORE = 10
FONT = pygame.font.SysFont("comicsans", 40)
FONT2 = pygame.font.SysFont("comicsans", 80)
FONT3 = pygame.font.SysFont("comicsans", 20)
ICON = pygame.image.load("assets/icon.png")
BACKROUND_SONG = 'assets/background_sound.mp3'
HIT_SOUND = pygame.mixer.Sound('assets/ball_sound.wav')
