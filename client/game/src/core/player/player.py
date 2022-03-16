import pygame

from client.game.src.utils.sprite import TankSprite


class Player:
    def __init__(self, screen, game, id: int, position=None):
        if position is None:
            position = (400, 400)
        self.screen = screen
        self.game = game
        self.map = game.map
        self.tank = None
        self.id = id
        self.position = position
        self.angle = 0
        self.points = 0
        self.bullets = 5
        self.reload = 0
        self.create_tank()

    def create_tank(self):
        tank = pygame.image.load('assets/textures/tank' + str(self.id) + '.png')

        (w, h) = self.screen.get_size()
        width = w / self.map.width
        height = h / self.map.height

        self.tank = TankSprite(self.position, pygame.transform.scale(tank, (width, height)))

    def draw(self):
        self.game.refresh_ground()

        self.screen.blit(self.tank.image, self.tank.rect)
        pygame.draw.rect(self.screen, (255, 0 ,0), (self.tank.rect.x, self.tank.rect.y, self.tank.rect.width, self.tank.rect.height), 2)
        # tank_copy = pygame.transform.rotate(self.tank, -self.angle)
        # x, y = self.position
        # new_position = [x - int(tank_copy.get_width() / 2), y - int(tank_copy.get_height() / 2)]
        # self.screen.blit(tank_copy, new_position)
        # print(tank_copy.get_rect())
        pygame.display.update()
        pass

    def _wall_collide(self):
        return len(pygame.sprite.spritecollide(self.tank, self.map.walls, False)) == 0

    def move(self, position):
        self.tank.move(position)
        if self._wall_collide():
            self.position = position
            self.draw()
        else:
            self.tank.move(self.position)
        # TODO: Emit information to the server
        pass

    def rotate(self, angle):
        self.tank.rotate(self.angle + angle)
        if self._wall_collide():
            self.angle += angle
            self.draw()
        else:
            self.tank.rotate(self.angle)
        # TODO: Emit information to the server
        pass

    def shot(self):
        if self.bullets > 0:
            self.bullets -= 1

            # TODO: Create bullet & emit information to the server
        else:
            print('You don`t have enough bullets in your magazine')

