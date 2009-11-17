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

import ConfigParser
import os
import shutil

class Preferences:
    def __init__(self, filename, default_filename):
        self.conf = ConfigParser.ConfigParser()
        self.default_conf = ConfigParser.ConfigParser()
        try:
            self.default_conf.read(default_filename)
        except ConfigParser.Error:
            # if default preferences can't be find it should exit
            print "Error: Couldn't find default preferences file"
            exit(2)
        if not os.path.isfile(filename):
            self.copy_default(default_filename, filename)
        try:
            self.conf.read(filename)
        except ConfigParser.Error:
            try:
                os.rename(filename, filename+'.backup')
            except OSError:
                print "Warning: Not creating preferences backup file"
            self.copy_default(default_filename, filename)

    def copy_default(self, default_filename, filename):
        try:
            shutil.copy(default_filename, filename)
            self.__init__(filename, default_filename)
        except IOError:
            print "Warning: preferences file couldn't be created"

    def get(self, section, option):
        if not self.conf.has_section(section) or \
           not self.conf.has_option(section, option):
            return self.default_conf.get(section, option)
        return self.conf.get(section, option)

    def get_resolution(self):
        res = self.get('screen', 'resolution')
        res  = res .lower()
        res = res.split("x")
        return [ int(res[0]), int(res[1])]

    def get_fullscreen(self):
        return self.get('screen', 'fullscreen')

    def get_key_up(self):
        return int(self.get('keyboard', 'up'))

    def get_key_down(self):
        return int(self.get('keyboard', 'down'))

    def get_key_right(self):
        return int(self.get('keyboard', 'right'))

    def get_key_left(self):
        return int(self.get('keyboard', 'left'))

    def get_key_fire(self):
        return int(self.get('keyboard', 'fire'))

    def get_key_rot_clock(self):
        return int(self.get('keyboard', 'rot_clock'))

    def get_key_rot_anti_clock(self):
        return int(self.get('keyboard', 'rot_anti_clock'))

    def get_key_player_play(self):
        return int(self.get('keyboard', 'player_play'))

    def get_key_player_stop(self):
        return int(self.get('keyboard', 'player_stop'))

    def get_key_player_next_track(self):
        return int(self.get('keyboard', 'player_next_track'))

    def get_mouse_sensitivity(self):
        return float(self.get('mouse', 'sensitivity'))

    def get_mouse_fire(self):
        return int(self.get('mouse', 'fire'))

    def get_joy_axis_x(self):
        return int(self.get('joystick', 'axis_x'))

    def get_joy_axis_y(self):
        return int(self.get('joystick', 'axis_y'))

    def get_joy_axis_z(self):
        return int(self.get('joystick', 'axis_z'))

    def get_joy_fire(self):
        return int(self.get('joystick', 'fire'))

    def get_joy_rot_clock(self):
        return int(self.get('joystick', 'rot_clock'))

    def get_joy_rot_anti_clock(self):
        return int(self.get('joystick', 'rot_anti_clock'))

    def get_joy_player_play(self):
        return int(self.get('joystick', 'player_play'))

    def get_joy_player_stop(self):
        return int(self.get('joystick', 'player_stop'))

    def get_joy_player_next_track(self):
        return int(self.get('joystick', 'player_next_track'))

    def get_joy_sensitivity(self):
        return float(self.get('joystick', 'sensitivity'))

    def get_joy_deadzone(self):
        return float(self.get('joystick', 'deadzone'))

    def get_joy_id(self):
        return int(self.get('joystick', 'id'))

    def get_input(self):
        return self.get('general', 'input')

    def get_music_volume(self):
        return float(self.get('general', 'music_volume'))

    fullscreen = property(get_fullscreen)
    resolution = property(get_resolution)
    key_up = property(get_key_up)
    key_down = property(get_key_down)
    key_right = property(get_key_right)
    key_left = property(get_key_left)
    key_fire = property(get_key_fire)
    key_rot_clock = property(get_key_rot_clock)
    key_rot_anti_clock = property(get_key_rot_anti_clock)
    key_player_play = property(get_key_player_play)
    key_player_stop = property(get_key_player_stop)
    key_player_next_track = property(get_key_player_next_track)
    mouse_sensitivity = property(get_mouse_sensitivity)
    mouse_fire = property(get_mouse_fire)
    j_axis_x = property(get_joy_axis_x)
    j_axis_y = property(get_joy_axis_y)
    j_axis_z = property(get_joy_axis_z)
    j_bt_fire = property(get_joy_fire)
    j_bt_rot_clock = property(get_joy_rot_clock)
    j_bt_rot_anti_clock = property(get_joy_rot_anti_clock)
    j_bt_player_play = property(get_joy_player_play)
    j_bt_player_stop = property(get_joy_player_stop)
    j_bt_player_next_track = property(get_joy_player_next_track)
    joy_sensitivity = property(get_joy_sensitivity)
    joy_deadzone = property(get_joy_deadzone)
    joy_id = property(get_joy_id)
    input = property(get_input)
    music_volume = property(get_music_volume)
