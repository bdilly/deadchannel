#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Author:
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#
# Copyright (C) 2009 Bruno Dilly
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ----------------------------------------------------------------------

import math
from game_object import GameObject

class Bullet(GameObject):
    """
    Class for bullets.
    """
    def __init__(self, position, speed=None, rotation=0, rotation_speed=0,
                 image=None, list=None, distance = -1):
        GameObject.__init__(self, image, position, rotation, speed,
                            rotation_speed)
        self.distance = 0
        self.max_distance = distance
        if list != None:
            self.add(list)

    def update(self, dt, ms):
        GameObject.update(self, dt, ms)
        if self.max_distance == -1:
            return
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.distance = self.distance + math.sqrt(move_speed[0]**2 + \
                move_speed[1]**2)
        if self.distance >= self.max_distance:
            self.at_max_distance()

    def at_max_distance(self):
        self.kill()


class FragmentaryBullet(Bullet):
    def __init__(self, position, speed=None, rotation=0, rotation_speed=0,
                 image=None, list=None, distance = -1, fragments = 2):
        Bullet.__init__(self, position, speed=speed, rotation=rotation,
                        rotation_speed=rotation_speed, image=image,
                        list=list, distance=distance)
        self.fragments = fragments
        self.list = list

    def at_max_distance(self):
        for frag in range(self.fragments):
            speed = 8
            angle_dt = 360 / self.fragments
            frag_angle = frag * angle_dt
            x = speed * math.cos(math.radians(frag_angle))
            y = speed * math.sin(math.radians(frag_angle))
            Bullet(self.get_pos(), [x, y], image = self.image, list = self.list)
        self.kill()

