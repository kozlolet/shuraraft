from math import floor
import pygame


def calculate_barycentric_coords(vertex1, vertex2, vertex3, point):
    x1, y1 = vertex1
    x2, y2 = vertex2
    x3, y3 = vertex3
    x, y = point

    den = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
    if den == 0:
        return

    w1 = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / den
    w2 = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / den
    w3 = 1 - w1 - w2

    return w1, w2, w3


def calculate_point_uv(w1, w2, w3, uv1, uv2, uv3):
    u1, u2, u3 = uv1[0], uv2[0], uv3[0]
    v1, v2, v3 = uv1[1], uv2[1], uv3[1]

    u = w1*u1 + w2*u2 + w3*u3
    v = w1*v1 + w2*v2 + w3*v3

    return u, v


def draw_texture_pixels(screen, arr, texture, quality, vertexes, uv):
    vertex1, vertex2, vertex3 = vertexes
    uv1, uv2, uv3 = uv

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # make bounding rectangle
    max_x = floor(max(vertex[0] for vertex in vertexes))+1
    min_x = floor(min(vertex[0] for vertex in vertexes))
    max_y = floor(max(vertex[1] for vertex in vertexes))+1
    min_y = floor(min(vertex[1] for vertex in vertexes))

    max_x = screen_width if max_x >= screen_width else max_x
    min_x = 0 if min_x <= 0 else min_x
    max_y = screen_height if max_y >= screen_height else max_y
    min_y = 0 if min_y <= 0 else min_y

    for x in range(floor(min_x/quality),
                   floor(max_x/quality)):
        for y in range(floor(min_y/quality),
                       floor(max_y/quality)):
            point_x = x*quality
            point_y = y*quality
            point = [point_x, point_y]
            weights = calculate_barycentric_coords(vertex1, vertex2, vertex3, point)
            if not weights:
                continue

            w1, w2, w3 = weights
            if not (w1 >= 0 and w2 >= 0 and w3 >= 0):
                continue

            u, v = calculate_point_uv(w1, w2, w3, uv1, uv2, uv3)

            texture_width = 16-1
            texture_height = 16-1
            pixel_texture_x = floor( texture_width * u )
            pixel_texture_y = floor( texture_height * v )

            pixel_color = texture[pixel_texture_y][pixel_texture_x][:3]

            # making square of pixels depending on quality
            for square_y in range(quality):
                for square_x in range(quality):
                    arr[point_x+square_x][point_y+square_y] = pixel_color



