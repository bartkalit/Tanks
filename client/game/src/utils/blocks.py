from client.game.src.utils.assets import Assets


class Blocks:
    wall = 'wall'
    ground = 'ground'

    @staticmethod
    def getAll():
        return {Blocks.wall, Blocks.ground}

    @staticmethod
    def setBlock(char, position):
        if char == '#':
            return Assets.setWall(position)
        if char == '.':
            return Assets.setGround(position)
