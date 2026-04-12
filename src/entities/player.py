import pygame
from math import cos, sin, radians
import json


class Player:
    def __init__(self, play_scene) -> None:
        self.play_scene = play_scene
        self.load_settings()

    def load_settings(self):
        with open('src/gamesettings.json', 'r') as file:
            self.settings = json.load(file)
        self.speed = self.settings['player_speed']
        self.x, self.y, self.z = self.settings['player_spawn_position']
        self.yaw, self.pitch = self.settings['player_look']
        self.view_angle = self.settings['player_view_angle']

    def save_settings(self):
        with open('gamesettings.json', 'w') as file:
            json.dump(self.settings, file)

    def mouse_handle(self, event):
        X_center = self.play_scene.game.X_center
        Y_center = self.play_scene.game.Y_center

        if hasattr(event, 'pos'):
            delta_mouse_x_pos = X_center - pygame.mouse.get_pos()[0]
            delta_mouse_y_pos = Y_center - pygame.mouse.get_pos()[1]
            if abs(delta_mouse_x_pos) >= 200 or abs(delta_mouse_y_pos) >= 200:
                pygame.mouse.set_pos(X_center, Y_center)
            else:
                self.yaw += delta_mouse_x_pos / 10
                if self.pitch < 90 and self.pitch > -90:
                    self.pitch -= delta_mouse_y_pos / 10
                else:
                    self.pitch = 89.9 if self.pitch > 0 else -89.9

                pygame.mouse.set_pos(X_center, Y_center)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.z += self.speed*cos(radians(self.yaw + 90))
            self.x -= self.speed*sin(radians(self.yaw + 90))
        if keys[pygame.K_d]:
            self.z -= self.speed*cos(radians(self.yaw + 90))
            self.x += self.speed*sin(radians(self.yaw + 90))
        if keys[pygame.K_s]:
            self.z -= self.speed*cos(radians(self.yaw))
            self.x += self.speed*sin(radians(self.yaw))
        if keys[pygame.K_w]:
            self.z += self.speed*cos(radians(self.yaw))
            self.x -= self.speed*sin(radians(self.yaw))
        if keys[pygame.K_SPACE]:
            self.y += self.speed
        if keys[pygame.K_LSHIFT]:
            self.y -= self.speed
        if keys[pygame.K_LEFT]:
            self.yaw += 1
        if keys[pygame.K_RIGHT]:
            self.yaw -= 1
        if keys[pygame.K_UP]:
            self.pitch -= 1
        if keys[pygame.K_DOWN]:
            self.pitch += 1

    def draw(self, screen) -> None:
        pass