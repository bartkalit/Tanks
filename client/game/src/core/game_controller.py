import pygame

from client.game.src.core.game import Game
from client.game.src.core.player.player import Player
from client.game.src.core.player.player_controller import PlayerController
from client.game.src.utils.config import Config


class GameController:
    def __init__(self, screen):
        self.screen = screen

        self.game = Game(screen)
        self.game.load_assets()
        self.game.refresh_map()
        self.current_player = None

    def join(self):
        players = self.game.players
        player = Player(self.screen, self.game, len(players) + 1, ((len(players) + 1) * 100, (len(players) + 1) * 100))
        print(self.current_player)
        if self.current_player is None:
            self.current_player = PlayerController(player)
        self.game.add_player(player)

    def start(self):
        self.game.refresh_map()
        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            frame_time = clock.tick(Config.game['fps'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.game.refresh_bullets(frame_time / 1000)
            self.current_player.on(frame_time / 1000)
            pygame.display.set_caption('FurryTanks - %.2f FPS' % clock.get_fps())