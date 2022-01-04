# -*- coding: utf-8 -*-
from math import sin, cos, pi, tan
import pygame as pg
from Settings import *


PHI = enumerate([f*FOV/N_LIGHTS for f in range(int(-N_LIGHTS/2), int(N_LIGHTS/2))])


def ray_collide(phi,  px, py, solid_objects, door_x_objects, door_y_objects):
    texture_type_x = texture_type_y = "B"
    tan_phi = tan(phi)
    tan_phi_pi = tan(pi / 2 - phi)
    sin_phi = sin(phi)
    sin_phi_0 = sin_phi if sin_phi != 0 else 0.00000000000001
    cos_phi = cos(phi)
    cos_phi_0 = cos_phi if cos_phi != 0 else 0.00000000000001
    # определяем направления движения по карте по  x и y
    sign_d_y = 1 if cos_phi > 0 else - 1
    sign_d_x = 1 if sin_phi > 0 else  -1
    # определчем не находимся ли мы внутри горизонтальной двери, если да, то проверяем не пересикается ли луч с дверью, если да, то отрисовываем её
    xy_mesh = (px // SIZE * SIZE, py // SIZE * SIZE)
    cross_not_find = True
    if xy_mesh in door_x_objects:
        y = py % SIZE
        if (sign_d_y > 0 and y < SIZE / 2) or (sign_d_y <= 0 and y > SIZE / 2):
            x = px % SIZE + sign_d_x * abs((y - SIZE / 2) * tan_phi)
            door_offset = door_x_objects[xy_mesh].door_offset
            if x > door_offset and 0 < x < SIZE:
                l = abs((y - SIZE / 2) / cos_phi_0)
                texture_type_y = "D"
                cross_not_find = False
                x = x - door_offset
    # если мы не в двери, то ищем пересечения с горизонтальными поверхностями объектов
    if cross_not_find:
        y = py // SIZE * SIZE + SIZE * (sign_d_y + 1) // 2
        x = px + sign_d_x * abs((y - py) * tan_phi)

        step_y = sign_d_y * SIZE
        step_x = sign_d_x * abs(SIZE * tan_phi)
        # определчем растояние до первого пересечения луча c ближайшей горизонтальной линией. определяем шаг по l
        l = abs((y - py) / cos_phi_0)
        step_l = abs((SIZE) / cos_phi_0)
        # идём по сетке по горизонтальным линиям, пока не найдём пересечение с объектом
        while l < DIST:
            xy_mesh = (x // SIZE * SIZE, (y - 1 + sign_d_y) // SIZE * SIZE)
            # ищем пересечения со стенами
            if xy_mesh in solid_objects:
                texture_type_y = solid_objects[xy_mesh].texture_type
                break
            # ищем пересечения с дверьми
            if xy_mesh in door_x_objects:
                door_offset = door_x_objects[xy_mesh].door_offset
                if (x + step_x / 2) % SIZE > door_offset and (x % SIZE + step_x / 2) < SIZE:
                    l += step_l / 2
                    texture_type_y = "D"
                    x += step_x / 2 - door_offset
                    break
            y += step_y
            x += step_x
            l += step_l
    x_offset = x % SIZE
    y_dist = l
    # определчем координаты Bx,By первого пересечения луча c ближайшей вертикальной линией. определяем шаги по x и по y
    sign_d_x = 1 if phi < pi else - 1
    sign_d_y = 1 if cos_phi > 0 else - 1
    # определчем не находимся ли мы внутри вертикальной двери, если да, то проверяем не пересикается ли луч с дверью, если да, то отрисовываем её
    xy_mesh = (px // SIZE * SIZE, py // SIZE * SIZE)
    cross_not_find = True
    if xy_mesh in door_y_objects:
        x = px % SIZE
        if (sign_d_x > 0 and x < SIZE / 2) or (sign_d_x <= 0 and x > SIZE / 2):
            y = py % SIZE + sign_d_y * abs((x - SIZE / 2) * tan_phi_pi)
            door_offset = door_y_objects[xy_mesh].door_offset
            if y > door_offset and 0 < y < SIZE:
                l = abs((x - SIZE / 2) / sin_phi_0)
                texture_type_x = "D"
                cross_not_find = False
                y = y - door_offset
    # если мы не в двери, то ищем пересечения с вертикальными поверхностями объектов
    if cross_not_find:
        x = px // SIZE * SIZE + SIZE * (sign_d_x + 1) // 2
        y = py + sign_d_y * abs((x - px) * tan_phi_pi)
        step_x = sign_d_x * SIZE
        step_y = sign_d_y * abs(SIZE * tan_phi_pi)
        # определчем растояние до первого пересечения луча c ближайшей вертикальной линией. определяем шаг по l
        l = abs((x - px) / sin_phi_0)
        step_l = abs((SIZE) / sin_phi_0)
        # идём по сетке по вертикальным линиям, пока не найдём пересечение с объектом
        while l < DIST:
            xy_mesh = ((x - 1 + sign_d_x) // SIZE * SIZE, y // SIZE * SIZE)
            if xy_mesh in solid_objects:
                texture_type_x = solid_objects[xy_mesh].texture_type
                break
            if (xy_mesh) in door_y_objects:
                door_offset = door_y_objects[xy_mesh].door_offset
                if (y + step_y / 2) % SIZE > door_offset and (y % SIZE + step_y / 2) < SIZE:
                    l += step_l / 2
                    texture_type_x = "D"
                    y += step_y / 2 - door_offset
                    break
            y += step_y
            x += step_x
            l += step_l
    y_offset = y % SIZE
    x_dist = l
    l, texture_type, texture_offset = (x_dist, texture_type_x, y_offset) if x_dist < y_dist else (
    y_dist, texture_type_y, x_offset)
    return l, texture_type, texture_offset


def ray_casting2(surface, player, solid_objects, door_x_objects, door_y_objects):
    ZBuffer =[]
    for i, phi in enumerate(PHI2):
        phi = (phi + player.alfa) % (2*pi)
        l, texture_type, texture_offset = ray_collide(phi, player.centerx, player.centery, solid_objects, door_x_objects, door_y_objects)
        if l < PLAYER_SIZE/2: l = PLAYER_SIZE/2
        if l > DIST:l = DIST
        l = l * cos(phi - player.alfa)
        segment_height = int(HEIGHT_SCALE / l )
        texture_segment = TEXTURES[texture_type].subsurface(texture_offset*TEXTURE_OFFSET_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        texture_segment = pg.transform.scale(texture_segment, (SEGMENT_WIDTH, segment_height))
        texture_spacing = (((N_LIGHTS-i-1)*SEGMENT_WIDTH), HALF_WIN_HEIGHT - segment_height//2)
        ZBuffer.append((l, texture_segment, texture_spacing))

    return ZBuffer

