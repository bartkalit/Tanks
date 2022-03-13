import pygame


class Player:
    def __init__(self, screen, game, id: int, position=None):
        if position is None:
            position = (0, 0)
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
        self.tank = pygame.image.load('assets/textures/tank' + str(self.id) + '.png')

        (w, h) = self.screen.get_size()
        width = w / self.map.width
        height = h / self.map.height

        self.tank = pygame.transform.scale(self.tank, (width, height))

    def draw(self):
        self.game.show_map()
        tank = pygame.transform.rotate(self.tank, -self.angle)
        self.screen.blit(tank, self.position)
        pygame.display.update()
        pass

    def move(self, position):
        self.position = position
        self.draw()
        # TODO: Emit information to the server
        pass

    def rotate(self, angle):
        self.angle += angle
        self.draw()
        # TODO: Emit information to the server
        pass

    def shot(self):
        if self.bullets > 0:
            self.bullets -= 1

            # TODO: Create bullet & emit information to the server
        else:
            print('You don`t have enough bullets in your magazine')

