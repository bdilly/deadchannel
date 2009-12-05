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
                 pu_attr=0, image=None):
        """
        Set position, speed, life time and image
        """
        GameObject.__init__(self, image, position, 0, speed, 0)
        self.type = type
        self.pu_attr = pu_attr
        self.set_life_time(life_time)

    def update(self, dt, ms, *args):
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

    def get_pu_attr(self):
        """
        Returns a dict of power up attributes wich content depends on type.
        For 'first_aid_kit' it will returns a single element, the life bonus.
        For secondary weapons this list has a name, ammunition, distance,
        and other related to each kind of sw.
        """
        return self.pu_attr
