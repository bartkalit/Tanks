from enum import Enum

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
        # TODO: Calculate new position
        new_position = pos
        if drive == Drive.FORWARD:
            # TODO: Calculate new position
            x = pos[0]
            y = pos[1]
            speed = Config.player['speed']['drive']
            new_position = (x + speed, y + speed)
            pass
        else:
            # TODO: Calculate new position
            x = pos[0]
            y = pos[1]
            speed = Config.player['speed']['drive']
            new_position = (x - speed, y - speed)
            pass

        self.player.move(new_position)
        # TODO: Send new position to the server

    def rotate(self, angle: Rotate):
        rotate_speed = Config.player['speed']['rotate']
        if angle == Rotate.LEFT:
            new_angle = rotate_speed
        else:
            new_angle = -rotate_speed

        self.player.rotate(new_angle)
        # TODO: Send new angle to the server
