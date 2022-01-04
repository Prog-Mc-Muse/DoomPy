# -*- coding: utf-8 -*-
import pygame as pg
from map import map
from Settings import *
from Ray_casting import ray_collide

PI_8 = pi/8
PI_3_8 = 3 * pi/8
PI_5_8 = 5 * pi/8
PI_7_8 = 7 * pi/8



class Blocks(pg.sprite.Sprite):
    def __init__(self, x, y, texture_type):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((SIZE, SIZE))
        self.rect = pg.Rect(x, y, SIZE, SIZE)
        pg.draw.rect(self.image, (0, 255, 0), (1, 1, SIZE-2, SIZE-2))
        self.texture_type = texture_type
        self.ism_state = ''


class SimpleSprite(pg.sprite.Sprite):
    def __init__(self, x, y, animate, fpf):
        pg.sprite.Sprite.__init__(self)
        self.anim = animate
        self.width = self.anim[0].get_width()
        self.height = self.anim[0].get_height()
        self.shift_scale = self.height/(WIN_HEIGHT)
        self.x = x + SIZE / 4
        self.y = y + SIZE / 4
        self.image = pg.Surface((SIZE / 2, SIZE / 2))
        self.rect = pg.Rect(x + SIZE/4, y + SIZE/4, SIZE/2, SIZE/2)
        pg.draw.rect(self.image, (0, 255, 0), (1,1,SIZE-2,SIZE-2))
        self.frame_num_fpf = len(animate)*fpf
        self.fpf = fpf
        self.anim_step = 0
        self.anim_frame_num = 0
        self.ism_state = ''


    def update(self):
        self.anim_step = (self.anim_step + 1) % self.frame_num_fpf
        self.anim_frame_num = self.anim_step//self.fpf

class FireSprite(pg.sprite.Sprite):
    def __init__(self, x, y, alpha, monster_type, fpf, size, shift_height, game_object_list):
        pg.sprite.Sprite.__init__(self)
        self.anim_base = monster_type['BASE']
        self.anim_dead = monster_type['DEAD']
        self.width = self.anim_base[0].get_width()
        self.height = self.anim_base[0].get_height()
        self.shift_scale =  3/(WIN_HEIGHT)
        self.shift_height = shift_height


        self.shift_scale = monster_type['scale'] / (WIN_HEIGHT)



        self.x = x - size/2
        self.y = y - size/2
        self.alfa = alpha
        self.size = size
        self.side = 0
        self.player = game_object_list.hero
        self.platforms = game_object_list.platforms
        self.solid_objects = game_object_list.solid_objects
        self.door_x_objects = game_object_list.door_x_objects
        self.door_y_objects = game_object_list.door_y_objects
        self.centerx = x
        self.centery = y
        self.image = pg.Surface((size, size))
        self.rect = pg.Rect(self.x, self.y, size, size)
        self.fpf = fpf
        self.anim_step = 0
        self.anim_frame_num = 0
        self.image3D = pg.Surface((self.width, self.height))
        self.ism = {'GO': self.go,
                    'DYING': self.dying,
                    'DEAD': self.dead}
        self.ism_state = 'GO'
        self.ism_step = 0
        self.dist2hero = DIST

    def go(self):
        xvel = ROCKET_STEP * sin(self.alfa)
        yvel = ROCKET_STEP * cos(self.alfa)
        # провряем колизии
        self.x += xvel
        self.rect.x = round(self.x)
        if self.Collision(xvel, 0):
            self.ism_step = 0
            self.ism_state = 'DYING'
        self.y += yvel
        self.rect.y = round(self.y)
        if self.Collision(0, yvel):
            self.ism_step = 0
            self.ism_state = 'DYING'
        self.centerx = self.x + self.size / 2
        self.centery = self.y + self.size / 2
        self.image3D = self.anim_base[self.side]

    def dying(self):
        self.ism_step += 1
        self.anim_step = self.ism_step // self.fpf
        self.image3D = self.anim_dead[self.anim_step]
        if self.anim_step >= 2:
            self.ism_step = 0
            self.ism_state = 'DEAD'

    def dead(self):
        pass

    def update(self):
        # определяем дистанцию до игрока
        dx = self.player.centerx - self.centerx
        dy = self.player.centery - self.centery
        l = sqrt(dx*dx + dy*dy)
        self.dist2hero = l
        # если растояние не слишком велико, определяем находится или нет игрок в поле видимости монстра
        self.see = False
        dy = dy if dy != 0 else 0.00000001
        if dy >= 0:
            alpha = atan(dx / dy) % (2 * pi)
        else:
            alpha = (pi - atan(- dx / dy)) % (2 * pi)
        ksi = alpha - self.alfa
        ksi = ksi if ksi > - pi else 2 * pi + ksi
        ksi = ksi if ksi < pi else ksi - 2 * pi
        self.angle_find(ksi)
        self.ism.get(self.ism_state)()

    def angle_find(self,ksi):
        if -PI_8 <= ksi < PI_8:
            self.side = 0
        elif PI_8 <= ksi < PI_3_8:
            self.side = 1
        elif PI_3_8 <= ksi < PI_5_8:
            self.side = 2
        elif PI_5_8 <= ksi < PI_7_8:
            self.side = 3
        elif PI_7_8 <= ksi or ksi < - PI_7_8:
            self.side = 4
        elif - PI_7_8 <= ksi < -PI_5_8:
            self.side = 5
        elif -PI_5_8 <= ksi < -PI_3_8:
            self.side = 6
        elif -PI_3_8 <= ksi < -PI_8:
            self.side = 7

    def Collision(self, xvel, yvel):
        collision = False
        for e in self.platforms:
            if not (e is self):
                if not e.ism_state == 'DEAD' and self.rect.colliderect(e.rect):
                    if xvel > 0:
                        self.rect.right = e.rect.left
                    if xvel < 0:
                        self.rect.left = e.rect.right
                    if yvel > 0:
                        self.rect.bottom = e.rect.top
                    if yvel < 0:
                        self.rect.top = e.rect.bottom
                    self.x = float(self.rect.x)
                    self.y = float(self.rect.y)
                    collision = True
                    try:
                        e.damage(20)
                    except:
                        pass
        e = self.player
        if self.rect.colliderect(e):
            collision = True
            e.damage(20)
        return collision


