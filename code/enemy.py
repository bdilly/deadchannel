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

class Callable:
    """
    Wrapper to class-method
    """
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Enemy(Actor):
    """
    Class for enemy characters
    """
    def __init__(self, position, life=1, behaviour="normal", image=None):
        """
        Creates an enemy character that could has one of the following
        behaves: normal, fast, or diagonal.
        """
        if behaviour == "normal":
            speed = [-4, 0]
        elif behaviour == "fast":
            speed = [-7, 0]
        elif behaviour == "diagonal":
            speed = [-3, 1]

        Actor.__init__(self, position, life, speed, image)

    def get_behaviours():
        """
        Returns a list with all the possible behaviours
        """
        return ["normal", "fast", "diagonal"]
    get_behaviours = Callable(get_behaviours)

