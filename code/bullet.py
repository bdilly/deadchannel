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
    def __init__(self, position, speed=None, image=None, list=None):
        GameObject.__init__( self, image, position, speed )
        if list != None:
            self.add( list )

