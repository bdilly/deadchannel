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

from game_object import GameObject

class PowerUp(GameObject):
    """
    Base class for all power-ups
    """
    def __init__(self, position, life_time=3000, speed=[0,0], type=None,
                 special=0, image=None):
        """
        Set position, speed, life time and image
        """
        GameObject.__init__(self, image, position, 0, speed, 0)
        self.type = type
        self.special = special
        self.set_life_time(life_time)

    def update(self, dt, ms):
        """
        Overrides GameObject update
        """
        self.set_life_time(self.get_life_time() - ms)
        if self.get_life_time() < 0:
            self.kill()
        GameObject.update(self, dt, ms)

    def get_life_time(self):
        """
        Return how much time the object will remains alive
        """
        return self.life_time

    def set_life_time(self, life_time):
        """
        Set how much time the object will remains alive
        """
        self.life_time = life_time

    def get_type(self):
        """
        Returns the tipe of power up. It can be 'life', 'shield', 'weapon'...
        """
        return self.type

    def get_special(self):
        """
        FIXME: this method should be at each derivated class.
        For example, for life, it is just an integer with the amount of life
        the avatar will receive. For a weapon, it should be a list with
        the type of weapon, and ammunition.
        """
        return self.special
