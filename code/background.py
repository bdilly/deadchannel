#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Authors:
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#   Joao Correa <joao@livewire.com.br>
#
# Copyright (C) 2009 Bruno Dilly
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ----------------------------------------------------------------------

import os
import pygame
from pygame.locals import *
from collections import deque

class Image:
    def __init__(self, image):
        self.image = image
        self.size = self.image.get_size()

class Layer:
    def __init__(self, image, width, layer):
        self.default_image = image
        self.pos = [0, 0]
        self.width = width
        self.layer = layer
        self.L = deque()
        self.w = width * image.size[0]
        self.h = image.size[1]

    def subLayer(self, screen):
        s = screen.get_size()
        self.pos = [0, s[1] - self.default_image.size[1]]

    def move(self):
        self.pos[0] -= 1

    def build(self):
        self.back = pygame.Surface((self.w, self.h), SRCALPHA)
        # checks if the number of images is OK
        while len(self.L) < self.width:
            self.L.append(self.default_image)

        lw = 0
        self.back.blit(self.L[0].image, (0, self.default_image.size[1] - self.L[0].size[1]))
        for i in range(1,self.width):
            lw += self.L[i-1].size[0]
            self.back.blit(self.L[i].image, (lw , self.h - self.L[i].size[1]))

        self.screen = self.back

        # remove the first image on the queue
        self.L.popleft()


class Background:
    """
    It's the animated game background created with tiles.
    """
    image = None
    pos = None
    L = deque()
    loaded_imgs = {}
    ms = 0
    size = [0, 0]

    def __init__(self, image0, image1):
        """
        Creates a surface with tiles repeated until cover the entire screen.
        """

        # to work "perfectly" all images in the tile must have the same size
        self.layer0 = Layer(Image(self.loadImage(image0)), 1, 0)
        self.size = self.layer0.default_image.size
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        image = self.loadImage(image1)
        size = image.get_size()         
        self.layer1 = Layer(Image(image), screen_size[0] / size[0] + 1, 1)
        self.layer1.subLayer(screen)

        self.layer0.build()
        self.layer1.build()

    def nextTile(self, next, layer):
        """
        Adds a tile to the queue and makes it default
        """
        self.layer1.default_image = Image(self.loadImage(next))
        self.layer1.L.append(self.layer1.default_image)
        #The tile added becomes the new default tile

    def update(self, ms):
        """
        Moves the background to the left
        """
        self.ms += ms
        if self.ms > 10:
            self.ms = 0
            self.layer1.move()
            # when it reaches the end, moves the background for the start point
            if (self.layer1.pos[0] <= -self.layer1.default_image.size[0]):
                self.layer1.pos[0] += self.layer1.default_image.size[0]
                self.layer1.build()

    def draw(self,screen):
        """
        Draws the background
        """
        screen.blit(self.layer0.screen, (0,0))
        screen.blit(self.layer1.screen, (self.layer1.pos))

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
            image = pygame.image.load(image).convert_alpha()
            # image is saved in memory, for no file reading
            self.loaded_imgs[image_path] = image
        return image

