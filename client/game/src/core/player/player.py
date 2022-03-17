from math import sqrt, atan2, degrees, cos, sin, pi

import pygame

from client.game.src.utils.config import Config
from client.game.src.utils.sprite import TankSprite


class Player:
    def __init__(self, game, id: int, position=None):
        if position is None:
            position = (400, 400)
        self.game = game
        self.screen = game.screen
        self.map = game.map
        self.tank = None
        self.id = id
        self.position = position
        self.angle = 0
        self.points = 0
        self.bullets = 5
        self.reload = 0
        self._tank_scale = 0.7
        self.create_tank()

    def create_tank(self):
        tank = pygame.image.load('assets/textures/tank' + str(self.id) + '.png')

        self.position = self.map.get_spawn_point
        self.tank = TankSprite(self.position, pygame.transform.scale(tank, self.get_tank_size()))
        self.rotate(self.init_angle())
        self.game.refresh_players()

    def init_angle(self):
        map_x, map_y = self.screen.get_size()
        map_x /= 2
        map_y /= 2
        x, y = self.position
        return -degrees(atan2(map_y - y, map_x - x))

    def draw(self):
        self.screen.blit(self.tank.image, self.tank.rect)
        # tank_copy = pygame.transform.rotate(self.tank, -self.angle)
        # x, y = self.position
        # new_position = [x - int(tank_copy.get_width() / 2), y - int(tank_copy.get_height() / 2)]
        # self.screen.blit(tank_copy, new_position)
        # print(tank_copy.get_rect())
        pass

    def _wall_collide(self):
        for wall in pygame.sprite.spritecollide(self.tank, self.map.walls, False):
            if pygame.sprite.collide_mask(wall, self.tank):
                return True
        return False

    def _player_collide(self):
        for player in self.game.players:
            if self == player:
                continue

            if pygame.sprite.collide_mask(self.tank, player.tank):
                return True

        return False

    def _collide(self):
        return self._player_collide() or self._wall_collide()

    def move(self, position):
        self.tank.move(position)
        if self._collide():
            self.tank.move(self.position)
        else:
            self.position = position
            self.game.refresh_players()
        # TODO: Emit information to the server
        pass

    def rotate(self, angle):
        self.tank.rotate(self.angle + angle)
        if self._collide():
            self.tank.rotate(self.angle)
        else:
            self.angle += angle
            self.game.refresh_players()
        # TODO: Emit information to the server
        pass

    def shot(self):
        if self.bullets > 0:
            self.bullets -= 1
            new_x, new_y = self.get_barrel_position()
            self.game.bullet_controller.add_bullet((new_x, new_y), self.angle)
            # TODO: Create bullet & emit information to the server
        else:
            print('You don`t have enough bullets in your magazine')

    def get_tank_size(self):
        (w, h) = self.screen.get_size()
        width = w / self.map.width * self._tank_scale
        height = h / self.map.height * self._tank_scale
        return width, height

    def get_barrel_position(self):
        x, y = self.position
        w, h = self.get_tank_size()
        h /= 1.5
        radians = -self.angle * pi / 180
        new_x = x + (h * cos(radians))
        new_y = y + (h * sin(radians))
        print("player:")
        print(f"x = {x} y = {y}")
        print("bullet:")
        print(f"x = {new_x} y = {new_y}")
        return new_x, new_y
