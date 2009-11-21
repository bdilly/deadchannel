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
from collections import deque

class Background:
    """
    It's the animated game background created with tiles.
    """
    image = None
    loaded_imgs = {}
    pos = None
    L = deque()

    def __init__(self, image):
        """
        Creates a surface with tiles repeated until cover the entire screen.
        """

        # to work "perfectly" all images in the tile must have the same size
        image = self.loadImage(image)
        self.default_image = image
        self.size = image.get_size()
        self.pos = [0, 0]
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil

        # ceil returns the ceiling of x as a float
        # we want the size of the screen plus a tile
        self.w = (ceil(float(screen_size[0]) / self.size[0]) + 1) * self.size[0]
        self.h = (ceil(float(screen_size[1]) / self.size[1]) + 1) * self.size[1]

        # creates a surface with width w and height h
        self.back = pygame.Surface((self.w, self.h))

        for i in range((self.back.get_size()[0]/self.size[0])):
            self.L.append(image)

        self.build()

    def loadImage(self, image_path):
        """
        Loads the image that is going to be used on the tile
        """
        
        # tries to load from memory for better performance
        # need to check if it is really better!
        if image_path in self.loaded_imgs:
            image = self.loaded_imgs[image_path]
        else:
            image = os.path.join('graphic', image_path)
            # loads the image
            image = pygame.image.load(image)
            # disables alpha
            image.set_alpha(None, RLEACCEL)
            # converts the image so it won't be done every blit
            # it improves the performance
            image = image.convert()
            self.loaded_imgs[image_path] = image
        return image

    def build(self):
        """
        Build the whole image in the background
        """

        # checks if the number of images is OK
        if len(self.L) < self.w:
            self.L.append(self.default_image)

        for i in range((self.back.get_size()[0]/self.size[0])):
            for j in range((self.back.get_size()[1]/self.size[1])):
                self.back.blit(self.L[i], (i * self.size[0], j * self.size[1]))

        self.image = self.back

        # remove the first image on the queue
        self.L.popleft()


    def nextTile(self, next):
        """
        Adds a tile to the queue
        """
        self.default_image = self.loadImage(next)
        #The tile added becomes the new default tile
        self.L.append(self.default_image)

    def update(self, dt):
        """
        Moves the background to the left
        """
        self.pos[0] -= 1
        # when it reaches the end, moves the background for the start point
        if (self.pos[0] < -self.size[0]):
            self.pos[0] += self.size[0]
            self.build()

    def draw(self,screen):
        """
        Draws the background
        """
        screen.blit(self.image, self.pos)

