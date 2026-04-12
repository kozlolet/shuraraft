import pygame
from src.config import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from src.scenes.play_scene import PlayScene


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.event.set_grab(True)
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.X_center = self.screen.get_width() / 2
        self.Y_center = self.screen.get_height() / 2

        self.scene = PlayScene(self)


    def run(self) -> None:
        while self.running:
            self.screen.fill(BG_COLOR)
            dt = self.clock.tick(FPS) / 1000.0

            self.scene.handle_events()
            self.scene.update()
            self.scene.draw()
            pygame.display.flip()

        pygame.quit()