class MovingSprite(pg.sprite.Sprite):
    def __init__(self, x, y, monster_type, game_object_list):
        pg.sprite.Sprite.__init__(self)
        self.game_object_list = game_object_list
        self.anim_base = monster_type['BASE']
        self.anim_move = monster_type['MOVE']
        self.anim_fire = monster_type['FIRE']
        self.anim_dying = monster_type['DYING']
        self.monster_type = monster_type
        self.shift_height = monster_type['shift_height']
        self.fpf = monster_type['fpf']
        self.fire_anim_frame = monster_type['fire_anim_frame']*self.fpf
        self.width = self.anim_base[0].get_width()
        self.height = self.anim_base[0].get_height()
        self.shift_scale = monster_type['scale']/(WIN_HEIGHT)
        self.fireball_altitude = monster_type['fireball_altitude']
        self.size = monster_type['rect_size']
        self.x = x + (SIZE - self.size) / 2
        self.y = y + (SIZE - self.size) / 2

        self.side = 0
        self.health = 100
        self.player = game_object_list.hero
        self.platforms = game_object_list.platforms
        self.solid_objects = game_object_list.solid_objects
        self.door_x_objects = game_object_list.door_x_objects
        self.door_y_objects = game_object_list.door_y_objects
        self.fire_objects = game_object_list.fire_objects
        self.centerx = x + self.size / 2
        self.centery = y + self.size / 2
        self.image = pg.Surface((self.size, self.size))
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)

        self.anim_step = 0
        self.ism_step = 0
        self.anim_frame_num = 0
        self.alfa = 3.9
        self.image3D = pg.Surface((self.width, self.height))
        self.ism = {'WAIT': self.wait,
                    'FIND': self.find,
                    'GO': self.go,
                    'FIRE': self.fire,
                    'DYING': self.dying,
                    'DEAD': self.dead}
        self.ism_state = 'WAIT'
        self.see = False
        self.dist2hero = DIST

    def wait(self):
        self.image3D = self.anim_base[self.side]
        if self.see:
            self.ism_step = 0
            self.ism_state ='FIND'
        if not self.health:
            self.ism_step = 0
            self.ism_state = 'DYING'

    def find(self):
        self.image3D = self.anim_base[self.side]
        if self.see:
            self.ism_step = 0
            self.ism_state ='GO'
        else:
            self.ism_step = 0
            self.ism_state = 'WAIT'
        if not self.health:
            self.ism_step = 0
            self.ism_state = 'DYING'

    def go(self):

        if self.dist2hero > MONSTER_MIN_DIST:
            xvel = DEVIL_STEP * sin(self.alfa)
            yvel = DEVIL_STEP * cos(self.alfa)
            # провряем колизии
            self.x += xvel
            self.rect.x = round(self.x)
            self.Collision(xvel, 0, self.platforms)

            self.y += yvel
            self.rect.y = round(self.y)
            self.Collision(0, yvel, self.platforms)

            self.centerx = self.x + self.size / 2
            self.centery = self.y + self.size / 2
        self.ism_step += 1
        self.anim_step = self.ism_step//self.fpf % len(self.anim_move)
        self.image3D = self.anim_move[self.anim_step-1]
        if self.ism_step >= 100:
            self.ism_state = 'FIRE'
            self.ism_step = 0
        if not self.see:
            self.ism_state = 'WAIT'
            self.ism_step = 0
        if not self.health:
            self.ism_step = 0
            self.ism_state = 'DYING'

    def fire(self):


        self.anim_step = self.ism_step//self.fpf
        self.image3D = self.anim_fire[self.anim_step]
        if self.ism_step == self.fire_anim_frame:
            xpoint = self.size * sin(self.alfa) + self.centerx
            ypoint = self.size * cos(self.alfa) + self.centery
            fire = FireSprite(xpoint, ypoint, self.alfa, FIREBALL_ANIM, 10, 10, self.fireball_altitude, self.game_object_list)
            self.fire_objects.add(fire)
        self.ism_step += 1
        if self.ism_step  >= len(self.anim_fire)*self.fpf:
            self.ism_step = 0
            self.ism_state = 'GO'
        if not self.health:
            self.ism_step = 0
            self.ism_state = 'DYING'




    def dying(self):
        if not self.ism_step:
            self.shift_height = 0

        self.ism_step += 1
        self.anim_step = self.ism_step // self.fpf
        self.image3D = self.anim_dying[self.anim_step]
        if self.anim_step >= len(self.anim_dying)-1:
            self.ism_step = 0
            self.ism_state = 'DEAD'


    def dead(self):
        self.image3D = self.anim_dying[len(self.anim_dying)-1]

    def damage(self, damage):
        self.health -= damage
        self.alfa = (self.player.alfa - pi)% (2*pi)

        if self.health <= 0:
            self.health = 0
            self.ism_step = 0


    def update(self):
        # определяем дистанцию до игрока
        dx = self.player.centerx - self.centerx
        dy = self.player.centery - self.centery
        l = sqrt(dx*dx + dy*dy)
        self.dist2hero = l
        # если растояние не слишком велико, определяем находится или нет игрок в поле видимости монстра
        self.see = False
        if l < DIST:
            dy = dy if dy != 0 else 0.00000001
            if dy >= 0:
                alpha = atan(dx / dy) % (2 * pi)
            else:
                alpha = (pi - atan(- dx / dy)) % (2 * pi)
            ksi = alpha - self.alfa
            ksi = ksi if ksi > - pi else 2 * pi + ksi
            ksi = ksi if ksi < pi else ksi - 2 * pi
            self.angle_find(ksi)
            if -PI_3_8 < (ksi) < PI_3_8:
                barrier_dist, _, _ = ray_collide(alpha, self.centerx, self.centery, self.solid_objects, self.door_x_objects, self.door_y_objects)
                if l < barrier_dist:
                    self.alfa = alpha
                    self.see = True
        self.ism.get(self.ism_state)()

    def angle_find(self,ksi):
        if -PI_8 <= ksi < PI_8:
            self.side = 0
        elif PI_8 <= ksi < PI_3_8:
            self.side = 1
        elif PI_3_8 <= ksi < PI_5_8:
            self.side = 2
        elif PI_5_8 <= ksi < PI_7_8:
            self.side = 3
        elif PI_7_8 <= ksi or ksi < - PI_7_8:
            self.side = 4
        elif - PI_7_8 <= ksi < -PI_5_8:
            self.side = 5
        elif -PI_5_8 <= ksi < -PI_3_8:
            self.side = 6
        elif -PI_3_8 <= ksi < -PI_8:
            self.side = 7
        self.anim_frame_num = self.side

    def Collision(self, xvel, yvel, platforms):
        for e in platforms:
            if not (e is self):
                if not e.ism_state == 'DEAD' and self.rect.colliderect(e.rect):
                    if xvel > 0:
                        self.rect.right = e.rect.left
                    if xvel < 0:
                        self.rect.left = e.rect.right
                    if yvel > 0:
                        self.rect.bottom = e.rect.top
                    if yvel < 0:
                        self.rect.top = e.rect.bottom
                    self.x = float(self.rect.x)
                    self.y = float(self.rect.y)


