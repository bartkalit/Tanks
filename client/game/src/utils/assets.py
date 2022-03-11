import pygame


class Blocks:
    wall = 'wall'
    ground = 'ground'

    @staticmethod
    def getAll():
        return {Blocks.wall, Blocks.ground}

    @staticmethod
    def getBlock(char):
        if char == '#':
            return Blocks.wall
        if char == '.':
            return Blocks.ground


class Assets:
    all = {}
    width = 0
    height = 0

    @staticmethod
    def setScreen(screen):
        Assets.screen = screen

    @staticmethod
    def load_assets(map_width, map_height):
        assets = Blocks.getAll()
        Assets.width = Assets.screen.get_size()[0] / map_width
        Assets.height = Assets.screen.get_size()[1] / map_height
        for asset in assets:
            Assets.all[asset] = pygame.image.load('assets/textures/' + asset + '.jpg')
            Assets.all[asset] = pygame.transform.scale(Assets.all[asset], (Assets.width, Assets.height))

    @staticmethod
    def setWall(position):
        return Assets.screen.blit(Assets.all[Blocks.wall], position)

    @staticmethod
    def setGround(position):
        return Assets.screen.blit(Assets.all[Blocks.ground], position)

    @staticmethod
    def setBlock(char, position):
        block = Blocks.getBlock(char)
        if block == Blocks.wall:
            return Assets.setWall(position)
        if block == Blocks.ground:
            return Assets.setGround(position)
