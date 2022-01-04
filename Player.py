# -*- coding: utf-8 -*-
import pygame as pg
from math import sin, cos, tan, pi
from Settings import *




class Player(pg.sprite.Sprite):
    def __init__(self, x0, y0, alfa0):
        pg.sprite.Sprite.__init__(self)
        pg.mouse.set_visible(False)
        self.alfa = alfa0
        self.startx = x0
        self.starty = y0
        self.x = float(x0)
        self.y = float(y0)
        self.health = 100
        self.centerx = self.x + PLAYER_SIZE / 2
        self.centery = self.y + PLAYER_SIZE / 2
        self.image = pg.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.image.set_colorkey((0, 0, 0, 255))
        self.rect = pg.Rect(x0, y0, PLAYER_SIZE, PLAYER_SIZE)
        pg.draw.circle(self.image, (0, 255, 0), (int(PLAYER_SIZE / 2), int(PLAYER_SIZE / 2)), 10)

    def update(self, keys, platforms, action_objects):
        left, right, forward, back, turn_left, turn_right, action, __ = keys
        xvel = yvel = 0
        if forward:
            xvel += STEP * sin(self.alfa)
            yvel += STEP * cos(self.alfa)
        if back:
            xvel -= STEP * sin(self.alfa)
            yvel -= STEP * cos(self.alfa)
        if left:
            xvel += STEP * cos(self.alfa)
            yvel -= STEP * sin(self.alfa)
        if right:
            xvel -= STEP * cos(self.alfa)
            yvel += STEP * sin(self.alfa)
        if turn_left:
            self.alfa += STEP_ANGEL
        if turn_right:
            self.alfa -= STEP_ANGEL
        if action:
            self.action_collision(action_objects)
        self.mouse_control()
        self.alfa %= (2 * pi)
        self.x += xvel
        self.rect.x = self.x
        self.Collision(xvel, 0, platforms, action_objects)
        self.y += yvel
        self.rect.y = self.y
        self.Collision(0, yvel, platforms, action_objects)
        self.centerx = self.x + PLAYER_SIZE / 2
        self.centery = self.y + PLAYER_SIZE / 2

    def Collision(self, xvel, yvel, platforms, action_objects):
        collision = False
        for e in action_objects:
            if  self.rect.colliderect(e.rect):
                if e.type == 'y':
                    if self.rect.centerx > e.rect.centerx:
                        self.rect.left = e.rect.right
                    else:
                        self.rect.right = e.rect.left
                else:
                    if self.rect.centery > e.rect.centery:
                        self.rect.top = e.rect.bottom
                    else:
                        self.rect.bottom = e.rect.top
                self.x = float(self.rect.x)
                self.y = float(self.rect.y)
        for e in platforms:
            if not e.ism_state == 'DEAD' and self.rect.colliderect(e.rect):
                if xvel > 0:
                    self.rect.right = e.rect.left
                if xvel < 0:
                    self.rect.left = e.rect.right
                if yvel > 0:
                    self.rect.bottom = e.rect.top
                if yvel < 0:
                    self.rect.top = e.rect.bottom
                collision = True
                self.x = float(self.rect.x)
                self.y = float(self.rect.y)
        return collision

    def action_collision(self, action_objects):
        for e in action_objects:
            if self.rect.colliderect(e.sence_rect):
                if e.open:
                    e.turn_close = True
                elif e.close:
                    e.turn_open = True

    def Teleport(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.centerx = self.x + PLAYER_SIZE / 2
        self.centery = self.y + PLAYER_SIZE / 2

    def mouse_control(self):
        if pg.mouse.get_focused():
            difference = pg.mouse.get_pos()[0] - WIN_WIDTH/2
            pg.mouse.set_pos((WIN_WIDTH/2,WIN_HEIGHT/2))
            self.alfa -= difference * MOUSE_SENSITIVITY

    def damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.health = 0

