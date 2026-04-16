from math import sqrt, degrees, radians, atan2, sin, cos, tan
import pygame
from src.render.blocks_id import blocks_id
from src.config import WIDTH, HEIGHT


def calculate_point_projection(screen, view_angle, yaw, pitch, player_pos, target_pos):
    player_x = player_pos[0]
    player_y = player_pos[1]
    player_z = player_pos[2]
    target_x = target_pos[0]
    target_y = target_pos[1]
    target_z = target_pos[2]
    aspect = screen.get_width()/screen.get_height()

    # edit by Y rotate
    XZ_distance = sqrt(  (target_x - player_x)**2 + (target_z - player_z)**2  )
    Y_relative_angle = degrees(atan2(target_x - player_x, target_z - player_z))

    target_x += XZ_distance * sin(radians(Y_relative_angle + yaw)) - (target_x - player_x)
    target_y += 0
    target_z -= (target_z - player_z) - XZ_distance*cos(radians(Y_relative_angle + yaw))

    # edit by X rotate
    YZ_distance = sqrt(  (target_y - player_y)**2 + (target_z - player_z)**2  )
    X_relative_angle = degrees(atan2(target_y - player_y, target_z - player_z))

    target_x += 0
    target_y += YZ_distance * sin(radians(X_relative_angle + pitch)) - (target_y - player_y)
    target_z -= (target_z - player_z) - YZ_distance*cos(radians(X_relative_angle + pitch))

    if player_z >= target_z-0.01:
        return

    # screen x calculate
    distance_toLeft = tan(radians(view_angle)/2) * (target_z - player_pos[2]) - (player_pos[0] - target_x)
    full_flat = tan(radians(view_angle)/2) * (target_z - player_pos[2]) * 2
    E_toLeft = distance_toLeft / full_flat
    target_screen_x = screen.get_width() * E_toLeft

    view_angle_vertical = degrees(  2 * atan2( tan( radians(view_angle)/2 ), aspect )  )
    # screen y calculate
    distance_toUp = tan(radians(view_angle_vertical)/2) * (target_z - player_pos[2]) - (target_y - player_pos[1])
    full_flat = tan(radians(view_angle_vertical)/2) * (target_z - player_pos[2]) * 2
    E_toUp = distance_toUp / full_flat
    target_screen_y = screen.get_height() * E_toUp

    return target_screen_x, target_screen_y


def split_block_on_polygons(block):
    world = block.chunk.world

    x = block.x + 16*block.chunk.x  # absolute
    y = block.y                     # absolute
    z = block.z + 16*block.chunk.z  # absolute

    polygons = []

    # -Z face
    if not world.get_block_id(x, y, z-1):
        polygons.append([[x+1, y, z], [x, y+1, z], [x, y, z]])
        polygons.append([[x+1, y, z], [x, y+1, z], [x+1, y+1, z]])

    # -X face
    if not world.get_block_id(x-1, y, z):
        polygons.append([[x, y, z], [x, y+1, z+1], [x, y, z+1]])
        polygons.append([[x, y, z], [x, y+1, z+1], [x, y+1, z]])

    # +X face
    if not world.get_block_id(x+1, y, z):
        polygons.append([[x+1, y+1, z], [x+1, y, z+1], [x+1, y, z]])
        polygons.append([[x+1, y+1, z], [x+1, y, z+1], [x+1, y+1, z+1]])

    # +Z face
    if not world.get_block_id(x, y, z+1):
        polygons.append([[x, y+1, z+1], [x+1, y, z+1], [x, y, z+1]])
        polygons.append([[x, y+1, z+1], [x+1, y, z+1], [x+1, y+1, z+1]])

    # -Y face
    if not world.get_block_id(x, y-1, z):
        polygons.append([[x, y, z+1], [x+1, y, z], [x, y, z]])
        polygons.append([[x, y, z+1], [x+1, y, z], [x+1, y, z+1]])

    # +Y face
    if not world.get_block_id(x, y+1, z):
        polygons.append([[x, y+1, z+1], [x+1, y+1, z], [x, y+1, z]])
        polygons.append([[x, y+1, z+1], [x+1, y+1, z], [x+1, y+1, z+1]])

    return [{'polygon': polygon, 'id': block.id} for polygon in polygons]


def chunk_polygons_render(chunk, polygons):
    play_scene = chunk.world.play_scene
    player_x = play_scene.player.x
    player_y = play_scene.player.y
    player_z = play_scene.player.z
    yaw = play_scene.player.yaw
    pitch = play_scene.player.pitch
    view_angle = play_scene.player.view_angle

    sorted_polygons = sort_polygons(polygons, (player_x, player_y, player_z))

    for polygon in sorted_polygons:
        polygon_screen = []
        skip = False
        polygon_color = blocks_id[polygon['id']]
        for point in polygon['polygon']:
            screen_coords = calculate_point_projection(screen=play_scene.game.screen,
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
            pygame.draw.polygon(play_scene.game.screen, polygon_color, polygon_screen)


def sort_polygons(polygons, player_pos):
    def get_polygon_center(polygon_points):
        if not polygon_points:
            return player_pos

        sum_x = sum(v[0] for v in polygon_points)
        sum_y = sum(v[1] for v in polygon_points)
        sum_z = sum(v[2] for v in polygon_points)
        n = len(polygon_points)

        return [sum_x / n, sum_y / n, sum_z / n]

    def distance_to_player(polygon):
        center = get_polygon_center(polygon['polygon'])

        return ((center[0] - player_pos[0])**2 +
                (center[1] - player_pos[1])**2 +
                (center[2] - player_pos[2])**2)

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


