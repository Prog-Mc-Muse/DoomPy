from Settings import *
from level_builder import FireSprite


class Arms:
    def __init__(self, game_object_list):
        self.game_object_list = game_object_list
        self.player = game_object_list.hero
        self.fire_objects = game_object_list.fire_objects
        self.image = WEAPON['BASE'][0]
        self.coord = (int(WIN_WIDTH - WEAPON['BASE'][0].get_width()*0.7), int(WIN_HEIGHT - WEAPON['BASE'][0].get_height()*0.95))
        self.anim_step = 0
        self.fpf = 10
        self.ism_step = 0
        self.ism ={'WAIT': self.wait,
                   'FIRE': self.fire,
                   'RELOAD': self.reload}
        self.ism_state = 'WAIT'
    def update(self, fire_on):
        self.fire_on = fire_on
        self.ism.get(self.ism_state)()

    def wait(self):
        self.image = WEAPON['BASE'][0]
        if self.fire_on:
            self.ism_state ='FIRE'

    def fire(self):
        self.ism_step += 1
        self.anim_step = self.ism_step // self.fpf
        self.image = WEAPON['FIRE'][self.anim_step]
        if self.ism_step == 30:
            xpoint = PLAYER_SIZE*2 * sin(self.player.alfa - pi/10) + self.player.centerx
            ypoint = PLAYER_SIZE*2 * cos(self.player.alfa- pi/10) + self.player.centery
            fire = FireSprite(xpoint, ypoint, self.player.alfa, FIREBALL_ANIM, 10, 10, 80, self.game_object_list)
            self.fire_objects.add(fire)
        if self.anim_step >= 3:
            self.ism_step = 0
            self.ism_state = 'WAIT'

    def reload(self):
        pass