import pygame

from client.game.src.core.map import Map
from client.game.src.utils.assets import Assets


class Game:

    def __init__(self, screen, map_name):
        self.map = self._load_map(map_name)
        self.assets = Assets(screen, self.map)
        self._screen = screen
        self._map_name = map_name
        self._map_img = self.generate_map()

    def show_map(self):
        self._screen.blit(self._map_img, (0, 0))


    def generate_map(self):
        x, y = 0, 0
        for row in self.map.data:
            x = 0
            for block in row:
                self.assets.set_block(block, (x, y))
                x += self.assets.width
            y += self.assets.height
        pygame.display.update()
        map_dir = "assets/maps/" + self._map_name + ".png"
        pygame.image.save(self._screen, map_dir)
        return pygame.image.load(map_dir)

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
