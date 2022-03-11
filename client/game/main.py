import pygame


class Map:
    def __init__(self, name, width, height, data):
        self.name = name
        self.width = width
        self.height = height
        self.data = data

    def __str__(self):
        return self.name + '\t' + str(self.width) + 'x' + str(self.height) + '\n' + str('\n'.join(self.data))


class Game:

    def __init__(self):
        self.map = self._load_map('kyiv')
        print(self.map)
        pass

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


game = Game()
