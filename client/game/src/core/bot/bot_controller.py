import sys
from enum import Enum
from heapq import *
from math import cos, sin, pi
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
    RIGHT = 0
    LEFT = 180

class BotController:
    def __init__(self, screen, game, player):
        self.screen = screen
        self.game = game
        self.player = player
        self.map = self.read_map(game.map.data)
        self.node = None
        self.x = 0
        self.y =0
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
        for i in range(len(map)):
            print(map[i])
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
        #player = self.find_closest_player()  # gdyby bylo wiecej graczy trzeba uzywac tej metody
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
            return True, None, None
        maze = Maze(new_map)
        maze.path = self.astar(maze)
        # maze.draw()
        shot = True
        if len(maze.path) <= 5:
            for i in range(len(maze.path)):
                if self.x != maze.path[i].x:
                    shot = False
                if shot:
                    for i in range(len(maze.path)):
                        if self.y != maze.path[i].y:
                            shot = False

        act = maze.path[len(maze.path) - 1]
        new = maze.path[len(maze.path) - 2]
        return shot, (act.x, act.y), (new.x, new.y)

    def move(self):
        shot, actual_poit, new_point = self.find_path()
        if (actual_poit != None):
            if (actual_poit[1] < new_point[1]):
                return shot, ExpectRotate.UP  # up
            if (actual_poit[1] > new_point[1]):
                return shot, ExpectRotate.DOWN  # down
            if (actual_poit[0] < new_point[0]):
                return shot, ExpectRotate.RIGHT  # right
            if (actual_poit[0] > new_point[0]):
                return shot, ExpectRotate.LEFT  # left
        return shot, self.player.angle  # stay

    def on(self, time):
        if self.player.is_alive():
            shot, rotate = self.move()
            angle = self.player.angle - rotate

            '''if abs(angle) < 1:
                if rotate == 0 and self.player.position[0] <= self.node[
                    0] * self.game.assets.width + self.game.assets.width / 2 or \
                        rotate == 180 and self.player.position[0] >= self.node[
                    0] * self.game.assets.width + self.game.assets.width / 2 or \
                        rotate == 270 and self.player.position[1] <= self.node[
                    1] * self.game.assets.height + self.game.assets.height / 2 or \
                        rotate == 270 and self.player.position[1] >= self.node[
                    1] * self.game.assets.height + self.game.assets.height / 2:
                    angle = 0'''
            width = self.game.assets.width
            height = self.game.assets.height
            if angle != 0 and (-1 < self.player.angle < 1 and self.x*width > self.player.position[0] - width/2
                               or 179 < self.player.angle < 181 and self.player.position[0] > (self.x+1)*width - width/2
                               or 269 < self.player.angle < 271 and self.y*height >= self.player.position[1] - height/2
                               or 89 < self.player.angle < 91 and self.player.position[1] > (self.y+1)*height - height/2):
                angle = 0

            if angle > 1:
                self.rotate(Rotate.RIGHT, 2*time)

            elif angle < -1:
                self.rotate(Rotate.LEFT,  2*time)
            else:
                if shot:
                    self.shot()
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
