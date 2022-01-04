# -*- coding: utf-8 -*-
import pygame as pg
from math import sin, cos, pi, tan, atan, sqrt, degrees
import pyganim

WIN_HEIGHT = 800
HALF_WIN_HEIGHT = WIN_HEIGHT//2
WIN_WIDTH = 1200
FPS =60
SIZE = 32
MOUSE_SENSITIVITY = 0.004
DIST = 4000


TEXTURE_WIDTH = 256
TEXTURE_HEIGHT = 512
TEXTURE_SCALE = TEXTURE_WIDTH // (SIZE*SIZE)
TEXTURE_SCALE = 1


FPS_POS = (1100, 10)


DIST = 1100

N_LIGHTS = WIN_WIDTH//2
SEGMENT_WIDTH = int(WIN_WIDTH/N_LIGHTS)

HEIGHT_SCALE = 80*WIN_HEIGHT


PLAYER_SIZE = 20
STEP = 2
STEP_ANGEL = 0.02

DEVIL_STEP = 1
MONSTER_MIN_DIST = 130

ROCKET_STEP = 10

pg.init()
surface = pg.display.set_mode([WIN_WIDTH, WIN_HEIGHT])

SKY = pg.image.load("img/sky2.png").convert_alpha()
SUN = pg.image.load("img/sun.png").convert_alpha()
GORI = pg.image.load("img/gori.png").convert_alpha()
TEXTURES = {"B": pg.image.load("img/1s.png").convert_alpha(), "W": pg.image.load("img/2s.png").convert_alpha(),"F": pg.image.load("img/3s.png").convert_alpha(),"D": pg.image.load("img/4s.png").convert_alpha()}



FOV = 60*pi/180
TEXTURE_OFFSET_SCALE = (TEXTURE_WIDTH - TEXTURE_SCALE - 1)/SIZE
MAX_HEIGHT = SIZE/PLAYER_SIZE *6 * WIN_HEIGHT
MAX_HEIGHT1 = 2 * WIN_HEIGHT
d = WIN_WIDTH/2/tan(pi/6)
PHI2 = [atan(x/d) for x in range(-WIN_WIDTH // 2, WIN_WIDTH // 2, WIN_WIDTH//N_LIGHTS)]


scale = 0.8
image3D = pg.image.load("Sprites/barrel/anim/0.png").convert_alpha()
size = int(image3D.get_width() * scale), int(image3D.get_height() * scale)
BARREL_ANIM = [pg.transform.scale(pg.image.load(f'Sprites/barrel/anim/{i}.png').convert_alpha(), (size)) for i in range(13)]


scale = 2
image3D = pg.image.load("Sprites/flame/anim/0.png").convert_alpha()
size = int(image3D.get_width() * scale), int(image3D.get_height() * scale)
FLAME_ANIM = [pg.transform.scale(pg.image.load(f"Sprites/flame/anim/{i}.png").convert_alpha(), (size)) for i in range(16)]


scale = 0.6
image3D = pg.image.load("Sprites/pin/anim/0.png").convert_alpha()
size = int(image3D.get_width() * scale), int(image3D.get_height() * scale)
PIN_ANIM = [pg.transform.scale(pg.image.load(f"Sprites/pin/anim/{i}.png").convert_alpha(), (size)) for i in range(8)]

scale = 0.5
image3D = pg.image.load("Sprites/devil/base/0.png").convert_alpha()
size = int(image3D.get_width() * scale), int(image3D.get_height() * scale)
DEVIL_ANIM = [pg.transform.scale(pg.image.load(f"Sprites/devil/anim/{i}.png").convert_alpha(), (size)) for i in range(9)]






DEVIL_ANIM = { 'BASE': [pg.image.load(f"Sprites/devil/base/{i}.png").convert_alpha() for i in range(8)],
                'MOVE': [pg.image.load("Sprites/devil/base/0.png").convert_alpha()],
                'FIRE': [pg.image.load(f"Sprites/devil/anim/{i}.png").convert_alpha() for i in range(9)],
               'DYING': [pg.image.load(f"Sprites/devil/death/{i}.png").convert_alpha() for i in range(6)],
               'shift_height': 300,
               'scale': 0.5,
               'rect_size': SIZE,
               'fpf': 10,
               'fire_anim_frame': 4,
               'fireball_altitude': 100}

# DEVIL1_ANIM = { 'BASE': [pg.image.load(f"Sprites/devil1/base/{i}.png").convert_alpha() for i in range(8)],
#                 'MOVE': [pg.image.load(f"Sprites/devil1/action/{i}.png").convert_alpha() for i in range(3)],
#                 'FIRE': [pg.image.load(f"Sprites/devil1/action/{i}.png").convert_alpha() for i in range(3, 6)],
#                'DYING': [pg.image.load(f"Sprites/devil1/death/{i}.png").convert_alpha() for i in range(11)],
#                'shift_height': 0,
#                'scale': 0.6,
#                'rect_size': SIZE,
#                'fpf': 15,
#                'fire_anim_frame': 2,
#                'fireball_altitude': 100}

ROBO_ANIM = { 'BASE': [pg.image.load(f"Sprites/robo/base/{i}.png").convert_alpha() for i in range(8)],
                'MOVE': [pg.image.load(f"Sprites/robo/action/{i}.png").convert_alpha() for i in range(5)],
                'FIRE': [pg.image.load(f"Sprites/robo/action/{i}.png").convert_alpha() for i in range(5, 10)],
               'DYING': [pg.image.load(f"Sprites/robo/death/{i}.png").convert_alpha() for i in range(4)],
               'shift_height': 0,
               'scale': 4,
               'rect_size': SIZE,
               'fpf': 15,
               'fire_anim_frame': 2,
               'fireball_altitude': 120}

# scale = 3
# image3D = pg.image.load("Sprites/fire/base/0.png").convert_alpha()
# size = int(image3D.get_width() * scale), int(image3D.get_height() * scale)
# FIREBALL_ANIM = { 'BASE': [pg.transform.scale(pg.image.load(f"Sprites/fire/base/{i}.png").convert_alpha(), (size)) for i in range(8)],
#                   'DEAD': [pg.transform.scale(pg.image.load(f"Sprites/fire/dead/{i}.png").convert_alpha(), (size)) for i in range(3)]}


FIREBALL_ANIM = { 'BASE': [pg.image.load(f"Sprites/fire/base/{i}.png").convert_alpha() for i in range(8)],
                  'DEAD': [pg.image.load(f"Sprites/fire/dead/{i}.png").convert_alpha() for i in range(3)],
                  'shift_height': 3,
                'scale': 3,
               'rect_size': 10,
               'fpf': 10,
               }

scale = 3
image3D = pg.image.load("Sprites/rocket/0.png").convert_alpha()
size = int(image3D.get_width() * scale), int(image3D.get_height() * scale*1.0)
WEAPON = { 'BASE': [pg.transform.scale(pg.image.load(f"Sprites/rocket/0.png").convert_alpha(), (size))],
            'FIRE': [pg.transform.scale(pg.image.load(f"Sprites/rocket/{i}.png").convert_alpha(), (size)) for i in range(4)]}