class DoorX(pg.sprite.Sprite):
    def __init__(self, x, y, texture_type):
        pg.sprite.Sprite.__init__(self)
        self.type = 'x'
        self.startx = x
        self.starty = y
        self.image = pg.Surface((SIZE, SIZE-10))
        self.rect = pg.Rect(x, y + 5, SIZE, SIZE-10)
        self.sence_rect = pg.Rect(x, y, SIZE, SIZE)
        pg.draw.rect(self.image,(0, 255, 0), (1,1,SIZE-2,SIZE-2-10))
        self.texture_type = texture_type
        self.door_offset = 0
        self.moove_step = 0.1
        self.open = False
        self.close = True
        self.turn_open = False
        self.turn_close = False
        self.ism_state = ''

    def update(self):
        if self.turn_close:
            self.open = False
            if self.door_offset >= 0:
                self.door_offset -= self.moove_step

            else:
                self.door_offset = 0
                self.turn_close = False
                self.close = True
        if self.turn_open:
            self.close = False
            if self.door_offset <= SIZE*0.9:
                self.door_offset += self.moove_step

            else:
                self.door_offset = SIZE*0.9
                self.turn_open = False
                self.open = True
        self.rect.x = self.startx + round(self.door_offset)


class DoorY(pg.sprite.Sprite):
    def __init__(self, x, y, texture_type):
        pg.sprite.Sprite.__init__(self)
        self.type = 'y'
        self.startx = x
        self.starty = y
        self.image = pg.Surface((SIZE-10, SIZE))
        self.rect = pg.Rect(x+5, y, SIZE-10, SIZE)
        self.sence_rect = pg.Rect(x, y, SIZE, SIZE)
        pg.draw.rect(self.image,(0, 255, 0), (1,1,SIZE-2-10,SIZE-2))
        self.texture_type = texture_type
        self.door_offset = 0
        self.moove_step = 0.1
        self.open = False
        self.close = True
        self.turn_open = False
        self.turn_close = False
        self.ism_state = ''

    def update(self):
        if self.turn_close:
            self.open = False
            if self.door_offset >= 0:
                self.door_offset -= self.moove_step

            else:
                self.door_offset = 0
                self.turn_close = False
                self.close = True
        if self.turn_open:
            self.close = False
            if self.door_offset <= SIZE*0.9:
                self.door_offset += self.moove_step

            else:
                self.door_offset = SIZE*0.9
                self.turn_open = False
                self.open = True
        self.rect.y = self.starty + round(self.door_offset)




