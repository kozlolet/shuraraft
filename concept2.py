import pygame
from math import sqrt, sin, cos, tan, radians, degrees, atan

# pygame setup
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True
pygame.event.set_grab(True)

X_center = screen.get_width() / 2
Y_center = screen.get_height() / 2

pygame.mouse.set_pos(X_center, Y_center)

def sort_polygons_by_distance(polygons_data, player_pos):
    polygons = polygons_data

    def get_polygon_center(polygon_points):
        if not polygon_points:
            return player_pos

        sum_x = sum(v[0] for v in polygon_points)
        sum_y = sum(v[1] for v in polygon_points)
        sum_z = sum(v[2] for v in polygon_points)
        n = len(polygon_points)

        return [sum_x / n, sum_y / n, sum_z / n]

    def distance_to_player(polygon_data):
        center = get_polygon_center(polygon_data[0])

        return ((center[0] - player_pos[0])**2 +
                (center[1] - player_pos[1])**2 +
                (center[2] - player_pos[2])**2)

    return sorted(polygons, key=distance_to_player, reverse=True)

def calculate_point_projection(view_angle, Y_angle, X_angle, player_pos, target_pos):
    # if target_pos[2] < player_pos[2]:
    #     return

    player_x = player_pos[0]
    player_y = player_pos[1]
    player_z = player_pos[2]
    target_x = target_pos[0]
    target_y = target_pos[1]
    target_z = target_pos[2]

    # edit by Y rotate
    XZ_distance = sqrt(  (target_x - player_x)**2 + (target_z - player_z)**2  )
    Y_relative_angle = degrees(atan(  (target_x - player_x)/(target_z - player_z)  ))

    target_x += XZ_distance*sin(radians( Y_relative_angle+Y_angle )) - (target_x - player_x)
    target_y += 0
    target_z -= (target_z - player_z) - XZ_distance*cos(radians( Y_relative_angle+Y_angle ))

    # edit by X rotate
    YZ_distance = sqrt(  (target_y - player_y)**2 + (target_z - player_z)**2  )
    X_relative_angle = degrees(atan(  (target_y - player_y)/(target_z - player_z)  ))

    target_x += 0
    target_y += YZ_distance*sin(radians( X_relative_angle+X_angle )) - (target_y - player_y)
    target_z -= (target_z - player_z) - YZ_distance*cos(radians( X_relative_angle+X_angle ))

    # screen x calculate
    distance_toLeft = tan(view_angle/2) * (target_z - player_pos[2]) - (player_pos[0] - target_x)
    full_flat = tan(view_angle/2) * (target_z - player_pos[2]) * 2
    E_toLeft = distance_toLeft / full_flat if full_flat else 1
    target_screen_x = screen.get_width() * E_toLeft

    # screen y calculate
    distance_toUp = tan(view_angle/2) * (target_z - player_pos[2]) - (target_y - player_pos[1])
    full_flat = tan(view_angle/2) * (target_z - player_pos[2]) * 2
    E_toUp = distance_toUp / full_flat if full_flat else 1
    target_screen_y = screen.get_height() * E_toUp

    return target_screen_x, target_screen_y


polygons_data = [
    [[[-1, -1, 3], [-1, 1, 3], [1, 1, 3]], (255, 0, 0)],
    [[[-1, -1, 3], [1, -1, 3], [1, 1, 3]], (255, 0, 0)],

    [[[1, 1, 3], [1, 1, 4], [1, -1, 4]], (0, 255, 0)],
    [[[1, 1, 3], [1, -1, 3], [1, -1, 4]], (0, 255, 0)],

    [[[-1, 1, 3], [-1, 1, 4], [-1, -1, 4]], (0, 255, 0)],
    [[[-1, 1, 3], [-1, -1, 3], [-1, -1, 4]], (0, 255, 0)],

    [[[-1, -1, 4], [-1, 1, 4], [1, 1, 4]], (255, 255, 0)],
    [[[-1, -1, 4], [1, -1, 4], [1, 1, 4]], (255, 255, 0)],
    # [[], [], []],
]

speed = 0.2
player_pos = [0, 0, 0]
view_angle = 90
Y_angle = 0
X_angle = 0

while running:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_a]:
        player_pos[2] += speed*cos(radians(Y_angle + 90))
        player_pos[0] -= speed*sin(radians(Y_angle + 90))
    if keys[pygame.K_d]:
        player_pos[2] -= speed*cos(radians(Y_angle + 90))
        player_pos[0] += speed*sin(radians(Y_angle + 90))
    if keys[pygame.K_s]:
        player_pos[2] -= speed*cos(radians(Y_angle))
        player_pos[0] += speed*sin(radians(Y_angle))
    if keys[pygame.K_w]:
        player_pos[2] += speed*cos(radians(Y_angle))
        player_pos[0] -= speed*sin(radians(Y_angle))
    if keys[pygame.K_SPACE]:
        player_pos[1] += speed
    if keys[pygame.K_LSHIFT]:
        player_pos[1] -= speed
    if keys[pygame.K_LEFT]:
        Y_angle += 1
    if keys[pygame.K_RIGHT]:
        Y_angle -= 1
    if keys[pygame.K_UP]:
        X_angle += 1
    if keys[pygame.K_DOWN]:
        X_angle -= 1

    if hasattr(event, 'pos'):
        delta_mouse_x_pos = X_center - pygame.mouse.get_pos()[0]
        delta_mouse_y_pos = Y_center - pygame.mouse.get_pos()[1]
        if abs(delta_mouse_x_pos) >= 200 or abs(delta_mouse_y_pos) >= 200:
            pygame.mouse.set_pos(X_center, Y_center)
            continue
        Y_angle += delta_mouse_x_pos / 10
        X_angle -= delta_mouse_y_pos / 10
        pygame.mouse.set_pos(X_center, Y_center)

    sorted_polygons_data = sort_polygons_by_distance(polygons_data, player_pos)

    for polygon_data in sorted_polygons_data:
        polygon_coords = polygon_data[0]
        polygon_color = polygon_data[1]
        polygon_screen = []
        for point in polygon_coords:
            screen_coords = calculate_point_projection(view_angle, Y_angle, X_angle, player_pos, point)
            if not screen_coords:
                continue

            polygon_screen.append(screen_coords)

        if len(polygon_screen) == 3:
            pygame.draw.polygon(screen, polygon_color, [
                [polygon_screen[0][0], polygon_screen[0][1]],
                [polygon_screen[1][0], polygon_screen[1][1]],
                [polygon_screen[2][0], polygon_screen[2][1]]
            ])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()