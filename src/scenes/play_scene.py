import time

import pygame
from src.entities.player import Player
from src.world import World

class PlayScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(self)
        self.world = World(self)
        self.world.load_world()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.game.running = False

            self.player.mouse_handle(event)

    def update(self) -> None:
        self.player.update()

    def draw(self) -> None:
        self.world.draw()





polygons_data = [
    [[[-1, -1, 3], [-1, 1, 3], [1, 1, 3]], (255, 0, 0)],
    [[[-1, -1, 3], [1, -1, 3], [1, 1, 3]], (255, 0, 0)],

    [[[1, 1, 3], [1, 1, 4], [1, -1, 4]], (0, 255, 0)],
    [[[1, 1, 3], [1, -1, 3], [1, -1, 4]], (0, 255, 0)],

    [[[-1, 1, 3], [-1, 1, 4], [-1, -1, 4]], (0, 255, 0)],
    [[[-1, 1, 3], [-1, -1, 3], [-1, -1, 4]], (0, 255, 0)],

    [[[-1, -1, 4], [-1, 1, 4], [1, 1, 4]], (255, 255, 0)],
    [[[-1, -1, 4], [1, -1, 4], [1, 1, 4]], (255, 255, 0)],
]