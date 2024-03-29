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
import random

import pygame
from pygame.locals import *

import mutagen

class Music_player:
    playlist = None
    loaded_index = -1
    loaded_track_info = None

    def __init__(self, hud, volume=1.0, default_setlist=None, music_dir=None):
        """
        Initializes music playback
        """
        # Fills the playlist
        self.playlist = []
        if default_setlist:
            self.playlist += glob.glob(os.path.join('music', '*.ogg'))
        if music_dir:
            MUSIC_DIR = os.path.abspath(music_dir)
            self.playlist += glob.glob(os.path.join(MUSIC_DIR, '*.ogg'))
        # Shuffles playlist
        random.shuffle(self.playlist)
        pygame.mixer.music.set_volume(volume)
        # The music player need a reference to the hud to show track info
        self.hud = hud
        self.playing = False

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
        if self.loaded_index == -1 or self.playing:
            return

        self.hud.show_track_info()
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        """
        Stops currently playing track
        """
        self.hud.hide_track_info()
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        """
        Loads and plays next track in playlist
        """
        self.stop()
        self.load_next()
        self.play()
