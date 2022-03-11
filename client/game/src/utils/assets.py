import pygame

from client.game.src.core.screen import Screen
from client.game.src.utils.blocks import Blocks


class Assets:
    all = {}
    width = 0
    height = 0

    @staticmethod
    def load_assets(map_width, map_height):
        assets = Blocks.getAll()
        Assets.width = Screen().resolution[0] / map_width
        Assets.height = Screen().resolution[0] / map_height
        for asset in assets:
            Assets.all[asset] = pygame.image.load('assets/textures/' + asset + '.jpg')
            Assets.all[asset] = pygame.transform.scale(Assets.all[asset], (Assets.width, Assets.height))

    @staticmethod
    def setWall(position):
        return Screen().screen.blit(Assets.all[Blocks.wall], position)

    @staticmethod
    def setGround(position):
        return Screen().screen.blit(Assets.all[Blocks.ground], position)