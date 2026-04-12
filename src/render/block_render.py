from math import sqrt, degrees, radians, atan2, sin, cos, tan
import pygame
from src.render.render_methods import *
from src.render.blocks_ids import block_ids
from src.config import WIDTH, HEIGHT


def split_block_on_polygons(x, y, z):
    polygons = [
        [[x+1, y, z], [x, y+1, z], [x, y, z]],
        [[x+1, y, z], [x, y+1, z], [x+1, y+1, z]],

        [[x, y, z], [x, y+1, z+1], [x, y, z+1]],
        [[x, y, z], [x, y+1, z+1], [x, y+1, z]],

        [[x+1, y+1, z], [x+1, y, z+1], [x+1, y, z]],
        [[x+1, y+1, z], [x+1, y, z+1], [x+1, y+1, z+1]],

        [[x, y+1, z+1], [x+1, y, z+1], [x, y, z+1]],
        [[x, y+1, z+1], [x+1, y, z+1], [x+1, y+1, z+1]],

        [[x, y, z+1], [x+1, y, z], [x, y, z]],
        [[x, y, z+1], [x+1, y, z], [x+1, y, z+1]],

        [[x, y+1, z+1], [x+1, y+1, z], [x, y+1, z]],
        [[x, y+1, z+1], [x+1, y+1, z], [x+1, y+1, z+1]],
    ]
    return polygons


class BlockRender:
    def __init__(self, block):
        self.block = block

    def split_block_on_polygons(self):
        x = self.block.x
        y = self.block.y
        z = self.block.z
        return [
            [[x+1, y, z], [x, y+1, z], [x, y, z]],
            [[x+1, y, z], [x, y+1, z], [x+1, y+1, z]],

            [[x, y, z], [x, y+1, z+1], [x, y, z+1]],
            [[x, y, z], [x, y+1, z+1], [x, y+1, z]],

            [[x+1, y+1, z], [x+1, y, z+1], [x+1, y, z]],
            [[x+1, y+1, z], [x+1, y, z+1], [x+1, y+1, z+1]],

            [[x, y+1, z+1], [x+1, y, z+1], [x, y, z+1]],
            [[x, y+1, z+1], [x+1, y, z+1], [x+1, y+1, z+1]],

            [[x, y, z+1], [x+1, y, z], [x, y, z]],
            [[x, y, z+1], [x+1, y, z], [x+1, y, z+1]],

            [[x, y+1, z+1], [x+1, y+1, z], [x, y+1, z]],
            [[x, y+1, z+1], [x+1, y+1, z], [x+1, y+1, z+1]],
        ]

    def block_polygons_render(self):
        player_x = self.block.world.play_scene.player.x
        player_y = self.block.world.play_scene.player.y
        player_z = self.block.world.play_scene.player.z
        yaw = self.block.world.play_scene.player.yaw
        pitch = self.block.world.play_scene.player.pitch
        view_angle = self.block.world.play_scene.player.view_angle
        block_color = block_ids[self.block.id]

        polygons = split_block_on_polygons(self.block.x, self.block.y, self.block.z)
        sorted_polygons = sort_polygons_by_distance(polygons, (player_x, player_y, player_z))


        for polygon in sorted_polygons:
            polygon_screen = []
            skip = False
            for point in polygon:
                screen_coords = calculate_point_projection(screen=self.block.world.play_scene.game.screen,
                                                           view_angle=view_angle,
                                                           yaw=yaw, pitch=pitch,
                                                           player_pos=(player_x, player_y, player_z),
                                                           target_pos=point)
                if not screen_coords:
                    skip = True
                    continue
                polygon_screen.append(screen_coords)

            if skip:
                continue

            out_screen_polygon = True
            for point_screen in polygon_screen:
                if point_screen[0] > 0 and point_screen[0] < WIDTH:
                    out_screen_polygon = False
                elif point_screen[1] > 0 and point_screen[1] < HEIGHT:
                    out_screen_polygon = False

            if not out_screen_polygon:
                pygame.draw.polygon(self.block.world.play_scene.game.screen, block_color, polygon_screen)



