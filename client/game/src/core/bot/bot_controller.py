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


class BotController:
    def __init__(self, screen, game, player):
        self.screen = screen
        self.game = game
        self.player = player
        self.map = self.read_map(game.map.data)

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
        start_node.visited = True
        end_node = maze.find_node('E')
        # fscore = {start_node:abs(end_node.x - start_node.x) + abs(end_node.y - start_node.y)}
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
                    # fscore[child] = maze.move_cost(child) + abs(end_node.x - child.x) + abs(end_node.y - child.y)
                    id += 1
                    heappush(q, (child.cost, id, child))

        return None

    def find_path(self):
        player = self.find_closest_player()

        new_map = copy.deepcopy(self.map)

        x = int(self.player.position[0] / self.game.assets.width)
        y = int(self.player.position[1] / self.game.assets.height)

        new_map[y][x] = 'S'
        x = int(player.position[0] / self.game.assets.width)
        y = int(player.position[1] / self.game.assets.height)
        new_map[y][x] = 'E'
        f = open("assets/maps/maze.txt", "w")

        for i in range(len(new_map)):
            for j in range(len(new_map[i])):
                    f.write(str(new_map[i][j]))
            f.write("\n")
        f.close()


        maze = Maze("assets/maps/maze.txt")
        maze.path = self.astar(maze)
        #maze.draw()
        #print('path length: ', len(maze.path))
        #for node in maze.path:
         #   print(f'({node.x}, {node.y})', end=' ')
        #print()

    def on(self, time):
        if self.player.is_alive():
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
                self.shot()
            if keys[pygame.K_r]:
                self._reload_magazine()
            if self.player.reload_time > 0:
                self._reload(time)

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

    def shot(self):
        if self.player.reload_time <= 0:
            self.player.reload_time = Config.player['tank']['reload_bullet']
            self.player.shot()
            StatBar.show_magazine(self.screen, self.player)
            if self.player.bullets == 0:
                self._reload_magazine()
            # TODO: Send bullet position to the server
