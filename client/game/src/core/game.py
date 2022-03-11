import pygame

from client.game.src.core.map import Map
from client.game.src.utils.assets import Assets


class Game:

    def __init__(self, screen):
        self.map = self._load_map('kyiv')
        self.assets = Assets(screen, self.map)
        pass

    def show_map(self):
        x, y = 0, 0
        for row in self.map.data:
            x = 0
            for block in row:
                self.assets.set_block(block, (x, y))
                x += self.assets.width
            y += self.assets.height

    def _load_map(self, map_name: str) -> Map:
        try:
            map = open('assets/maps/' + map_name + '.map')
            lines = map.readlines()
            y = len(lines)
            x = 0
            data = []
            for line in lines:
                line = line.replace('\n', '')
                data.append(line)

                if x == 0:
                    x = len(line)
                elif len(line) != x:
                    raise Exception('Invalid map data')
            return Map(map_name, x, y, data)
        except ValueError:
            print(ValueError)

        return None
