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

    def get_screen_resolution(self):
        res = self.get('screen', 'resolution')
        res  = res .lower()
        res = res.split("x")
        return [ int(res[0]), int(res[1])]

    def get_screen_fullscreen(self):
        return self.get('screen', 'fullscreen')

    def get_keyboard_up(self):
        return int(self.get('keyboard', 'up'))

    def get_keyboard_down(self):
        return int(self.get('keyboard', 'down'))

    def get_keyboard_right(self):
        return int(self.get('keyboard', 'right'))

    def get_keyboard_left(self):
        return int(self.get('keyboard', 'left'))

    def get_keyboard_fire(self):
        return int(self.get('keyboard', 'fire'))

    def get_keyboard_secondary_fire(self):
        return int(self.get('keyboard', 'secondary_fire'))

    def get_keyboard_rot_clock(self):
        return int(self.get('keyboard', 'rot_clock'))

    def get_keyboard_rot_anti_clock(self):
        return int(self.get('keyboard', 'rot_anti_clock'))

    def get_keyboard_player_play(self):
        return int(self.get('keyboard', 'player_play'))

    def get_keyboard_player_stop(self):
        return int(self.get('keyboard', 'player_stop'))

    def get_keyboard_player_next_track(self):
        return int(self.get('keyboard', 'player_next_track'))

    def get_keyboard_prev_secondary_weapon(self):
        return int(self.get('keyboard', 'prev_secondary_weapon'))

    def get_keyboard_next_secondary_weapon(self):
        return int(self.get('keyboard', 'next_secondary_weapon'))

    def get_keyboard_toogle_fullscreen(self):
        return int(self.get('keyboard', 'toogle_fullscreen'))

    def get_mouse_sensitivity(self):
        return float(self.get('mouse', 'sensitivity'))

    def get_mouse_fire(self):
        return int(self.get('mouse', 'fire'))

    def get_mouse_secondary_fire(self):
        return int(self.get('mouse', 'secondary_fire'))

    def get_mouse_prev_secondary_weapon(self):
        return int(self.get('mouse', 'prev_secondary_weapon'))

    def get_mouse_next_secondary_weapon(self):
        return int(self.get('mouse', 'next_secondary_weapon'))

    def get_joystick_axis_x(self):
        return int(self.get('joystick', 'axis_x'))

    def get_joystick_axis_y(self):
        return int(self.get('joystick', 'axis_y'))

    def get_joystick_axis_z(self):
        return int(self.get('joystick', 'axis_z'))

    def get_joystick_fire(self):
        return int(self.get('joystick', 'fire'))

    def get_joystick_secondary_fire(self):
        return int(self.get('joystick', 'secondary_fire'))

    def get_joystick_rot_clock(self):
        return int(self.get('joystick', 'rot_clock'))

    def get_joystick_rot_anti_clock(self):
        return int(self.get('joystick', 'rot_anti_clock'))

    def get_joystick_player_play(self):
        return int(self.get('joystick', 'player_play'))

    def get_joystick_player_stop(self):
        return int(self.get('joystick', 'player_stop'))

    def get_joystick_player_next_track(self):
        return int(self.get('joystick', 'player_next_track'))

    def get_joystick_prev_secondary_weapon(self):
        return int(self.get('joystick', 'prev_secondary_weapon'))

    def get_joystick_next_secondary_weapon(self):
        return int(self.get('joystick', 'next_secondary_weapon'))

    def get_joystick_sensitivity(self):
        return float(self.get('joystick', 'sensitivity'))

    def get_joystick_deadzone(self):
        return float(self.get('joystick', 'deadzone'))

    def get_joystick_id(self):
        return int(self.get('joystick', 'id'))

    def get_general_input(self):
        return self.get('general', 'input')

    def get_general_music_volume(self):
        return float(self.get('general', 'music_volume'))

    def get_general_default_setlist(self):
        return self.get('general', 'use_default_setlist')

    def get_general_music_dir(self):
        return self.get('general', 'music_dir')

    screen_fullscreen = property(get_screen_fullscreen)
    screen_resolution = property(get_screen_resolution)
    keyboard_up = property(get_keyboard_up)
    keyboard_down = property(get_keyboard_down)
    keyboard_right = property(get_keyboard_right)
    keyboard_left = property(get_keyboard_left)
    keyboard_fire = property(get_keyboard_fire)
    keyboard_secondary_fire = property(get_keyboard_secondary_fire)
    keyboard_rot_clock = property(get_keyboard_rot_clock)
    keyboard_rot_anti_clock = property(get_keyboard_rot_anti_clock)
    keyboard_player_play = property(get_keyboard_player_play)
    keyboard_player_stop = property(get_keyboard_player_stop)
    keyboard_player_next_track = property(get_keyboard_player_next_track)
    keyboard_prev_secondary_weapon = property(get_keyboard_prev_secondary_weapon)
    keyboard_next_secondary_weapon = property(get_keyboard_next_secondary_weapon)
    keyboard_toogle_fullscreen = property(get_keyboard_toogle_fullscreen)
    mouse_sensitivity = property(get_mouse_sensitivity)
    mouse_fire = property(get_mouse_fire)
    mouse_secondary_fire = property(get_mouse_secondary_fire)
    mouse_prev_secondary_weapon = property(get_mouse_prev_secondary_weapon)
    mouse_next_secondary_weapon = property(get_mouse_next_secondary_weapon)
    joystick_axis_x = property(get_joystick_axis_x)
    joystick_axis_y = property(get_joystick_axis_y)
    joystick_axis_z = property(get_joystick_axis_z)
    joystick_fire = property(get_joystick_fire)
    joystick_secondary_fire = property(get_joystick_secondary_fire)
    joystick_rot_clock = property(get_joystick_rot_clock)
    joystick_rot_anti_clock = property(get_joystick_rot_anti_clock)
    joystick_player_play = property(get_joystick_player_play)
    joystick_player_stop = property(get_joystick_player_stop)
    joystick_player_next_track = property(get_joystick_player_next_track)
    joystick_prev_secondary_weapon = property(get_joystick_prev_secondary_weapon)
    joystick_next_secondary_weapon = property(get_joystick_next_secondary_weapon)
    joystick_sensitivity = property(get_joystick_sensitivity)
    joystick_deadzone = property(get_joystick_deadzone)
    joystick_id = property(get_joystick_id)
    general_input = property(get_general_input)
    general_music_volume = property(get_general_music_volume)
    general_default_setlist = property(get_general_default_setlist)
    general_music_dir = property(get_general_music_dir)
