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
import copy

# Time that track info will be shown
TRACK_INFO_TIME = 3000

class HUD:
    """
    HUD (Heads-Up Display) class. It displays info as life and experience
    points.
    """
    last_xp = -1
    image_font = None
    track_info = None

    def __init__(self, player, pos=None, image_life=None):
        """
        Initialize the class setting some attributes as font and images
        properties.
        """
        font = None
        ptsize = 30
        font_color = "0xff0000"
        self.player = player
        self.pos = pos or [0, 0]
        self.fcolor = pygame.color.Color(font_color)
        self.font = pygame.font.Font(font, ptsize)
        self.image_life = image_life
        self.size_image_life= self.image_life.get_size()

    def set_track_info(self, info):
        """
        Sets track info
        """
        self.track_info = info

    def show_track_info(self):
        """
        Shows the track info for an ammount of time, then fades out
        """
        if not self.track_info:
            return
        self.showing_track = True
        self.elapsed_time_showing_track = 0

    def update(self, dt, ms):
        """
        Updates HUD animations
        """
        if not self.track_info:
            return
        info = self.track_info
        if self.start_showing_track:
            if self.elapsed_time_showing_track > TRACK_INFO_TIME:
                self.showing_track = False

    def draw_track_info(self, screen):
        """
        Draws currently playing track info
        """
        w = screen.get_width()
        h = screen.get_height()
        if self.track_info:
            text = "%s by %s\n%s (%s)" % (info['title'], info['artist'],
                info['album'], info['date'])
            self.image_track = self.font.render(text, True, self.fcolor)
            #pos =

    def draw_life(self, screen):
        """
        Draw the life bar.
        """
        # makes a shallow copy
        pos = copy.copy(self.pos)
        for i in range(self.player.get_life()):
            pos[0] += self.size_image_life[0]
            screen.blit(self.image_life, pos)

    def draw_xp(self, screen):
        """
        Draw XP points.
        """
        pos = copy.copy(self.pos)
        pos[0] += 12 * self.size_image_life[0]
        xp = self.player.get_xp()
        # only render the text again if xp has changed
        if self.last_xp != xp:
            self.last_xp = xp
            text = "XP: % 4d" % xp
            self.image_font = self.font.render(text, True, self.fcolor)
        screen.blit(self.image_font, pos)

    def draw(self, screen):
        """
        Draw the HUD. Basically calls each pieces of information draw method.
        """
        self.draw_life(screen)
        self.draw_xp(screen)
