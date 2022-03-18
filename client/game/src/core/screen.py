import pygame
import time

from client.game.src.core.game.game_controller import GameController
from client.game.src.utils.config import Config


class Screen(object):
    game = None
    target_fps = 120
    prev_time = time.time()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            pygame.init()
            cls.instance = super(Screen, cls).__new__(cls)
            cls.instance.resolution = (Config.screen['resolution']['width'], Config.screen['resolution']['height'] + Config.screen['stat_bar'])
            cls.instance._set_window()
            cls.instance.game = GameController(cls.instance.screen)
            cls.instance.game.join()
            cls.instance.game.join()
            cls.instance.game.start()
        return cls.instance

    def _set_window(self):
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('FurryTanks')
        pygame.display.set_icon(pygame.image.load('assets/icons/logo.png'))

    @staticmethod
    def refresh_screen():
        pygame.display.update()

