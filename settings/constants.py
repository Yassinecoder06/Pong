import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 80
BALL_VEL, PADDLE_VEL = 2000, 20000
AI_LEVEL = 4
BALL_RADIUS = 7
OUTLINE = 10
FPS = 60
WINNER_SCORE = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 40)
FONT2 = pygame.font.SysFont("comicsans", 80)
HIT_SOUND = pygame.mixer.Sound('assets/ball_sound.wav')
