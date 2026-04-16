import time
from src.text import Text
import pygame
from src.entities.player import Player
from src.world import World

class PlayScene:
    def __init__(self, game, world_name):
        self.game = game
        self.world_name = world_name
        self.world = World(self)
        self.player = Player(self)
        self.texts = []

        self._f3_on = False
        self._font_f3 = pygame.font.Font(None, 32)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self._f3_on = False if self._f3_on else True
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

            self.player.mouse_handle(event)

    def update(self) -> None:
        self.player.handle_events()
        self.player.update()
        if self._f3_on:
            self.f3()

    def f3(self):
        height = self._font_f3.get_height()

        def add_text(text):
            offset = len(self.texts)*height
            text = self._font_f3.render(text, True, '#ffffff')
            text_obj = Text(self, text, 0, offset)
            self.texts.append(text_obj)

        add_text(f'X: {self.player.x}')
        add_text(f'Y: {self.player.y}')
        add_text(f'Z: {self.player.z}')
        add_text(f'yaw: {self.player.yaw}')
        add_text(f'pitch: {self.player.pitch}')


    def draw(self) -> None:
        self.world.draw()

        for text in self.texts:
            text.draw()
        self.texts = []

    def stop(self):
        self.player.save_settings()
        self.world.save_settings()





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