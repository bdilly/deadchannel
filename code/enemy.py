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
    def __init__(self, position, rotation=180, life=1, behaviour="normal", rotation_speed=0,
                 image=None):
        """
        Creates an enemy character that could has one of the following
        behaves: normal, fast, or diagonal.
        """

        self.counter = 1
        self.orientation = True
        self.behaviour = behaviour
        if behaviour == "normal":
            speed = [-4, 0]
        elif behaviour == "fast":
            speed = [-7, 0]
        elif behaviour == "diagonal":
            speed = [-3, 1]
        elif behaviour == "seeker":
            speed = [-3, 1]
        elif behaviour == "zigzag":
            speed = [-3, 1]

        Actor.__init__(self, position, rotation, life, speed,
                       rotation_speed, image)

    def update(self, dt, ms, counter, x, y):
        if self.behaviour == "zigzag":
            if self.counter % 15 == 0:
                if self.orientation == False:
                    self.speed = [-3, -8]
                    self.orientation = True
                else:
                    self.speed = [-3, 8]
                    self.orientation = False
        elif self.behaviour == "seeker":
            if self.counter %2 == 0:
                if self.orientation == True:
                    e_x, e_y = self.get_pos()
                    if e_y > y:
                        self.speed = [-3, -1]
                    elif e_y < y:
                        self.speed = [-3, 1]
                    else:
                        self.speed = [-3, 0]
            else:
                self.speed = [-3, 0]
        self.counter = self.counter + 1
        Actor.update(self, dt, ms)

    def get_behaviours():
        """
        Returns a list with all the possible behaviours
        """
        return ["normal", "fast", "diagonal"]
    get_behaviours = Callable(get_behaviours)

