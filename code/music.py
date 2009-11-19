#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Author:
#   Thiago Borges Abdnur <bolaum@gmail.com>
#
# Copyright (C) 2009 Thiago Borges Abdnur
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ----------------------------------------------------------------------

import os
import glob

import pygame
from pygame.locals import *

import mutagen

class Music_player:
    playlist = None
    loaded_index = -1
    loaded_track_info = None

    def __init__(self, hud, volume=1.0):
        """
        Initializes music playback
        """
        # Fills the playlist
        # TODO
        self.playlist = glob.glob(os.path.join('music', '*.ogg'))
        pygame.mixer.music.set_volume(volume)
        # The music player need a reference to the hud to show track info
        self.hud = hud

    def load_next(self):
        """
        Loads next music in the playlist. Wraps around if playlist ended.
        """
        # if playlist is empty, don't do anything
        if len(self.playlist) == 0:
            return
        loading = (self.loaded_index + 1) % len(self.playlist)
        try:
            pygame.mixer.music.load(self.playlist[loading])
            self.loaded_index = loading
            self.loaded_track_info = mutagen.File(self.playlist[loading])
            self.hud.set_track_info(self.loaded_track_info)
            print self.loaded_track_info
        except Exception as e:
            print "Error loading music %s: %s" % (self.playlist[loading], e)
            self.loaded_index = -1

    def play(self):
        """
        Plays currently loaded music
        """
        # if music not loaded, return
        if self.loaded_index == -1:
            return
        self.hud.show_track_info()
        pygame.mixer.music.play()

    def stop(self):
        """
        Stops currently playing track
        """
        pygame.mixer.music.stop()

    def next_track(self):
        """
        Loads and plays next track in playlist
        """
        self.stop()
        self.load_next()
        self.play()
