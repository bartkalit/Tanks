from enum import Enum
from math import cos, sin, pi
import pygame

from client.game.src.utils.config import Config


class Drive(Enum):
    FORWARD = 0
    BACKWARD = 1


class Rotate(Enum):
    RIGHT = 1
    LEFT = 0


class PlayerController:
    def __init__(self, player):
        self.player = player

    def on(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.drive(Drive.FORWARD)
        if keys[pygame.K_s]:
            self.drive(Drive.BACKWARD)
        if keys[pygame.K_a]:
            self.rotate(Rotate.LEFT)
        if keys[pygame.K_d]:
            self.rotate(Rotate.RIGHT)

    def drive(self, drive: Drive):
        pos = self.player.position
        speed = Config.player['speed']['drive']
        radians = -self.player.angle * pi / 180
        if drive == Drive.FORWARD:
            x = pos[0] + (speed * cos(radians))
            y = pos[1] + (speed * sin(radians))
            new_position = (x, y)
        else:
            x = pos[0] - (speed * cos(radians))
            y = pos[1] - (speed * sin(radians))
            new_position = (x, y)

        self.player.move(new_position)
        # TODO: Send new position to the server

    def rotate(self, angle: Rotate):
        rotate_speed = Config.player['speed']['rotate']
        if angle == Rotate.LEFT:
            new_angle = -rotate_speed
        else:
            new_angle = rotate_speed

        if new_angle > 360:
            new_angle -= 360
        elif new_angle < -360:
            new_angle += 360

        self.player.rotate(new_angle)
        # TODO: Send new angle to the server
