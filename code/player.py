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
from actor import Actor
from bullet import Bullet

class Player(Actor):
    """
    Represents the player avatar.
    """
    def __init__(self, position, rotation=0, life=10, image=None):
        """
        Initialize object, setting position, life, xp.
        """
        Actor.__init__(self, position, rotation, life, [0, 0], 0, image)
        self.set_xp(0)

    def update(self, dt):
        """
        Override GameObjecte update()
        Keep the player inside the screen instead of killing it
        """
        self.set_rotation(self.get_rotation() + self.get_rotation_speed())
        if self.images:
            self.image = self.images[self.rotation * len(self.images) / 360]

        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_xp(self):
        """
        Return experience points
        """
        return self.xp

    def set_xp(self, xp):
        """
        Set experience points
        """
        self.xp = xp

    def fire(self, fire_list, image):
        """
        Fire a bullet with double speed
        """
        pos = self.get_pos()
        speed = 8
        x = speed * math.cos(math.radians(self.get_rotation()))
        y = speed * math.sin(math.radians(self.get_rotation()))
        Bullet(pos, [x, y], image=image, list=fire_list)

    def get_powerup(self, type, special):
        """
        Get a powerup
        """
        if type == "life":
            self.set_life(self.get_life() + special)
