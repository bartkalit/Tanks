import sys
from enum import Enum
from heapq import *
from math import cos, sin, pi
import random

import numpy as np
import pygame
import copy

from client.game.src.core.bot.a_star import A_Star
from client.game.src.core.bot.maze import Maze, path_from
from client.game.src.core.stat_bar.stat_bar import StatBar
from client.game.src.utils.config import Config

class Drive(Enum):
    FORWARD = 0
    BACKWARD = 1


class Rotate(Enum):
    LEFT = 0
    RIGHT = 1


class ExpectRotate(float, Enum):
    UP = 270
    DOWN = 90
    LEFT = 180
    RIGHT = 0


class DirectionAngle(float, Enum):
    UP = 90
    DOWN = 270
    LEFT = 180
    RIGHT = 0


class BotController:
    SHOT_DISTANCE = 30
    ANGLE_OFFSET = 1
    POS_OFFSET = 10

    def __init__(self, screen, game, player):
        self.screen = screen
        self.game = game
        self.player = player
        self.map = self.read_map(game.map.data)
        self.node = None
        self.x = 0
        self.y = 0
        self.glitch_time = 0
        self.enemy = self.find_closest_player()

    def distance(self, player):
        return abs(self.player.position[0] - player.position[0]) + abs(self.player.position[1] - player.position[1])

    def find_closest_player(self):
        minDistance = sys.maxsize
        minPlayer = None

        for player in self.game.players:
            if player != self.player:
                if minDistance > self.distance(player):
                    minDistance = self.distance(player)
                    minPlayer = player
        return minPlayer

    def read_map(self, map):
        # for i in range(len(map)):
        #     print(map[i])
        for i in range(len(map)):
            map[i] = list(map[i])
            for j in range(len(map[i])):
                if map[i][j] == 'S':
                    map[i][j] = '.'

        return map

    def astar(self, maze):
        start_node = maze.find_node('S')
        self.node = (start_node.x, start_node.y)
        start_node.visited = True
        end_node = maze.find_node('E')
        start_node.cost = abs(end_node.x - start_node.x) + abs(end_node.y - start_node.y)
        q = []
        id = 0
        heappush(q, (start_node.cost, id, start_node))
        while q:
            node = heappop(q)[2]  # LIFO
            node.visited = True
            if node.type == 'E':
                return path_from(node)

            children = maze.get_possible_movements(node)
            for child in children:
                if not child.visited:
                    child.parent = node
                    child.moves_cost = node.moves_cost + maze.move_cost(child)
                    child.cost = abs(end_node.x - child.x) + abs(end_node.y - child.y) + child.moves_cost
                    id += 1
                    heappush(q, (child.cost, id, child))

        return None

    def find_path(self):
        # player = self.find_closest_player()  # gdyby bylo wiecej graczy trzeba uzywac tej metody
        player = self.enemy
        new_map = copy.deepcopy(self.map)
        width = self.game.assets.width
        height = self.game.assets.height

        self.x = int(self.player.position[0] / width)
        self.y = int(self.player.position[1] / height)

        new_map[self.y][self.x] = 'S'
        x2 = int(player.position[0] / width)
        y2 = int(player.position[1] / height)
        new_map[y2][x2] = 'E'

        if (self.x, self.y) == (x2, y2):
            return None, None, 0
        maze = Maze(new_map)
        maze.path = self.astar(maze)
        # maze.draw()

        act = maze.path[len(maze.path) - 1]
        new = maze.path[len(maze.path) - 2]
        return (act.x, act.y), (new.x, new.y), len(maze.path)

    def move(self):
        if self.enemy.is_alive():
            actual_point, new_point, length = self.find_path()
            if actual_point:
                if actual_point[1] < new_point[1]:
                    return length, ExpectRotate.UP
                if actual_point[1] > new_point[1]:
                    return length, ExpectRotate.DOWN
                if actual_point[0] < new_point[0]:
                    return length, ExpectRotate.RIGHT
                if actual_point[0] > new_point[0]:
                    return length, ExpectRotate.LEFT
        return 0, self.player.angle  # stay

    def move2(self):
        moves = []
        actual_point = ""
        if self.enemy.is_alive():
            actual_point, new_point, length = self.find_path()
            if actual_point:
                if not (actual_point[1] < new_point[1]) and self.map[actual_point[0]][actual_point[1] - 1] != "#":
                   moves.append([length, DirectionAngle.DOWN])
                if not (actual_point[1] > new_point[1]) and self.map[actual_point[0]][actual_point[1] + 1] != "#":
                    print(self.map[actual_point[0]][actual_point[1] - 1])
                    moves.append([length, DirectionAngle.UP])
                if not (actual_point[0] < new_point[0]) and self.map[actual_point[0] - 1][actual_point[1]] != "#":
                    moves.append([length, DirectionAngle.RIGHT])
                if not (actual_point[0] > new_point[0]) and self.map[actual_point[0] + 1][actual_point[1]] != "#":
                    moves.append([length, DirectionAngle.LEFT])
        print(actual_point, new_point, moves)
        if len(moves):
            for angle in list(zip(*moves))[1]:
                if angle - 1 < self.player.angle < angle + 1:
                    #print("1")
                    return 0, self.player.angle  # stay

            r = random.randrange(0, len(moves), 1)
            #print("2")
            return moves[r][0], moves[r][1]
        #print("3")
        return 0, self.player.angle  # stay


    def shot_condition(self, length):
        """
        Checks if enemy is in a straight line with a bot and if bot faces the enemy
        :param int length: Length of a shortest path between bot and an enemy in a number of tiles
        :return: If bot is supposed to shot
        :rtype: bool
        """
        e_x, e_y = self.enemy.position
        b_x, b_y = self.player.position
        b_angle = self.player.angle
        if length < self.SHOT_DISTANCE:
            if b_x - self.POS_OFFSET <= e_x <= b_x + self.POS_OFFSET:
                # enemy above
                if b_y > e_y:
                    if DirectionAngle.UP - self.ANGLE_OFFSET <= b_angle<= DirectionAngle.UP + self.ANGLE_OFFSET:
                        return True
                # enemy below
                if b_y < e_y:
                    if DirectionAngle.DOWN - self.ANGLE_OFFSET <= b_angle <= DirectionAngle.DOWN + self.ANGLE_OFFSET:
                        return True
            elif b_y - self.POS_OFFSET <= e_y <= b_y + self.POS_OFFSET:
                # enemy on a left
                if b_x > e_x:
                    if DirectionAngle.LEFT - self.ANGLE_OFFSET <= b_angle <= DirectionAngle.LEFT + self.ANGLE_OFFSET:
                        return True
                # enemy on a right
                if b_x < e_x:
                    if DirectionAngle.RIGHT - self.ANGLE_OFFSET <= b_angle <= DirectionAngle.RIGHT + self.ANGLE_OFFSET:
                        return True
        return False

    @staticmethod
    def whole_angle(angle):
        if -45 < angle < 45:
            return 0
        elif 45 < angle < 135:
            return 90
        elif 135 < angle < 225:
            return 180
        else:
            return 270

    def on(self, time):
        if self.player.is_alive():
            self._reload(time)
            length, rotate = self.move2()
            shot = self.shot_condition(length)
            angle = self.player.angle - rotate
            width = self.game.assets.width
            height = self.game.assets.height
            if angle != 0 and (-1 < self.player.angle < 1 and self.x * width > self.player.position[0] - width / 2
                               or 179 < self.player.angle < 181 and self.player.position[0] > (
                                       self.x + 1) * width - width / 2
                               or 269 < self.player.angle < 271 and self.y * height >= self.player.position[
                                   1] - height / 2
                               or 89 < self.player.angle < 91 and self.player.position[1] > (
                                       self.y + 1) * height - height / 2):
                angle = 0

            if shot:
                self.shot()
            if angle > 1:
                self.rotate(Rotate.RIGHT, 2 * time)

            elif angle < -1:
                self.rotate(Rotate.LEFT, 2 * time)
            else:

                self.player.rotate(self.whole_angle(self.player.angle) - self.player.angle, time)
                if self.glitch_time < 0:
                    self.drive(Drive.BACKWARD, time)
                    move_value = 1
                else:
                    move_value = self.drive(Drive.FORWARD, time)

                self.glitch_time += move_value
                if self.glitch_time == 100:
                    self.glitch_time = -50
                elif move_value == 0:
                    self.glitch_time = 0

    def _reload(self, time):
        self.player.reload_time -= time
        StatBar.show_reload(self.screen, self.player)
        if self.player.reload_time <= 0:
            StatBar.show_magazine(self.screen, self.player)

    def _reload_magazine(self):
        if self.player.bullets != Config.player['tank']['magazine']:
            self.player.reload_magazine()
            self.player.reload_time = Config.player['tank']['reload_magazine']

    def drive(self, drive: Drive, time):
        x, y = self.player.position
        radians = -self.player.angle * pi / 180
        if drive == Drive.FORWARD:
            speed = Config.player['speed']['drive']['forward'] * time
            new_x = x + (speed * cos(radians))
            new_y = y + (speed * sin(radians))
        else:
            speed = Config.player['speed']['drive']['backward'] * time
            new_x = x - (speed * cos(radians))
            new_y = y - (speed * sin(radians))

        new_position = (new_x, new_y)

        self.player.move(new_position)
        if (x, y) == self.player.position:
            return 1
        else:
            return 0
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

        self.player.rotate(new_angle, 1)
        # TODO: Send new angle to the server

    def shot(self):
        if self.player.reload_time <= 0:
            self.player.reload_time = Config.player['tank']['reload_bullet']
            self.player.shot()
            StatBar.show_magazine(self.screen, self.player)
            if self.player.bullets == 0:
                self._reload_magazine()
            # TODO: Send bullet position to the server
