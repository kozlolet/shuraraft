from math import sqrt, degrees, radians, atan2, sin, cos, tan, floor
import pygame
from src.render.blocks_id import blocks_id
from src.config import WIDTH, HEIGHT
from src.render.calculate_projection import calculate_screen_polygon
from src.render.UV import draw_texture_pixels
import numpy


def chunk_polygons_render(chunk, polygons):
    play_scene = chunk.world.play_scene
    screen = play_scene.game.screen
    textures = chunk.world.textures
    player = play_scene.player

    distance_sorted_polygons = sort_polygons_by_distance(polygons, player)
    arr = pygame.surfarray.pixels3d(screen)

    for polygon in distance_sorted_polygons:
        polygon_texture = textures[blocks_id[polygon['id']][0]]
        polygon_color = blocks_id[polygon['id']][1]

        view_faces = get_faces_that_the_player_sees(player, polygon['polygon']['pos'])
        if polygon['face_dir'] not in view_faces:
            continue

        polygon_screen = calculate_screen_polygon(screen, player, polygon['polygon']['pos'])
        if not polygon_screen:
            continue

        out_screen_polygon = True
        for point_screen in polygon_screen:
            if 0 < point_screen[0] < WIDTH:
                out_screen_polygon = False
            elif 0 < point_screen[1] < HEIGHT:
                out_screen_polygon = False

        if out_screen_polygon:
            continue

        if distance_to_polygon(player, polygon['polygon']['pos']) <= player.settings['texturing_distance']:
            quality = player.settings['texture_step']
            if player.settings['dynamic_texture_step']:
                quality = automatic_quality_by_distance(player, polygon['polygon']['pos'])

            draw_texture_pixels(screen=screen,
                                arr=arr,
                                texture=polygon_texture,
                                quality=quality,
                                vertexes=polygon_screen,
                                uv=polygon['polygon']['uv'])
        else:
            pygame.draw.polygon(screen, polygon_color, polygon_screen)
    del arr




def sort_polygons_by_distance(polygons, player):
    def distance_to_player(polygon):
        center = get_polygon_center(polygon['polygon']['pos'])

        return ((center[0] - player.x)**2 +
                (center[1] - player.y)**2 +
                (center[2] - player.z)**2)

    return sorted(polygons, key=distance_to_player, reverse=True)


def sort_chunks_by_distance(chunks, player_pos):
    def get_chunk_center(chunk):
        absolute_chunk_x = 16*chunk.x
        absolute_chunk_z = 16*chunk.z

        return [absolute_chunk_x+8, absolute_chunk_z+8]

    def distance_to_player(chunk):
        center = get_chunk_center(chunk)

        return ((center[0] - player_pos[0])**2 +
                (center[1] - player_pos[1])**2)

    return sorted(chunks, key=distance_to_player, reverse=True)


def distance_to_polygon(player, polygon_vertexes):
    polygon_center = get_polygon_center(polygon_vertexes)
    return ((polygon_center[0] - player.x)**2 +
            (polygon_center[1] - player.y)**2 +
            (polygon_center[2] - player.z)**2)


def automatic_quality_by_distance(player, polygon_vertexes):
    distance = distance_to_polygon(player, polygon_vertexes)

    texture_step = floor(1000/distance)+1

    texture_step = 16 if texture_step > 16 else texture_step
    texture_step = 1 if texture_step < 1 else texture_step

    return texture_step


def get_polygon_center(polygon_vertexes):
    sum_x = sum(v[0] for v in polygon_vertexes)
    sum_y = sum(v[1] for v in polygon_vertexes)
    sum_z = sum(v[2] for v in polygon_vertexes)
    n = len(polygon_vertexes)

    return [sum_x / n, sum_y / n, sum_z / n]


def get_faces_that_the_player_sees(player, polygon_vertexes):
    # return what parts of the block does the player see

    polygon_center = get_polygon_center(polygon_vertexes)

    view_faces = []
    if player.x > polygon_center[0]:
        view_faces.append('+x')
    else:
        view_faces.append('-x')

    if player.y > polygon_center[1]:
        view_faces.append('+y')
    else:
        view_faces.append('-y')

    if player.z > polygon_center[2]:
        view_faces.append('+z')
    else:
        view_faces.append('-z')

    return view_faces







