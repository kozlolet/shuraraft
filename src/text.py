class Text:
    def __init__(self, play_scene, text, x, y):
        self.play_scene = play_scene
        self.screen = play_scene.game.screen
        self.text = text
        self.x = x
        self.y = y

    def draw(self):
        self.screen.blit(self.text, (self.x, self.y))
