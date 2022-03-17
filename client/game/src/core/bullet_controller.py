from math import sin, cos

import pygame

from client.game.src.core.bullet import Bullet
from client.game.src.utils.config import Config


class BulletController:
    def __init__(self, game):
        self.game = game
        self.bullets = []

    def add_bullet(self, position, angle):
        self.bullets.append(Bullet(self.game.screen, position, angle))

    def update_bullets(self, time):
        for bullet in self.bullets:
            self.move(bullet, time)
            bullet.draw()

    def move(self, bullet, time):
        speed = Config.bulllet['speed'] * time
        x, y = bullet.position
        # sin i cos moga być odwrotnie
        new_x = x + speed * sin(bullet.angle)
        new_y = y + speed * cos(bullet.angle)
        bullet.move((new_x, new_y))