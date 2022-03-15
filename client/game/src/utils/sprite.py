import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)


class TankSprite(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self._image = image
        self._position = position
        self.rect = self.image.get_rect(center=position)

    def move(self, position):
        self._position = position
        self.rect = self.image.get_rect(center=position)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self._image, angle)
        self.rect = self.image.get_rect(center=self._position)