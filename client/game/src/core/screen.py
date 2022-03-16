import pygame
import time

from client.game.src.core.game import Game
from client.game.src.core.player.player_controller import PlayerController
from client.game.src.core.player.player import Player


class Screen(object):
    game = None
    target_fps = 120
    prev_time = time.time()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Screen, cls).__new__(cls)
            cls.instance.resolution = (800, 800)
            cls.instance._set_window()
            cls.instance.current_player = None
            cls.instance.new_game()
            cls.instance.loop()
        return cls.instance

    def _set_window(self):
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('FurryTanks')
        pygame.display.set_icon(pygame.image.load('assets/icons/logo.png'))

    @staticmethod
    def refresh_screen():
        pygame.display.update()

    def new_game(self):
        self.instance.game = Game(self.instance.screen)
        self.instance.game.load_assets()
        self.instance.game.refresh_map()
        player = Player(self.instance.screen, self.instance.game, 1)
        self.instance.current_player = PlayerController(player)
        self.refresh_screen()

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            frame_time = clock.tick(self.instance.target_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.instance.current_player.on(frame_time / 1000)
            pygame.display.set_caption('FurryTanks - %.2f FPS' % clock.get_fps())

