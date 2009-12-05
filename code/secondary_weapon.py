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

class SecondaryWeapon:

    def __init__(self, type, attributes):
        self.type = type
        self.name = attributes['name']
        self.ammo = int(attributes['ammo'])
        self.max_ammo = int(attributes['max_ammo'])
        self.distance = int(attributes['distance'])
        self.max_cooldown = int(attributes['cooldown'])
        self.cooldown = self.max_cooldown
        self.warm = int(attributes['heating'])
        self.max_charge = int(attributes['max_charge'])

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_ammo(self):
        return self.ammo

    def get_max_ammo(self):
        return self.ammo

    def get_distance(self):
        return self.distance

    def get_cooldown(self):
        return self.cooldown

    def set_cooldown(self, time):
        if time > self.max_cooldown:
            self.cooldown = self.max_cooldown
        elif time < 0:
            self.cooldown = 0
        else:
            self.cooldown = time

    def get_warm(self):
        return self.warm

    def get_max_charge(self):
        return self.max_charge

    def increase_ammo(self, ammo):
        """
        Increase ammunition or return False if no more ammo can be carried
        """
        if self.ammo == self.max_ammo:
            return False
        self.ammo = self.ammo + ammo
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
        return True

    def decrease_ammo(self, ammo):
        """
        Decrease ammunition or return False if the ammount required can't be
        decremented.
        """
        if self.ammo < ammo:
            return False
        self.ammo = self.ammo - ammo
        return True

class MultipleShotWeapon(SecondaryWeapon):
    def __init__(self, type, attributes):
        SecondaryWeapon.__init__(self, type, attributes)
        self.radius = int(attributes['radius'])
        self.simultaneous_shoots = int(attributes['simultaneous_shoots'])

    def get_radius(self):
        return self.radius

    def get_simultaneous_shoots(self):
        return self.simultaneous_shoots

class FragmentaryGrenade(SecondaryWeapon):
    def __init__(self, type, attributes):
        SecondaryWeapon.__init__(self, type, attributes)
        self.fragments = int(attributes['fragments'])

    def get_fragments(self):
        return self.fragments
