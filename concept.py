import pygame
from math import sqrt, sin, cos, tan

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True

X_center = screen.get_width() / 2
Y_center = screen.get_height() / 2

def calculate_point_projection(view_angle, player_pos, target):
    if target[2] < player_pos[2]:
        return

    # screen x calculate
    distance_toLeft = tan(view_angle/2) * (target[2] - player_pos[2]) - (player_pos[0] - target[0])
    full_flat = tan(view_angle/2) * (target[2] - player_pos[2]) * 2
    E_toLeft = distance_toLeft / full_flat if full_flat else 1
    target_screen_x = screen.get_width() * E_toLeft

    # screen y calculate
    distance_toUp = tan(view_angle/2) * (target[2] - player_pos[2]) - (target[1] - player_pos[1])
    full_flat = tan(view_angle/2) * (target[2] - player_pos[2]) * 2
    E_toUp = distance_toUp / full_flat if full_flat else 1
    target_screen_y = screen.get_height() * E_toUp

    return target_screen_x, target_screen_y


lines = [
    [[-5, 2, 4], [-2, 2, 4]],   [[2, 2, 4], [5, 2, 4]],
    [[-5, -2, 4], [-2, -2, 4]],   [[2, -2, 4], [5, -2, 4]],

    [[-5, 2, 6], [-2, 2, 6]],   [[2, 2, 6], [5, 2, 6]],
    [[-5, -2, 6], [-2, -2, 6]],   [[2, -2, 6], [5, -2, 6]],
]
player_pos = [0, 0, 0]
view_angle = 90

while running:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= 1
    if keys[pygame.K_d]:
        player_pos[0] += 1
    if keys[pygame.K_s]:
        player_pos[2] -= 1
    if keys[pygame.K_w]:
        player_pos[2] += 1
    if keys[pygame.K_SPACE]:
        player_pos[1] += 1
    if keys[pygame.K_LSHIFT]:
        player_pos[1] -= 1

    for line in lines:
        line_screen = []
        for point in line:
            point_screen_x, point_screen_y = calculate_point_projection(view_angle, player_pos, point)
            if point_screen_x and point_screen_y:
                line_screen.append([point_screen_x, point_screen_y])

        if len(line_screen) == 2:
            pygame.draw.line(screen, (255, 255, 255), [line_screen[0][0], line_screen[0][1]], [line_screen[1][0], line_screen[1][1]], 5)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()