import pygame
from pygame.surface import Surface

from game.game import Game
from game.player import Player
from utils import Button

from genetic_algorithm.utils import load_individual_parameters

from smart_player import SmartPlayer

import json

class Application:
    def __init__(self):
        self.background_color = (25, 25, 25)
        self.text_color = (255, 255, 255)
        self.app_screen = None
        self.game_screen = None
        self.game_screen_size = 600
        self.game_state_type_vision = True

    def initialize(self):
        self._load_config()
        self.game_grid_size = self.settings['game_settings']['grid_size']
        self.game_rect_size = self.game_screen_size // self.game_grid_size

        self.app_screen = pygame.display.set_mode((600, 700))
        pygame.display.set_caption('Snakepy')
        pygame.font.init()
        self.game_surface = Surface((self.game_screen_size, self.game_screen_size))

    def _load_config(self):
        try:
            with open('config.json', 'r') as fin:
                self.settings = json.load(fin)
                print('Loading configuration...')
        except:
            self.settings = {"network_settings": {
                            "input_type_comment" : "choose between vision and game state",
                            "input_type": "vision",
                            "hidden_layers" : [8, 4],
                            "hidden_layer_activation_comment" : "choose between ReLU and Sigmoid",
                            "hidden_layer_activation" : "ReLU"
                            },
                        "genetic_algorithm_settings" : {
                            "population_size" : 1000,
                            "parents_size" : 200,
                            "selection_type_comment" : "choose between roulette wheel selection and tournament selection",
                            "selection_type" : "tournament selection",
                            "crossover_type_comment" : "choose between single point crossover and uniform crossover",
                            "crossover_type" : "uniform crossover",
                            "mutation_type_comment" : "choose between boundary mutation, flip mutation and uniform mutation",
                            "mutation_type" : "uniform mutation",
                            "mutation_rate" : 0.01
                            },
                        "game_settings" : {
                            "grid_size" : 30
                            }
                        }
            with open('config.json', 'w') as fout:
                json.dump(self.settings, fout, indent=4)
            


    def _draw_buttons(self, button_list, mouse):
        for button in button_list:
            if button.collidepoint(mouse):
                button.draw(self.app_screen, 55)
            else:
                button.draw(self.app_screen, 50)

    def _draw_game(self, game):
        self.game_surface.fill((0, 0, 0))
        body = game.player_body
        snack = game.snack

        for pos in body:
            pygame.draw.rect(self.game_surface, (0, 255, 0), (pos[0]*self.game_rect_size, pos[1]*self.game_rect_size, self.game_rect_size, self.game_rect_size))
        
        pygame.draw.rect(self.game_surface, (255, 0, 0), (snack[0]*self.game_rect_size, snack[1]*self.game_rect_size, self.game_rect_size, self.game_rect_size))

    def _main_menu(self):
        play_button = Button(50, 50, 100, 50, 'Play')
        ga_play_button = Button(50, 150, 300, 50, 'Genetic Algorithm')
        quit_button = Button(50, 625, 100, 50, 'Quit')
        button_list = [play_button, ga_play_button, quit_button]

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
                elif ga_play_button.collidepoint(mouse):
                    self._auto_play()
                elif quit_button.collidepoint(mouse):
                    run = False
            
            pygame.display.update()

    def _auto_play(self):
        run = True
        game = Game(self.game_grid_size)

        score_text = pygame.font.SysFont('Times New Roman MS', 50)

        input_type = self.settings['network_settings']['input_type']
        input_dim = 8 if input_type == 'vision' else (self.game_grid_size + 2)**2
        hidden_layers = self.settings['network_settings']['hidden_layers']
        hidden_layer_activation = self.settings['network_settings']['hidden_layer_activation']
        player = SmartPlayer(input_dim, hidden_layers, hidden_layer_activation)

        # load the trained model if available
        load_individual_parameters(str(player.network), hidden_layer_activation, player)

        while run and not game.is_game_finished:
            self.app_screen.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                run = False
            
            game_state = game.get_game_state(self.game_state_type_vision)
            player.predict_direction(game_state)
            
            pygame.time.delay(25)

            game.update(player)
            if player.steps_since_last_snack > 200:
                player.alive = False
                game.is_game_finished = True
            self._draw_game(game)

            text_surface = score_text.render('Score: ' + str(player.score), True, self.text_color)

            self.app_screen.blit(text_surface, (225, 25))
            self.app_screen.blit(self.game_surface, (0, 100))
            pygame.display.update()


    def _play_game(self):
        run = True
        game = Game(self.game_grid_size)

        score_text = pygame.font.SysFont('Times New Roman MS', 50)
        player = Player()
            
        while run and not game.is_game_finished:
            self.app_screen.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                run = False
            
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.direction = (0, -1)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.direction = (0, 1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.direction = (-1, 0)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.direction = (1, 0)

            pygame.time.delay(75)

            game.update(player)
            self._draw_game(game)

            text_surface = score_text.render('Score: ' + str(player.score), True, self.text_color)

            self.app_screen.blit(text_surface, (225, 25))
            self.app_screen.blit(self.game_surface, (0, 100))
            pygame.display.update()


    def run(self):
        self._main_menu()