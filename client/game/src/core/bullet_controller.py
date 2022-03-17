from math import sin, cos, degrees, pi

import pygame

from client.game.src.core.bullet import Bullet
from client.game.src.utils.config import Config


class BulletController:
    def __init__(self, game):
        self.game = game
        self.bullets = []

    def add_bullet(self, position, angle):
        self.bullets.append(Bullet(self.game.screen, position, angle))

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

    def move_bullets(self, time):
        for bullet in self.bullets:
            self.move(bullet, time)

    def move(self, bullet, time):
        speed = Config.bulllet['speed'] * time
        x, y = bullet.position
        radians = -bullet.angle * pi / 180
        new_x = x + (speed * cos(radians))
        new_y = y + (speed * sin(radians))
        bullet.move((new_x, new_y))
