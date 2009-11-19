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

import copy

import pygame
from pygame.locals import *

# Position of track box relative to BR corner of the box,
# proportional to screen width and height
TRACK_INFO_BOX_POS = (1.0, 0.95)     # (w, h)
# Text to box margin in pixels
TRACK_INFO_BOX_MARGIN = (15, 15)    # (TB, LR)
# Time to go in and out in ms
TRACK_INFO_BOX_ANIM_TIME = 200
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
        #font = None
        ptsize = 30
        font_color = "0x555555"
        self.player = player
        self.pos = pos or [0, 0]
        self.fcolor = pygame.color.Color(font_color)
        #self.font = pygame.font.Font(font, ptsize)
        self.font = pygame.font.SysFont('verdana', ptsize)
        self.image_life = image_life
        self.size_image_life= self.image_life.get_size()
        self.start_showing_track = False
        self.showing_track = False

    def set_track_info(self, info):
        """
        Sets track info
        """
        if info != self.track_info:
            self.track_info = info

    def show_track_info(self):
        """
        Shows the track info for an ammount of time, then fades out
        """
        if not self.track_info:
            return
        self.start_showing_track = True

    def __render_trackbox(self):
        info = self.track_info
        fcolor = (255, 255, 255)

        text0 = "%s by %s"  % (info['title'][0], info['artist'][0])
        text1 = "%s (%s)"   % (info['album'][0], info['date'][0])
        # print "Rendering track info: %s" % text
        self.font.set_bold(True)
        image_track_ln0 = self.font.render(text0, True, fcolor)
        self.font.set_bold(False)
        image_track_ln1 = self.font.render(text1, True, fcolor)
        # Gets rendered text size
        wf0, hf0 = image_track_ln0.get_size()
        wf1, hf1 = image_track_ln1.get_size()
        # Creates box background
        bg_size = [max(wf1, wf0) + (TRACK_INFO_BOX_MARGIN[0] * 2),
            hf1 + hf0 + (TRACK_INFO_BOX_MARGIN[1] * 2)]
        bg = pygame.Surface(bg_size, HWSURFACE | SRCALPHA)
        bg.fill((0, 0, 0, 200))
        # Calculates its position on HUD (lower right)
        #self.trackbox_pos = [(TRACK_INFO_BOX_POS[0] * w) - bg_size[0],
        #    (TRACK_INFO_BOX_POS[1] * h) - bg_size[1]]
        # Blits text to background
        bg.blit(image_track_ln0,
            [TRACK_INFO_BOX_MARGIN[0], TRACK_INFO_BOX_MARGIN[1]])
        bg.blit(image_track_ln1,
            [TRACK_INFO_BOX_MARGIN[0], hf0 + TRACK_INFO_BOX_MARGIN[1]])
        return bg

    def update(self, screen, ms):
        """
        Updates HUD animations
        """
        if not self.track_info:
            return
        info = self.track_info
        w, h = screen.get_size()
        if self.start_showing_track:
            self.showing_track = True
            self.elapsed_time_showing_track = 0
            self.start_showing_track = False
            self.image_trackbox = self.__render_trackbox()
            htb = self.image_trackbox.get_height()
            self.trackbox_pos = [w, (TRACK_INFO_BOX_POS[1] * h) - htb]
            #self.trackbox_dt = (1000 / 24)
            #(w - ((TRACK_INFO_BOX_POS[1] * w) - wtb)) /
        elif self.showing_track:
            elapsed = self.elapsed_time_showing_track
            if elapsed > TRACK_INFO_TIME + (2 * TRACK_INFO_BOX_ANIM_TIME):
                self.showing_track = False
            else:
                wtb = self.image_trackbox.get_width()
                trackbox_minw = (TRACK_INFO_BOX_POS[0] * w) - wtb
                ppms = float(wtb) / float(TRACK_INFO_BOX_ANIM_TIME)
                if elapsed + ms < TRACK_INFO_BOX_ANIM_TIME:
                    self.trackbox_pos[0] -= ppms * ms
                    #print "Box pos = %s ppms = %s" % (self.trackbox_pos, ppms)
                elif elapsed + ms > TRACK_INFO_BOX_ANIM_TIME + TRACK_INFO_TIME:
                    self.trackbox_pos[0] += ppms * ms
                else:
                    self.trackbox_pos[0] = trackbox_minw
                self.elapsed_time_showing_track += ms

    def draw_track_info(self, screen):
        """
        Draws currently playing track info
        """
        if self.showing_track:
            screen.blit(self.image_trackbox, self.trackbox_pos)

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
        self.draw_track_info(screen)
