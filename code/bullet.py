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

class Bullet(GameObject):
    """
    Class for bullets.
    """
    def __init__(self, position, speed=None, rotation=0, rotation_speed=0,
                 image=None, list=None):
        GameObject.__init__(self, image, position, rotation, speed,
                            rotation_speed)
        if list != None:
            self.add(list)

