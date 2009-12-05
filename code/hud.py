#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Authors:
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#   Thiago Borges Abdnur <bolaum@gmail.com>
#
# Copyright (C) 2009 Bruno Dilly and Thiago Borges Abdnur
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
TRACK_INFO_BOX_ANIM_TIME = 500
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
        self.hide_track = False

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

    def hide_track_info(self):
        if self.showing_track:
           self.hide_track = True

    def __render_trackbox(self):
        info = self.track_info
        fcolor = (255, 255, 255)

        if info.has_key('title'):
            title = info['title'][0]
        else:
            title = "Unknown title"

        if info.has_key('artist'):
            artist = info['artist'][0]
        else:
            artist = "Unknown artist"

        if info.has_key('album'):
            album = info['album'][0]
        else:
            album = "Unknown album"

        if info.has_key('date'):
            date = "(%s)" % info['date'][0]
        else:
            date = ""

        text0 = "%s by %s"  % (title, artist)
        text1 = "%s %s"   % (album, date)
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

        #self.trackbox_pos = [(TRACK_INFO_BOX_POS[0] * w) - bg_size[0],
        #    (TRACK_INFO_BOX_POS[1] * h) - bg_size[1]]
        # Blits text to background
        bg.blit(image_track_ln0,
            [TRACK_INFO_BOX_MARGIN[0], TRACK_INFO_BOX_MARGIN[1]])
        bg.blit(image_track_ln1,
            [TRACK_INFO_BOX_MARGIN[0], hf0 + TRACK_INFO_BOX_MARGIN[1]])
        return bg

    def __update_trackbox(self, screen, ms):
        """
        Updates trackbox animation
        """
        if not self.track_info:
            return
        info = self.track_info
        w, h = screen.get_size()
        if self.start_showing_track and not self.hide_track:
            self.showing_track = True
            self.elapsed_time_showing_track = 0
            self.start_showing_track = False
            self.image_trackbox = self.__render_trackbox()
            htb = self.image_trackbox.get_height()
            self.trackbox_pos = [w, (TRACK_INFO_BOX_POS[1] * h) - htb]
            self.hide_track = False
        elif self.showing_track:
            elapsed = self.elapsed_time_showing_track
            if elapsed > TRACK_INFO_TIME + (2 * TRACK_INFO_BOX_ANIM_TIME):
                self.showing_track = False
                self.trackbox_pos[0] = w
                self.hide_track = False
                self.elapsed_time_showing_track = 0
            else:
                elapsed += ms
                wtb = self.image_trackbox.get_width()
                trackbox_minw = (TRACK_INFO_BOX_POS[0] * w) - wtb
                if elapsed < TRACK_INFO_BOX_ANIM_TIME:
                    if self.hide_track:
                        elapsed = 2 * TRACK_INFO_BOX_ANIM_TIME + \
                            TRACK_INFO_TIME - elapsed
                    else:
                        # "Go in" animation
                        # Calculates its position on HUD during animation
                        # Calculates v0 (pixels/ms) v0 = 2*dS/tf
                        v0 = (2 * (trackbox_minw - w)) / TRACK_INFO_BOX_ANIM_TIME
                        # Calculates acceleration (pixels/ms^2) a = -v0/tf
                        a = -v0 / TRACK_INFO_BOX_ANIM_TIME
                        # S = S0 + V0*t + (a*t^2)/2
                        self.trackbox_pos[0] = w + (v0 * float(elapsed)) + \
                            ((a * (float(elapsed)**2)) / 2.0)
                elif elapsed > TRACK_INFO_BOX_ANIM_TIME + TRACK_INFO_TIME:
                    t = float(elapsed - (TRACK_INFO_BOX_ANIM_TIME + TRACK_INFO_TIME))
                    # "Go out" animation
                    # Calculates its position on HUD during animation
                    # Calculates acceleration (pixels/ms^2) a = -v0/tf
                    a = 2 * (w - trackbox_minw) / (TRACK_INFO_BOX_ANIM_TIME**2)
                    # S = S0 + V0*t + (a*t^2)/2
                    self.trackbox_pos[0] = trackbox_minw + ((a * (t**2)) / 2.0)
                else:
                    if self.hide_track:
                        elapsed = TRACK_INFO_BOX_ANIM_TIME + TRACK_INFO_TIME
                        print "HIDING TRACK"
                    self.trackbox_pos[0] = trackbox_minw

                self.elapsed_time_showing_track = elapsed

    def update(self, screen, ms):
        """
        Updates HUD animations
        """
        self.__update_trackbox(screen, ms)

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
