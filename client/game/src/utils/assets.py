import pygame

from client.game.src.utils.blocks import Blocks


class Assets:
    all = {}
    width = 0
    height = 0

    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.load_assets()

    def load_assets(self):
        assets = Blocks.getAll()

        (w, h) = self.screen.get_size()
        self.width = w / self.map.width
        self.height = h / self.map.height
        for asset in assets:
            self.all[asset] = pygame.image.load('assets/textures/' + asset + '.png')
            self.all[asset] = pygame.transform.scale(self.all[asset], (self.width, self.height))

    def set_wall(self, position):
        return self.screen.blit(self.all[Blocks.wall], position)

    def set_ground(self, position):
        return self.screen.blit(self.all[Blocks.ground], position)

    def set_block(self, char, position):
        block = Blocks.getBlock(char)
        if block == Blocks.wall:
            return self.set_wall(position)
        if block == Blocks.ground:
            return self.set_ground(position)
