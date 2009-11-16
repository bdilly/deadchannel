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

from power_up import PowerUp

class FirstAidKit(PowerUp):
    """
    Power up object that healths the avatar
    """
    def __init__(self, position, life_time=3000, speed=[0,0], special=0,
                 image=None):
        """
        Set position, speed, life time and image
        """
        PowerUp.__init__(self, position, life_time, speed, 'life', special,
                         image)
        self.set_life_time(life_time)


