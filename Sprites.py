from Settings import *



def sprite_locate(surface, player, sprites_objects):
    ZBuffer = []
    for obj in sprites_objects:
        dx = obj.centerx - player.centerx
        dy = obj.centery - player.centery
        dy = dy if dy != 0 else 0.00000001
        if dy >= 0:
            alpha = atan(dx / dy) % (2*pi)
        else:
            alpha = pi + atan( dx / dy) % (2*pi)
        ksi = alpha - player.alfa if alpha - player.alfa > - pi else 2*pi + alpha - player.alfa
        ksi = ksi if ksi < pi else ksi - 2*pi
        #print(degrees(ksi), degrees(alpha), degrees(player.alfa))
        if -pi/3 < (ksi) < pi/3:


            l = obj.dist2hero
            if l < PLAYER_SIZE/2:
                l = PLAYER_SIZE/2
            pattern_height = int(HEIGHT_SCALE / l)
            sprite_height = pattern_height * obj.shift_scale*obj.image3D.get_height()
            sprite_height_shift = pattern_height * obj.shift_scale* obj.shift_height
            sprite_width = pattern_height * obj.shift_scale*obj.image3D.get_width()
            sprite_img = pg.transform.scale(obj.image3D, (int(sprite_width), int(sprite_height)))
            x_offset = int(-tan(ksi)/tan(pi/6)*WIN_WIDTH/2 + WIN_WIDTH/2 - sprite_width/2)
            y_offset = int( HALF_WIN_HEIGHT + pattern_height/2 - sprite_height - sprite_height_shift)
            sprite_spacing = (x_offset, y_offset)
            ZBuffer.append((l, sprite_img, sprite_spacing))

    return ZBuffer
    ZBuffer = sorted(ZBuffer, key=lambda n: n[0], reverse=True)
    for segment in ZBuffer:
        surface.blit(segment[1], segment[2])

