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

from actor import Actor
from bullet import Bullet

class Player(Actor):
    """
    Represents the player avatar.
    """
    def __init__(self, position, life=10, image=None):
        """
        Initialize object, setting position, life, xp, gold
        """
        Actor.__init__(self, position, life, [0, 0], image)
        self.set_xp(0)
        self.set_gold(0)

    def update(self, dt):
        """
        Override GameObjecte update()
        Keep the player inside the screen instead of killing it
        """
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

    def get_gold(self):
        """
        Return gold
        """
        return self.gold

    def set_gold(self, gold):
        """
        Set gold
        """
        self.gold = gold

    def fire(self, fire_list, image):
        """
        Fire a bullet with double speed
        """
        pos = self.get_pos()
        Bullet(pos, [8, 0], image, fire_list)

