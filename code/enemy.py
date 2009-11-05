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

class Enemy(Actor):
    """
    Class for enemy characters
    """
    def __init__(self, position, life=1, speed=None, image=None):
        """
        Creates an enemy character
        """
        Actor.__init__(self, position, life, speed, image)

