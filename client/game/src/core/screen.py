import pygame

from client.game.src.core.game import Game
from client.game.src.utils.assets import Assets


class Screen(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Screen, cls).__new__(cls)

            cls.instance.resolution = (800, 800)
            cls.instance._set_window()
            cls.instance.game = Game()
            cls.instance.loop()
        return cls.instance

    def _set_window(self):
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('FurryTanks')
        Assets.setScreen(self.screen)

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.game.show_map()
