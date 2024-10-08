from .constants import *

pygame.init()
pygame.font.init()


class Game:

    def __init__(self, win, creator, version):
        self.win = win
        self.choice = 0
        self.creator = creator
        self.version = version
        self.color1 = "white"
        self.color2 = "black"

    def init(self, paddles, ball, score=True):
        paddles[0].init()
        paddles[1].init()
        ball.init()
        if score:
            for paddle in paddles:
                paddle.init_score()

    def start(self, paddles, ball):
        start = True
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.win.resize(event)
                    self.init(paddles, ball, False)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()
                    if event.key == pygame.K_n:
                        if self.color1 == "black" and self.color2 == "white":
                            self.color1, self.color2 = "white", "black"
                        elif self.color1 == "white" and self.color2 == "black":
                            self.color1, self.color2 = "black", "white"

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

            creator_text = FONT3.render(f"Created by {self.creator}", True, self.color1)
            version_text = FONT3.render(f"version {self.version}", True, self.color1)
            start_text = FONT2.render("Start", True, self.color1)
            singleplayer_text = FONT.render("press s to play", True, "green")
            multiplayer_text = FONT.render("press m to play multiplayer", True, 'red')
            tournament_text = FONT.render("press t to play tournament", True, 'cyan')
            self.win.window.fill(self.color2)
            self.win.window.blit(creator_text, (0, 0))
            self.win.window.blit(version_text, (self.win.width - version_text.get_width(), 0))
            self.win.window.blit(start_text, (self.win.width // 2 - start_text.get_width() // 2,
                                              self.win.height // 3 - start_text.get_height() // 2))
            self.win.window.blit(singleplayer_text, (self.win.width // 2 - singleplayer_text.get_width() // 2,
                                                     self.win.height // 3 - singleplayer_text.get_height() // 2 +
                                                     start_text.get_height()))
            self.win.window.blit(multiplayer_text, (self.win.width // 2 - multiplayer_text.get_width() // 2,
                                                    self.win.height // 3 - multiplayer_text.get_height() // 2 +
                                                    singleplayer_text.get_height() + start_text.get_height()))
            self.win.window.blit(tournament_text, (self.win.width // 2 - tournament_text.get_width() // 2,
                                                   self.win.height // 3 - tournament_text.get_height() // 2 +
                                                   singleplayer_text.get_height() + multiplayer_text.get_height() +
                                                   start_text.get_height()))
            pygame.display.update()

    def tournament_check(self, ai, player, ball):
        won_text = FONT.render("You won", True, "green")
        lost_text = FONT.render("You lost", True, "red")
        upgrade_text = FONT.render("You're upgraded to the next level", True, "green")
        downgrade_text = FONT.render("You're downgraded to the level below", True, "red")
        text = FONT.render("You will be back to the start menu", True, self.color1)

        if ai.paddle.score == WINNER_SCORE and ai.level == 1:
            self.win.window.blit(lost_text, (self.win.width // 2 - lost_text.get_width() // 2, self.win.height // 2 -
                                             lost_text.get_height()))
            self.win.window.blit(text, (self.win.width // 2 - text.get_width() // 2,
                                        self.win.height // 2 - text.get_height() + lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
            self.init([ai.paddle, player], ball, True)
            self.start([ai.paddle, player], ball)
            self.set_level(ai, player, ball)
        elif player.score == WINNER_SCORE and ai.level == 5:
            self.win.window.blit(won_text, (self.win.width // 2 - won_text.get_width() // 2, self.win.height // 2 -
                                            won_text.get_height()))
            self.win.window.blit(text, (self.win.width // 2 - text.get_width() // 2,
                                        self.win.height // 2 - text.get_height() + text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
            self.init([ai.paddle, player], ball, True)
            self.start([ai.paddle, player], ball)
            self.set_level(ai, player, ball)

        w = False
        if ai.paddle.score == WINNER_SCORE:
            ai.subtract_level()
            w = True
            self.win.window.blit(lost_text, (self.win.width // 2 - lost_text.get_width() // 2, self.win.height // 2 -
                                             lost_text.get_height()))
            self.win.window.blit(downgrade_text, (self.win.width // 2 - downgrade_text.get_width() // 2,
                                                  self.win.height // 2 - downgrade_text.get_height() +
                                                  lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
        elif player.score == WINNER_SCORE:
            ai.add_level()
            w = True
            self.win.window.blit(won_text, (self.win.width // 2 - won_text.get_width() // 2,
                                            self.win.height // 2 - won_text.get_height()))
            self.win.window.blit(upgrade_text, (self.win.width // 2 - upgrade_text.get_width() // 2,
                                                self.win.height // 2 - upgrade_text.get_height() +
                                                won_text.get_height()))
            pygame.display.update()
            pygame.time.delay(5000)
        if w:
            self.init([ai.paddle, player], ball, True)

    def draw_winner(self, winning_player):
        winner_text = FONT.render(f"The winner is {winning_player}", True, "green")
        text = FONT.render(f"You can restart again in {5}s ", True, "red")
        self.win.window.blit(winner_text, (self.win.width // 2 - winner_text.get_width() // 2,
                                           self.win.height // 2 - winner_text.get_height()))
        self.win.window.blit(text, (self.win.width // 2 - text.get_width() // 2,
                                    self.win.height // 2 - text.get_height() + winner_text.get_height()))
        pygame.display.update()
        pygame.time.delay(5000)

    def check_winner(self, left_paddle, right_paddle, ball):
        w, winning_player = False, ""
        if right_paddle.score == WINNER_SCORE:
            winning_player = "Right player"
            w = True
        elif left_paddle.score == WINNER_SCORE:
            winning_player = "Left player"
            w = True

        if w:
            self.draw_winner(winning_player)
            self.init([left_paddle, right_paddle], ball, True)

    def pause(self, paddles, ball):
        paused = True
        pygame.mixer.music.pause()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.win.resize(event)
                    self.init(paddles, ball, False)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                pygame.mixer.music.unpause()
                break
            pause_text = FONT.render("Pause", True, "red")
            continue_text = FONT.render("press c to continue", True, "green")
            self.win.window.blit(pause_text, (self.win.width // 2 - pause_text.get_width() // 2,
                                              self.win.height // 2 - pause_text.get_height()))
            self.win.window.blit(continue_text, (self.win.width // 2 - continue_text.get_width() // 2,
                                                 self.win.height // 2 - continue_text.get_height() +
                                                 pause_text.get_height()))
            pygame.display.update()

    def set_level(self, ai, paddle, ball):
        run = True
        if self.choice == 1 or self.choice == 3:
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        self.win.resize(event)
                        self.init([ai.paddle, paddle], ball, False)
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
                beginner_text = FONT.render("a- Beginner", True, self.color1)
                amateur_text = FONT.render("b- Amateur", True, self.color1)
                normal_text = FONT.render("c- Normal", True, self.color1)
                professional_text = FONT.render("d- Professional", True, self.color1)
                top_player_text = FONT.render("e- Top Player", True, self.color1)
                self.win.window.fill(self.color2)
                self.win.window.blit(select_text, (self.win.width // 2 - select_text.get_width() // 2,
                                                   self.win.height // 7 - select_text.get_height()))
                self.win.window.blit(beginner_text, (self.win.width // 2 - beginner_text.get_width() // 2,
                                                     self.win.height * 2 // 7 - beginner_text.get_height()))
                self.win.window.blit(amateur_text, (self.win.width // 2 - amateur_text.get_width() // 2,
                                                    self.win.height * 3 // 7 - amateur_text.get_height()))
                self.win.window.blit(normal_text, (self.win.width // 2 - normal_text.get_width() // 2,
                                                   self.win.height * 4 // 7 - normal_text.get_height()))
                self.win.window.blit(professional_text, (self.win.width // 2 - professional_text.get_width() // 2,
                                                         self.win.height * 5 // 7 - professional_text.get_height()))
                self.win.window.blit(top_player_text, (self.win.width // 2 - top_player_text.get_width() // 2,
                                                       self.win.height * 6 // 7 - top_player_text.get_height()))

                pygame.display.update()

    def draw(self, paddles, ball, left_score, right_score):
        self.win.window.fill(self.color2)

        for i in range(10, self.win.height, 25):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win.window, self.color1, (self.win.width // 2 - OUTLINE // 2, i, 10, 20))

        for paddle in paddles:
            paddle.draw(self.color1)
        ball.draw(self.color1)

        left_score_img = FONT.render(str(left_score), True, self.color1)
        right_score_img = FONT.render(str(right_score), True, self.color1)
        self.win.window.blit(left_score_img, (self.win.width // 20, self.win.height // 20))
        self.win.window.blit(right_score_img, (self.win.width - self.win.width // 20 - right_score_img.get_width(),
                                               self.win.height // 20))

        pygame.display.update()
