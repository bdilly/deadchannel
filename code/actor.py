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

from bullet import Bullet
from game_object import GameObject

class Actor(GameObject):
    """
    Base class for all characters
    """
    def __init__(self, position, rotation=270, life=1, speed=[0,0],
                 rotation_speed=0, image=None):
        """
        Set acceleration and image
        """
        GameObject.__init__(self, image, position, rotation, speed,
                            rotation_speed)
        self.set_life(life)
        self.set_accel([3, 3])

    def get_life(self):
        """
        Return the enemy's life
        """
        return self.life

    def set_life(self, life):
        """
        Set the character's life
        """
        self.life = life

    def do_collision(self):
        """
        Kill object if life reaches 0 when colliding
        """
        self.set_life(self.get_life() -1)
        if self.get_life() == 0:
            self.kill()

    def is_dead(self):
        """
        Return true if the object's life reached 0
        """
        return self.get_life() == 0

    def get_accel(self):
        """
        Returns acceleration
        """
        return self.acceleration

    def set_accel(self, accel):
        """
        Sets acceleration
        """
        self.acceleration = accel

    def accel_top(self):
        """
        Reduce vertical speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        """
        Increase vertical speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        """
        Reduce horizontal speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        """
        Increase horizontal speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))

    def rotate_clock(self, rot_accel):
        """
        Increase or reduce rotational speed
        """
        rot_speed = self.get_rotation_speed()
        self.set_rotation_speed(rot_speed + rot_accel)

    def fire(self, fire_list, image):
        """
        Fire a bullet in the same position with double speed.
        """
        # create a list with speed in axis x and y
        speed = list(self.get_speed())
        # double horizontal speed
        speed[0] *= 2
        Bullet(self.get_pos(), speed, image=image, list=fire_list)

