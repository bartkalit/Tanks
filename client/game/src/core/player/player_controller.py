from enum import Enum
from math import cos, sin, pi
import pygame

from client.game.src.utils.config import Config


class Drive(Enum):
    FORWARD = 0
    BACKWARD = 1


class Rotate(Enum):
    LEFT = 0
    RIGHT = 1


class PlayerController:
    def __init__(self, player):
        self.player = player
        self.reload_time = 0

    def on(self, time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.drive(Drive.FORWARD, time)
        if keys[pygame.K_s]:
            self.drive(Drive.BACKWARD, time)
        if keys[pygame.K_a]:
            self.rotate(Rotate.LEFT, time)
        if keys[pygame.K_d]:
            self.rotate(Rotate.RIGHT, time)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.reload_time > 0:
            self.reload_time -= time

    def drive(self, drive: Drive, time):
        x, y = self.player.position
        speed = Config.player['speed']['drive'] * time
        radians = -self.player.angle * pi / 180
        if drive == Drive.FORWARD:
            new_x = x + (speed * cos(radians))
            new_y = y + (speed * sin(radians))
        else:
            new_x = x - (speed * cos(radians))
            new_y = y - (speed * sin(radians))

        new_position = (new_x, new_y)
        self.player.move(new_position)
        # TODO: Send new position to the server

    def rotate(self, angle: Rotate, time):
        rotate_speed = Config.player['speed']['rotate'] * time
        if angle == Rotate.LEFT:
            new_angle = rotate_speed
        else:
            new_angle = -rotate_speed

        if new_angle > 360:
            new_angle -= 360
        elif new_angle < -360:
            new_angle += 360

        self.player.rotate(new_angle)
        # TODO: Send new angle to the server

    def shoot(self):
        if self.reload_time <= 0:
            self.reload_time = Config.bulllet['reload']
            x, y = self.player.position
            # TODO: Calculate position in front of the tank and replace hard coded 20
            new_x, new_y = self.player.get_barrel_position()
            # new_x = x + sin(self.player.angle) * 20
            # new_y = y + cos(self.player.angle) * 20
            self.player.game.bullet_controller.add_bullet((new_x, new_y), self.player.angle)
        else:
            print("poleruj lufe frajerze")
