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

import os
# random will be useful for lots of things, as position where enemies will be
# placed
import random as Random
# imports all the available pygame modules
import pygame
# puts set of constants and functions very handy into the global namespace
# of our script
from pygame.locals import *
# game modules
from background import Background
from player import Player
from enemy import Enemy
from hud import HUD

class Game:
    screen = None
    screen_size = None
    run = True
    actors_list = None
    player = None
    interval = 0
    # if false, use keys to rotate the player. otherwise use analogic input
    analogic = False
    keys_up = [K_UP, K_w]
    keys_down = [K_DOWN, K_s]
    keys_right = [K_RIGHT, K_d]
    keys_left = [K_LEFT, K_a]
    keys_fire = [K_SPACE]
    keys_rot_clock = [K_e]
    keys_rot_anti_clock = [K_q]

    def __init__(self, size, fullscreen):
        """
        Starts pygamge, defines resolution, sets caption, disable mouse cursor.
        """
        # initialize all needed pygame modules
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        # create display
        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()

        # make mouse cursor invisible
        pygame.mouse.set_visible(0)
        # change the title windows to "deadchannel"
        pygame.display.set_caption('deadchannel');

        # load all images TODO: it could display a "loading" screen
        self.load_images()

    def load_images(self):
        """
        Load all image files and convert, setting the colorkey
        """
        def load_image(filename):
            img = pygame.image.load(os.path.join('graphic', filename))
            # disable alpha, it the image contains an alpha layer
            img.set_alpha(None, RLEACCEL)
            img = img.convert()
            # colorkey is the color value that will be reference transparency
            img.set_colorkey((255,255,255), RLEACCEL)
            return img

        self.image_player = []
        for image in ["player_0.png", "player_45.png", "player_90.png",
                      "player_135.png", "player_180.png", "player_225.png",
                      "player_270.png", "player_315.png"]:
            self.image_player.append(load_image(image))
        self.image_player_fire = load_image("player_fire.png")
        self.image_enemy = load_image("enemy.png")
        self.image_enemy_fire = load_image("enemy_fire.png")
        self.image_life = load_image("life.png")

    def handle_events(self):
        """
        Handle user's events.
        """
        player = self.player

        for event in pygame.event.get():
            type = event.type
            if type in (KEYDOWN, KEYUP):
                key = event.key
            if type == QUIT:
                self.run = False

            elif type == KEYDOWN:
                if key == K_ESCAPE:
                    self.run = False
                elif key in self.keys_up:
                    player.accel_top()
                elif key in self.keys_down:
                    player.accel_bottom()
                elif key in self.keys_right:
                    player.accel_right()
                elif key in self.keys_left:
                    player.accel_left()
                elif not self.analogic:
                    if key in self.keys_fire:
                        self.interval = 0
                        player.fire(self.actors_list["fire"],
                                    self.image_player_fire)
                    elif key in self.keys_rot_clock:
                        player.rotate_clock()
                    elif key in self.keys_rot_anti_clock:
                        player.rotate_anti_clock()

            elif type == KEYUP:
                if key in self.keys_down:
                    player.accel_top()
                elif key in self.keys_up:
                    player.accel_bottom()
                elif key in self.keys_left:
                    player.accel_right()
                elif key in self.keys_right:
                    player.accel_left()
                elif not self.analogic:
                    if key in self.keys_rot_clock:
                        player.rotate_anti_clock()
                    elif key in self.keys_rot_anti_clock:
                        player.rotate_clock()

            if not self.analogic:
                keys = pygame.key.get_pressed()
                if self.interval > 10:
                    self.interval = 0
                    for key in keys:
                        if key in self.keys_fire:
                            player.fire(self.actors_list["fire"],
                                        self.image_player_fire)


    def actors_update(self, dt):
        """
        Updates actors and background
        """
        self.background.update(dt)

        for actor in self.actors_list.values():
            actor.update(dt)

        self.hud.update(dt)

    def actors_draw(self):
        """
        Draw actors and background
        """
        self.background.draw(self.screen)

        for actor in self.actors_list.values():
            actor.draw(self.screen)

        # draw the hud after all the actors, so it will be at the top
        self.hud.draw(self.screen)

    def actor_check_hit(self, actor, actors_list, action):
        """
        Check if an actor hitted in others provided by a list. If it does,
        call action.
        """
        # check if the actor is instance of a group of sprites
        if isinstance(actor, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(actor, actors_list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        # check if the actor is a sprite
        elif isinstance(actor, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(actor, actors_list, 1):
                action()
            return actor.is_dead()

    def actors_act(self):
        """
        Check for hits and if the player is dead.
        """
        # check if player was hitted by a bullet
        self.actor_check_hit(self.player, self.actors_list["enemies_fire"],
                             self.player.do_collision)
        if self.player.is_dead():
            self.run = False
            return

        # check if the player collided with an enemy
        self.actor_check_hit(self.player, self.actors_list["enemies"],
                             self.player.do_collision)
        if self.player.is_dead():
            self.run = False
            return

        # check if enemies were hitted by a bullet
        hitted = self.actor_check_hit(self.actors_list["fire"],
                                      self.actors_list["enemies"],
                                          Enemy.do_collision)

        # increase xp based on hits
        self.player.set_xp(self.player.get_xp() + len(hitted))

    def manage_enemies(self):
        """
        Creates enemies randomly at random positions and randomly fire
        """
        self.ticks += 1
        # enemies fire randomly
        if self.ticks > Random.randint(20,30):
            for enemy in self.actors_list["enemies"].sprites():
                if Random.randint(0,10) > 5:
                    enemy.fire(self.actors_list["enemies_fire"],
                               self.image_enemy_fire)
                self.ticks = 0

        # creates enemies randomly
        r = Random.randint(0,100)
        # the bigger the multiplier, harder to create a new enemy
        # 100 / multiplier is the max of enemies on the screen at the same time
        multiplier = 20
        if (r > (multiplier * len(self.actors_list["enemies"]))):
            # chooses one between the possible behaviours
            behaviour = Random.choice(Enemy.get_behaviours())
            enemy = Enemy([0, 0], 270, 1, behaviour, 0, self.image_enemy)
            size = enemy.get_size()
            y = Random.randint(size[1] / 2, self.screen_size[1] - size[1] / 2)
            pos = [self.screen_size[0] + size[0] / 2, y]
            enemy.set_pos(pos)
            # add sprite to group
            self.actors_list["enemies"].add(enemy)

    def loop(self):
        """
        Main loop
        """
        # creates the background
        self.background = Background("tile.png")

        #starts clock
        clock = pygame.time.Clock()
        dt = 16
        self.ticks = 0
        self.interval = 1

        # the player starts from the left center point of the screen
        pos = [0, self.screen_size[1] / 2]
        self.player = Player(pos, life=10, image=self.image_player)

        self.hud = HUD(self.player, [20, 30], self.image_life)
        # RenderPlain is a container class for many Sprites
        self.actors_list = {
            "enemies" : pygame.sprite.RenderPlain(),
            "enemies_fire" : pygame.sprite.RenderPlain(),
            "player": pygame.sprite.RenderPlain(self.player),
            "fire" : pygame.sprite.RenderPlain(),
        }

        while self.run:
            clock.tick(1000/dt)

            # handle input
            self.handle_events()
            # update all the game elements
            self.actors_update(dt)
            self.actors_act()
            # create enemies
            self.manage_enemies()
            # draw the elements to the back buffer
            self.actors_draw()
            # flip the front and back buffer
            pygame.display.flip()

