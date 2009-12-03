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

import math
from actor import Actor
from bullet import Bullet, FragmentaryBullet, GuidedBullet
from secondary_weapon import SecondaryWeapon, MultipleShotWeapon, \
                             FragmentaryGrenade

class Player(Actor):
    sw_list = []
    sw_selected = -1
    max_life = 10
    cooldown = 30
    warm = 30
    """
    Represents the player avatar.
    """
    def __init__(self, position, rotation=0, life=10, image=None):
        """
        Initialize object, setting position, life, xp.
        """
        Actor.__init__(self, position, rotation, life, [0, 0], 0, image)
        self.set_xp(0)

    def update(self, dt, ms):
        """
        Override GameObjecte update()
        Keep the player inside the screen instead of killing it
        """
        self.set_rotation(self.get_rotation() + self.get_rotation_speed())
        if self.images:
            self.image = self.images[self.rotation * len(self.images) / 360]

        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

        self.cooldown += ms
        for w in self.sw_list:
            w.set_cooldown(w.get_cooldown() + ms)

    def get_xp(self):
        """
        Return experience points
        """
        return self.xp

    def set_xp(self, xp):
        """
        Set experience points
        """
        self.xp = xp

    def set_life(self, life):
        """
        Set player's life if it's not more than max life or return False.
        Overrides Actor's set_life method.
        """
        if life > self.max_life:
            return False
        self.life = life
        return True

    def fire(self, fire_list, image, primary=True, enemy_list=None):
        """
        Fire a bullet if primary is True, or use secondary weapon
        """
        pos = self.get_pos()
        rot = self.get_rotation()
        speed = 8
        x = speed * math.cos(math.radians(rot))
        y = speed * math.sin(math.radians(rot))
        if primary:
            if self.cooldown >= self.warm:
                self.cooldown -= self.warm
                Bullet(pos, [x, y], image = image, list = fire_list)
        else:
            weapon = self.get_selected_secondary_weapon()
            # verifies if the weapon can be used. if not, cooldown
            # goes to 0 and the player will need to wait more  =)
            if weapon.get_cooldown() >= weapon.get_warm():
                weapon.set_cooldown(weapon.get_cooldown() - weapon.get_warm())
            else:
                weapon.set_cooldown(0)
                return
            if isinstance(weapon, FragmentaryGrenade):
                if not weapon.decrease_ammo(1):
                    self.drop_secondary_weapon(weapon)
                    return
                FragmentaryBullet(pos, [x, y], image = image, list = fire_list,
                       distance = weapon.get_distance(),
                       fragments = weapon.get_fragments())
            elif isinstance(weapon, MultipleShotWeapon):
                angle = weapon.get_radius()
                bullets = weapon.get_simultaneous_shoots()
                angle_dt = angle / bullets
                if not weapon.decrease_ammo(bullets):
                    self.drop_secondary_weapon(weapon)
                    return
                for b in range(bullets):
                    b_angle = rot - angle / 2 + b * angle_dt
                    x = speed * math.cos(math.radians(b_angle))
                    y = speed * math.sin(math.radians(b_angle))
                    Bullet(pos, [x, y], image = image, list = fire_list,
                           distance = weapon.get_distance())
            elif weapon.type == "sw_guided":
                if not weapon.decrease_ammo(1):
                    self.drop_secondary_weapon(weapon)
                    return
                GuidedBullet(pos, [x, y], image = image, list = fire_list,
                             enemy_list = enemy_list)

    def get_powerup(self, type, special):
        """
        Get a powerup. Return true if the player could get it, or
        false if he can't.
        """
        if type == "first_aid_kit":
            return self.get_first_aid_kit(int(special[0]))
        # secondary weapon
        elif "sw" in type:
            if type == "sw_mult":
                sw = MultipleShotWeapon(type, special)
            elif type == "sw_frag":
                sw = FragmentaryGrenade(type, special)
            else:
                sw = SecondaryWeapon(type, special)
            return self.get_secondary_weapon(sw)

    def get_first_aid_kit(self, bonus_life):
        """
        Increment player's life by bonus_life
        """
        if not self.set_life(self.get_life() + bonus_life):
            return False
        print "Hmm, nice!  +" + str(bonus_life) + " life"
        return True

    def get_secondary_weapon(self, weapon):
        """
        Add a secondary weapon to the inventory
        """
        for w in self.sw_list:
            if w.get_name() == weapon.get_name():
                if not w.increase_ammo(weapon.get_ammo()):
                    return False
        self.sw_list.append(weapon)
        print "Yay! " + weapon.get_name() + " added to inventory"
        if self.sw_selected == -1:
            self.next_secondary_weapon()
        return True

    def drop_secondary_weapon(self, weapon):
        """
        Remove a secondary weapon from the inventory
        """
        self.sw_list.pop(self.sw_selected)
        self.sw_selected = self.sw_selected - 1
        print "Wow!", weapon.get_name(), "dropped"
        self.next_secondary_weapon()

    def get_selected_secondary_weapon(self):
        if len(self.sw_list) == 0:
            return None
        return self.sw_list[self.sw_selected]

    def prev_secondary_weapon(self):
        if len(self.sw_list) == 0:
            return
        self.sw_selected = (self.sw_selected - 1) % len(self.sw_list)
        print self.get_selected_secondary_weapon().get_name(), "selected"

    def next_secondary_weapon(self):
        if len(self.sw_list) == 0:
            return
        self.sw_selected = (self.sw_selected + 1) % len(self.sw_list)
        print self.get_selected_secondary_weapon().get_name(), "selected"

