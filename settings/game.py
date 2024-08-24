import pygame
from .constants import *

pygame.init()
pygame.font.init()


class Game:

    def __init__(self, win):
        self.win = win
        self.choice = 0

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
                self.choice = 1
                break
            if keys[pygame.K_m]:
                self.choice = 2
                break
            if keys[pygame.K_t]:
                self.choice = 3
                break
            start_text = FONT2.render("Start", True, "white")
            singleplayer_text = FONT.render("press s to play", True, "green")
            multiplayer_text = FONT.render("press m to play multiplayer", True, 'red')
            tournament_text = FONT.render("press t to play tournament", True, 'yellow')
            self.win.fill("black")
            self.win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3 - start_text.get_height() // 2))
            self.win.blit(singleplayer_text, (WIDTH // 2 - singleplayer_text.get_width() // 2,
                                HEIGHT // 3 - singleplayer_text.get_height() // 2 + start_text.get_height()))
            self.win.blit(multiplayer_text, (WIDTH // 2 - multiplayer_text.get_width() // 2,
                                        HEIGHT // 3 - multiplayer_text.get_height() // 2 + singleplayer_text.get_height() +
                                        start_text.get_height()))
            self.win.blit(tournament_text, (WIDTH // 2 - tournament_text.get_width() // 2,
                                        HEIGHT // 3 - tournament_text.get_height() // 2 + singleplayer_text.get_height() + multiplayer_text.get_height() +
                                        start_text.get_height()))
            pygame.display.update()

    def tournament_check(self, ai, player, ball):
        won_text = FONT.render("You won", True, "green")
        lost_text = FONT.render("You lost", True, "red")
        upgrade_text = FONT.render("You're upgraded to the next level", True, "green")
        downgrade_text = FONT.render("You're downgraded to the level below", True, "red")
        text = FONT.render("You will be back to the start menu", True, "white")

        if ai.paddle.score == WINNER_SCORE and ai.level == 1:
            self.win.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height()))
            self.win.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - text.get_height() + lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
            self.start()
            self.set_level(ai)
            ball.init()
            player.init()
            ai.paddle.init()

        elif player.score == WINNER_SCORE and ai.level == 5:
            self.win.blit(won_text, (WIDTH // 2 - won_text.get_width() // 2, HEIGHT // 2 - won_text.get_height()))
            self.win.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - text.get_height() + text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
            self.start()
            self.set_level(ai)
            ball.init()
            player.init()
            ai.paddle.init()

        w = False
        if ai.paddle.score == WINNER_SCORE:
            ai.subtract_level()
            w = True
            self.win.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height()))
            self.win.blit(downgrade_text, (WIDTH // 2 - downgrade_text.get_width() // 2,
                            HEIGHT // 2 - downgrade_text.get_height() + lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
        elif player.score == WINNER_SCORE:
            ai.add_level()
            w = True
            self.win.blit(won_text, (WIDTH // 2 - won_text.get_width() // 2, HEIGHT // 2 - won_text.get_height()))
            self.win.blit(upgrade_text, (WIDTH // 2 - upgrade_text.get_width() // 2,
                            HEIGHT // 2 - upgrade_text.get_height() + won_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
        
        if w:
            ball.init()
            player.init()
            ai.paddle.init()

    def draw_winner(self, winning_player):
        winner_text = FONT.render(f"The winner is {winning_player}", True, "green")
        text = FONT.render(f"You can restart again in {5}s ", True, "red")
        self.win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height()))
        self.win.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - text.get_height() + winner_text.get_height()))
        pygame.display.update()
        pygame.time.delay(5000)

    def check_winner(self, left_paddle, right_paddle, ball):
        w = False
        if right_paddle.score == WINNER_SCORE:
            winning_player = "Right player"
            w = True
        elif left_paddle.score == WINNER_SCORE:
            winning_player = "Left player"
            w = True

        if w:
            self.draw_winner(winning_player)
            ball.init()
            right_paddle.init()
            left_paddle.init()

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

    def set_level(self, ai):
        run = True
        if self.choice == 1 or self.choice == 3:
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            ai.level = 1
                            run = False
                            break
                        if event.key == pygame.K_b:
                            ai.level = 2
                            run = False
                            break
                        if event.key == pygame.K_c:
                            ai.level = 3
                            run = False
                            break
                        if event.key == pygame.K_d:
                            ai.level = 4
                            run = False
                            break
                        if event.key == pygame.K_e:
                            ai.level = 5
                            run = False
                            break
                        
                select_text = FONT.render("Select Level", True, "red")
                beginner_text = FONT.render("a- Beginner", True, "white")
                amateur_text = FONT.render("b- Amateur", True, "white")
                normal_text = FONT.render("c- Normal", True, "white")
                professional_text = FONT.render("d- Professional", True, "white")
                top_player_text = FONT.render("e- Top Player", True, "white")
                self.win.fill("black")
                self.win.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 7 - select_text.get_height()))
                self.win.blit(beginner_text, (WIDTH // 2 - beginner_text.get_width() // 2, HEIGHT * 2 // 7 - beginner_text.get_height()))
                self.win.blit(amateur_text, (WIDTH // 2 - amateur_text.get_width() // 2, HEIGHT * 3 // 7 - amateur_text.get_height()))
                self.win.blit(normal_text, (WIDTH // 2 - normal_text.get_width() // 2, HEIGHT * 4 // 7 - normal_text.get_height()))
                self.win.blit(professional_text, (WIDTH // 2 - professional_text.get_width() // 2, HEIGHT * 5 // 7 - professional_text.get_height()))
                self.win.blit(top_player_text, (WIDTH // 2 - top_player_text.get_width() // 2, HEIGHT * 6 // 7 - top_player_text.get_height()))
                        
                pygame.display.update()

    def draw(self, paddles, ball, left_score, right_score):
        self.win.fill("black")

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, "white", (WIDTH // 2 - OUTLINE // 2, i, 10, 20))

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
