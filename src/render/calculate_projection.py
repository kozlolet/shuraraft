from math import sqrt, degrees, radians, cos, sin, tan, atan2


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


def calculate_screen_polygon(screen, player, polygon_pos):
    screen_vertexes = []
    for vertex in polygon_pos:
        screen_vertex = calculate_point_projection(
            screen=screen,
            view_angle=player.view_angle,
            yaw=player.yaw,
            pitch=player.pitch,
            player_pos=[player.x, player.y, player.z],
            target_pos=vertex
        )
        if screen_vertex:
            screen_vertexes.append(screen_vertex)
        else:
            return

    return screen_vertexes
