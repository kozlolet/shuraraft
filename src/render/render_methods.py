from math import sqrt, degrees, radians, atan2, sin, cos, tan


def calculate_point_projection(screen, view_angle, yaw, pitch, player_pos, target_pos):
    player_x = player_pos[0]
    player_y = player_pos[1]
    player_z = player_pos[2]
    target_x = target_pos[0]
    target_y = target_pos[1]
    target_z = target_pos[2]

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

    if player_z > target_z:
        return

    # screen x calculate
    distance_toLeft = tan(view_angle/2) * (target_z - player_pos[2]) - (player_pos[0] - target_x)
    full_flat = tan(view_angle/2) * (target_z - player_pos[2]) * 2
    E_toLeft = distance_toLeft / full_flat
    target_screen_x = screen.get_width() * E_toLeft

    # screen y calculate
    distance_toUp = tan(view_angle/2) * (target_z - player_pos[2]) - (target_y - player_pos[1])
    full_flat = tan(view_angle/2) * (target_z - player_pos[2]) * 2
    E_toUp = distance_toUp / full_flat
    target_screen_y = screen.get_height() * E_toUp

    return target_screen_x, target_screen_y


def sort_polygons_by_distance(polygons, player_pos):
    def get_polygon_center(polygon_points):
        if not polygon_points:
            return player_pos

        sum_x = sum(v[0] for v in polygon_points)
        sum_y = sum(v[1] for v in polygon_points)
        sum_z = sum(v[2] for v in polygon_points)
        n = len(polygon_points)

        return [sum_x / n, sum_y / n, sum_z / n]

    def distance_to_player(polygons):
        center = get_polygon_center(polygons)

        return ((center[0] - player_pos[0])**2 +
                (center[1] - player_pos[1])**2 +
                (center[2] - player_pos[2])**2)

    return sorted(polygons, key=distance_to_player, reverse=True)


def sort_blocks_by_distance(blocks, player_pos):
    get_block_center = lambda block: [block.x + 0.5, block.y + 0.5, block.z + 0.5]

    def distance_to_player(block):
        center = get_block_center(block)

        return ((center[0] - player_pos[0])**2 +
                (center[1] - player_pos[1])**2 +
                (center[2] - player_pos[2])**2)

    return sorted(blocks, key=distance_to_player, reverse=True)