# -*- coding: utf-8 -*-
from Settings import *
from Player import *
from Ray_casting import ray_casting2 as ray_casting
from level_builder import level_build
from Sprites import sprite_locate
from arms import Arms
SKY_SCALE = WIN_WIDTH/(pi/3)
GORI_SCALE = 2400
PI_3 = pi/3



pg.init()
surface = pg.display.set_mode([WIN_WIDTH, WIN_HEIGHT])

clock = pg.time.Clock()
pg.display.set_caption("DoomPy")
Background = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
Background.fill((80, 80, 80))
Sky = pg.Surface((WIN_WIDTH, WIN_HEIGHT/2))
Sky.fill((0, 180, 255))
Floor = pg.Surface((WIN_WIDTH, WIN_HEIGHT/2))
Floor.fill((50, 50, 50))



class GameObjectSession:
    def __init__(self, Level):
        self.hero = Player(55, 55, PI_3)
        self.entities = pg.sprite.Group()
        self.platforms = set()
        self.monsters = set()
        self.solid_objects = dict()
        self.door_x_objects = dict()
        self.door_y_objects = dict()
        self.action_objects = set()
        self.sprite_objects = set()
        self.fire_objects = set()
        self.moving_objects = []
        self.level = Level
        self.entities.add(self.hero)
        self.wh_map = level_build(self)
        self.arms = Arms(self)

def event_handler(keys):
    left, right, forward, back, turn_left, turn_right, action, __ = keys
    fire = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            if event.key == pg.K_LEFT:
                turn_left = True
            if event.key == pg.K_RIGHT:
                turn_right = True
            if event.key == pg.K_w:
                forward = True
            if event.key == pg.K_a:
                left = True
            if event.key == pg.K_d:
                right = True
            if event.key == pg.K_s:
                back = True
            if event.key == pg.K_f:
                action = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                fire = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                turn_left = False
            if event.key == pg.K_RIGHT:
                turn_right = False
            if event.key == pg.K_w:
                forward = False
            if event.key == pg.K_a:
                left = False
            if event.key == pg.K_d:
                right = False
            if event.key == pg.K_s:
                back = False
            if event.key == pg.K_f:
                action = False
    return left, right, forward, back, turn_left, turn_right, action, fire


def mini_karta_drow():
    pg.draw.line(surface, (255, 255, 255), (Game.hero.rect.center), (Game.hero.rect.centerx + DIST * sin(Game.hero.alfa), Game.hero.rect.centery + DIST * cos(Game.hero.alfa)))
    for e in Game.entities:
        surface.blit(e.image, (e.rect.left, e.rect.top))
    for e in Game.fire_objects:
        surface.blit(e.image, (e.rect.left, e.rect.top))
def fps_drow():
    display_fps = str(int(clock.get_fps()))
    render = font.render(display_fps, 0, (255,0,0))
    surface.blit(render, FPS_POS)

def arms_drow():
    x = int(WIN_WIDTH - WEAPON['BASE'][0].get_width())
    y = int(WIN_HEIGHT - WEAPON['BASE'][0].get_height())
    surface.blit(WEAPON['BASE'][0], ( x, y))

def health_indicator_update():
    health_indicator = pg.Surface((Game.hero.health, 20))
    if Game.hero.health> 75:
        health_indicator.fill((0,255,0))
    elif Game.hero.health> 50:
        health_indicator.fill((250, 250, 0))
    elif Game.hero.health> 25:
        health_indicator.fill((250, 130, 0))
    else:
        health_indicator.fill((255, 0, 0))
    surface.blit(health_indicator, (10, 10))

def sky_draw():
    surface.blit(Sky, (0, 0))
    v = (Game.hero.alfa) % PI_3 * SKY_SCALE
    #ksi = (Game.hero.alfa - PI_3 / 2)
    surface.blit(SKY, (v, 0))
    surface.blit(SKY, (-WIN_WIDTH + v, 0))

def game_over():
    message_dialog = pg.Surface((800, 200))
    message_dialog.fill((255, 0, 0))
    my_font1 = pg.font.SysFont('Arial', 36)
    text1 = my_font1.render('Вы проиграли!', 1, (255, 255, 255))

    message_dialog.blit(text1, (300, 50))

    surface.blit(message_dialog, (WIN_WIDTH // 7, WIN_HEIGHT // 3))
    pg.display.update()

    for i in range(2):
        clock.tick(1 / 2)
    exit()


left = right = forward = back = turn_left = turn_right = action = fire= False
keys = (left, right, forward, back, turn_left, turn_right, action, fire)
Game = GameObjectSession(0)
font = pg.font.SysFont('Arial', 36, bold = True)
k = 0
kk = 0
dk = pi*0.0001


while True:
    keys = event_handler(keys)
    surface.blit(Background, (0, 0))
    sky_draw()
    surface.blit(Floor, (0, WIN_HEIGHT/2))
    Game.hero.update(keys, Game.platforms, Game.action_objects)
    wall = ray_casting(surface, Game.hero, Game.solid_objects, Game.door_x_objects, Game.door_y_objects)
    sprites = sprite_locate(surface, Game.hero, Game.sprite_objects | Game.fire_objects)
    ZBuffer = sorted(wall+sprites, key=lambda n: n[0], reverse=True)

    for segment in ZBuffer:

        surface.blit(segment[1], segment[2])
    delete_objects = []
    # mini_karta_drow()
    for d in Game.action_objects:
        d.update()
    for sprite in Game.sprite_objects:
        sprite.update()

    delete_objects = []
    for sprite in Game.fire_objects:
        sprite.update()
        if sprite.ism_state == 'DEAD':
            delete_objects.append(sprite)

    for sprite in delete_objects:
        Game.fire_objects.remove(sprite)
    Game.arms.update(keys[7])
    health_indicator_update()
    surface.blit(Game.arms.image, Game.arms.coord)
    if not Game.hero.health:
        game_over()

    fps_drow()
    pg.display.update()
    clock.tick(60)