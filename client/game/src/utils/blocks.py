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
