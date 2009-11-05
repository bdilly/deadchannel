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

import os
import pygame
from pygame.locals import *

class Background:
    """
    It's the animated game background created with tiles.
    """
    image = None
    pos = None

    def __init__(self, image):
        """
        Creates a surface with tiles repeated until cover the entire screen.
        """
        # sets the absolute path
        image = os.path.join('graphic', image)
        # loads the image
        image = pygame.image.load(image)
        # disables alpha
        image.set_alpha(None, RLEACCEL)
        # converts the image so it won't be done every blit
        # it improves the performance
        image = image.convert()
        self.size = image.get_size()
        self.pos = [0, 0]
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        # ceil returns the ceiling of x as a float
        # we want the size of the screen plus a tile
        w = (ceil(float(screen_size[0]) / self.size[0]) + 1) * self.size[0]
        h = (ceil(float(screen_size[1]) / self.size[1]) + 1) * self.size[1]

        # creates a surface with width w and height h
        back = pygame.Surface((w, h))

        # covers the entire screen
        for i in range((back.get_size()[0]/self.size[0])):
            for j in range((back.get_size()[1]/self.size[1])):
                back.blit(image, (i * self.size[0], j * self.size[1]))

        self.image = back

    def update(self, dt):
        """
        Moves the background to the left
        """
        self.pos[0] -= 1
        # when it reaches the end, moves the background for the start point
        if (self.pos[0] < -self.size[0]):
            self.pos[0] += self.size[0]

    def draw(self,screen):
        """
        Draws the background
        """
        screen.blit(self.image, self.pos)