def level_build(game_object_list):
    y = 0
    row_length = 0
    for row in map[game_object_list.level]:
        if len(row) > row_length:
            row_length = len(row)
        x = 0
        for el in row:
            if el == "B":
                platform = Blocks(x, y, 'B')
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.solid_objects[(x,y)] = platform
            if el == "W":
                platform = Blocks(x, y, 'W')
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.solid_objects[(x,y)] = platform
            if el == "F":
                platform = Blocks(x, y, 'F')
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.solid_objects[(x,y)] = platform
            if el == "-":
                platform = DoorX(x, y, '-')
                game_object_list.entities.add(platform)
                #game_object_list.platforms.append(platform)
                game_object_list.action_objects.add(platform)
                game_object_list.door_x_objects[(x,y)] = platform
            if el == "|":
                platform = DoorY(x, y, '|')
                game_object_list.entities.add(platform)
                #game_object_list.platforms.append(platform)
                game_object_list.action_objects.add(platform)
                game_object_list.door_y_objects[(x,y)] = platform
            if el == "o":
                platform = SimpleSprite(x, y, BARREL_ANIM, 10)
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.sprite_objects.add(platform)

            if el == "f":
                platform = SimpleSprite(x, y, FLAME_ANIM, 10)
                game_object_list.entities.add(platform)
                game_object_list.sprite_objects.add(platform)

            if el == "g":
                platform = SimpleSprite(x, y, PIN_ANIM, 10)
                game_object_list.entities.add(platform)
                game_object_list.sprite_objects.add(platform)

            if el == "d":
                platform = MovingSprite(x, y, DEVIL_ANIM, game_object_list)
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.monsters.add(platform)
                game_object_list.sprite_objects.add(platform)

            if el == "q":
                platform = MovingSprite(x, y, ROBO_ANIM, game_object_list)
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.monsters.add(platform)
                game_object_list.sprite_objects.add(platform)

            if el == "b":
                platform = SimpleSprite(x, y, BIG_ANIM, 20)
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.sprite_objects.add(platform)
            if el == "r":
                platform = SimpleSprite(x, y, ROBO_ANIM, 20)
                game_object_list.entities.add(platform)
                game_object_list.platforms.add(platform)
                game_object_list.sprite_objects.add(platform)
            if el in 'S':
                game_object_list.hero.startx = x
                game_object_list.hero.starty = y
                game_object_list.hero.Teleport(x, y)
            x += SIZE
        y+=SIZE
    return row_length * SIZE, len(map[game_object_list.level]) * SIZE