import pygame
from pygame.surface import Surface

from game.game import Game
from game.player import Player
from utils import Button

class Application:
    def __init__(self):
        self.background_color = (25, 25, 25)
        self.text_color = (255, 255, 255)
        self.app_screen = None
        self.game_screen = None
        self.game_screen_size = 600
        self.game_grid_size = 30
        self.game_rect_size = self.game_screen_size // self.game_grid_size

    def initialize(self):
        self.app_screen = pygame.display.set_mode((600, 700))
        pygame.display.set_caption('Snakepy')
        pygame.font.init()
        self.player = Player()
        self.game = Game(self.player, self.game_grid_size)
        self.game_surface = Surface((self.game_screen_size, self.game_screen_size))

    def _draw_buttons(self, button_list, mouse):
        for button in button_list:
            if button.collidepoint(mouse):
                button.draw(self.app_screen, 55)
            else:
                button.draw(self.app_screen, 50)

    def _draw_game(self):
        self.game_surface.fill((0, 0, 0))
        body = self.game.player_body
        snack = self.game.snack

        for pos in body:
            pygame.draw.rect(self.game_surface, (0, 255, 0), (pos[0]*self.game_rect_size, pos[1]*self.game_rect_size, self.game_rect_size, self.game_rect_size))
        
        pygame.draw.rect(self.game_surface, (255, 0, 0), (snack[0]*self.game_rect_size, snack[1]*self.game_rect_size, self.game_rect_size, self.game_rect_size))

    def _main_menu(self):
        play_button = Button(50, 50, 100, 50, 'Play')
        quit_button = Button(50, 625, 100, 50, 'Quit')
        button_list = [play_button, quit_button]

        run = True
        while run:
            self.app_screen.fill(self.background_color)
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            mouse = pygame.mouse.get_pos()

            self._draw_buttons(button_list, mouse)

            if clicked:
                if play_button.collidepoint(mouse):
                    self._play_game()
                    self.game.reset()
                elif quit_button.collidepoint(mouse):
                    run = False
            
            pygame.display.update()

    def _play_game(self):
        run = True

        score_text = pygame.font.SysFont('Times New Roman MS', 50)

        while run and not self.game.is_game_finished:
            self.app_screen.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                run = False
            
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.direction = (0, -1)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.direction = (0, 1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.direction = (-1, 0)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.direction = (1, 0)

            pygame.time.delay(75)

            self.game.update()
            self._draw_game()

            text_surface = score_text.render('Score: ' + str(self.game.score), True, self.text_color)

            self.app_screen.blit(text_surface, (0, 25))
            self.app_screen.blit(self.game_surface, (0, 100))
            pygame.display.update()



    def run(self):
        self._main_menu()