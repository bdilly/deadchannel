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

import pygame
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):
    """
    Base class that represents all the objects in game.
    It inherits from Sprite and has a rect that makes easy to move the image
    """
    images = None
    def __init__(self, image, position, rotation=0, speed=None,
                 rotation_speed=0):
        """
        Load the object image, create a rect, set position and
        speed (static by default).
        """
        pygame.sprite.Sprite.__init__(self)
        if isinstance(image, list):
            self.image = image[0]
            self.images = image
        else:
            self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.set_pos(position)
        self.set_rotation(rotation)
        self.set_speed(speed or (0,0))
        self.set_rotation_speed(rotation_speed)

    def update(self, dt, ms):
        """
        Updates the position and rotation angle and destroy the object
        if it's out of the screen
        """
        self.set_rotation(self.rotation + self.rotation_speed)
        if self.images:
            self.image = self.images[self.rotation * len(self.images) / 360]
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
        if (self.rect.right < self.area.left) or \
            (self.rect.bottom < self.area.top) or \
            (self.rect.top > self.area.bottom):
            self.kill()

    def get_speed(self):
        """
        Return object speed
        """
        return self.speed

    def set_speed(self, speed):
        """
        Set object speed
        """
        self.speed = speed

    def get_pos(self):
        """
        Return object position
        """
        return (self.rect.center[0],
                self.rect.center[1])

    def set_pos(self,pos):
        """
        Set object position
        """
        self.rect.center = (pos[0], pos[1])

    def get_rotation(self):
        """
        Get object rotation angle
        """
        return self.rotation

    def set_rotation(self, rotation):
        """
        Set object rotation angle
        """
        self.rotation = rotation % 360

    def get_rotation_speed(self):
        """
        Get rotation speed
        """
        return self.rotation_speed

    def set_rotation_speed(self, rotation_speed):
        """
        Set rotation speed
        """
        self.rotation_speed = rotation_speed

    def get_size(self):
        """
        Get image size
        """
        return self.image.get_size()

