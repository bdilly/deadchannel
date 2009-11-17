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
from stage import Stage
from music import Music_player
from first_aid_kit import FirstAidKit
from power_up import PowerUp

class Game:
    screen = None
    screen_size = None
    run = True
    actors_list = None
    player = None
    rot_accel = 2

    def __init__(self, preferences):
        """
        Starts pygamge, defines resolution, sets caption, disable mouse cursor.
        """
        # Set mixer arguments before modules initialization
        pygame.mixer.pre_init(44100)
        # initialize all needed pygame modules
        self.preferences = preferences
        pygame.init()
        flags = DOUBLEBUF
        if preferences.fullscreen:
            flags |= FULLSCREEN
        # create display
        self.screen = pygame.display.set_mode(preferences.resolution, flags)
        self.screen_size = self.screen.get_size()

        # make mouse cursor invisible
        pygame.mouse.set_visible(False)
        # grabs the mouse, so pygame has complete control over it
        pygame.event.set_grab(True)
        # set title windows
        pygame.display.set_caption('Dead Channel');

        # initialize joysticks
        self.init_joysticks()
        # load all images TODO: it could display a "loading" screen
        self.load_images()
        # loads music player
        self.music_player = Music_player()

    def init_joysticks(self):
        """
        Initialize all joysticks found
        """
        for j in xrange(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(j)
            joystick.init()

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
        self.image_first_aid_kit = load_image("first_aid_kit.png")

    def handle_events(self):
        """
        Handle user's events.
        """
        player = self.player
        preferences = self.preferences

        for event in pygame.event.get():
            type = event.type
            if type in (KEYDOWN, KEYUP):
                key = event.key
            elif type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                button = event.button
            elif type == MOUSEMOTION:
                mouse_rel = event.rel
            elif type in (JOYBUTTONUP, JOYBUTTONDOWN):
                joy_id = event.joy
                button = event.button
            elif type == JOYAXISMOTION:
                joy_id = event.joy
                axis = event.axis
                value = event.value
            elif type == JOYHATMOTION:
                joy_id = event.joy
                value = event.value
            elif type == QUIT:
                self.run = False
            if type == KEYDOWN:
                if key == K_ESCAPE:
                    self.run = False

            if preferences.input in ("mouse", "keyboard"):
                if type == KEYDOWN:
                    if key == preferences.key_up:
                        player.accel_top()
                    elif key == preferences.key_down:
                        player.accel_bottom()
                    elif key == preferences.key_right:
                        player.accel_right()
                    elif key == preferences.key_left:
                        player.accel_left()
                    elif key == preferences.key_player_play:
                        self.music_player.play()
                    elif key == preferences.key_player_stop:
                        self.music_player.stop()
                    elif key == preferences.key_player_next_track:
                        self.music_player.next_track()
                elif type == KEYUP:
                    if key == preferences.key_down:
                        player.accel_top()
                    elif key == preferences.key_up:
                        player.accel_bottom()
                    elif key == preferences.key_left:
                        player.accel_right()
                    elif key == preferences.key_right:
                        player.accel_left()

                if preferences.input == "keyboard":
                    if type == KEYDOWN:
                        if key == preferences.key_fire:
                            player.fire(self.actors_list["fire"],
                                        self.image_player_fire)
                        elif key == preferences.key_rot_clock:
                            player.rotate_clock(self.rot_accel)
                        elif key == preferences.key_rot_anti_clock:
                            player.rotate_clock(-self.rot_accel)
                    elif type == KEYUP:
                        if key == preferences.key_rot_clock:
                            player.rotate_clock(-self.rot_accel)
                        elif key == preferences.key_rot_anti_clock:
                            player.rotate_clock(self.rot_accel)

                elif preferences.input == "mouse":
                    if type == MOUSEBUTTONDOWN:
                        # mouse left button is 1, middle is 2, and right is 3
                        if button == preferences.mouse_fire:
                            player.fire(self.actors_list["fire"],
                                        self.image_player_fire)
                    elif type == MOUSEMOTION:
                        # rel is a tuple with x and y relative movements
                        # if player move the cursor down or left, it has
                        # the same effect
                        #FIXME HACK: the first rel is a huge number, the
                        # difference between 0, 0 and the curson position.
                        # So it needs to be avoided.
                        # This hack should be removed after we include
                        # screens before the game screen
                        if mouse_rel[0] < 100 and mouse_rel[1] < 100:
                            rot = player.get_rotation()
                            rot = rot + int((mouse_rel[0] + mouse_rel[1]) *\
                                             preferences.mouse_sensitivity)
                            player.set_rotation(rot)

            elif preferences.input == "joystick_analogic":
                if type == JOYAXISMOTION and joy_id == preferences.joy_id:
                    if axis == preferences.j_axis_x:
                        if abs(value) > preferences.joy_deadzone:
                            h_speed = value * preferences.joy_sensitivity
                        else:
                            h_speed = 0
                        player.set_speed([h_speed, player.get_speed()[1]])
                    elif axis == preferences.j_axis_y:
                        if abs(value) > preferences.joy_deadzone:
                            v_speed = value * preferences.joy_sensitivity
                        else:
                            v_speed = 0
                        player.set_speed([player.get_speed()[0], v_speed])
                    elif axis == preferences.j_axis_z:
                        if abs(value) < preferences.joy_deadzone:
                            value = 0
                        rot_speed = int(value * preferences.joy_sensitivity)
                        player.set_rotation_speed(rot_speed)
                elif type == JOYBUTTONDOWN and joy_id == preferences.joy_id:
                    if button == preferences.j_bt_fire:
                        player.fire(self.actors_list["fire"],
                                    self.image_player_fire)

            elif preferences.input == "joystick_d-pad":
                if type == JOYHATMOTION and joy_id == preferences.joy_id:
                    accel = player.get_accel()
                    speed = [value[0] * accel[0], -value[1] * accel[1]]
                    player.set_speed(speed)
                elif type == JOYBUTTONDOWN and joy_id == preferences.joy_id:
                    if button == preferences.j_bt_fire:
                        player.fire(self.actors_list["fire"],
                                    self.image_player_fire)
                    elif button == preferences.j_bt_rot_clock:
                            player.rotate_clock(self.rot_accel)
                    elif button == preferences.j_bt_rot_anti_clock:
                            player.rotate_clock(-self.rot_accel)
                elif type == JOYBUTTONUP and joy_id == preferences.joy_id:
                    if button == preferences.j_bt_rot_clock:
                            player.rotate_clock(-self.rot_accel)
                    elif button == preferences.j_bt_rot_anti_clock:
                            player.rotate_clock(self.rot_accel)

    def actors_update(self, dt, ms):
        """
        Updates actors and background
        """
        self.background.update(dt)

        for actor in self.actors_list.values():
            actor.update(dt, ms)

        self.hud.update(dt, ms)

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
            # third argument is dokill (if true the object will be killed
            collided_list = pygame.sprite.spritecollide(actor, actors_list, 1)
            for obj in collided_list:
                if isinstance(obj, PowerUp):
                    action(obj.get_type(), obj.get_special())
                else:
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

        # check if the player get a powerup
        self.actor_check_hit(self.player, self.actors_list["powerups"],
                             self.player.get_powerup)

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

    def manage_elements(self, stage, counter):
        """
        Creates enemies and itens based on the xml parsed file
        """
        self.ticks += 1
        # enemies fire randomly
        if self.ticks > Random.randint(20,30):
            for enemy in self.actors_list["enemies"].sprites():
                if Random.randint(0,10) > 5:
                    enemy.fire(self.actors_list["enemies_fire"],
                               self.image_enemy_fire)
                self.ticks = 0

        # creates enemies based on xml file
        L = stage.pop(counter)
        for element in L:
            if element.type == "enemy":
                # FIX: Create enemies and itens similarly (create a generic class)
                enemy = Enemy([0, 0], element.rot, element.life, element.behaviour,
                              element.rotspeed, self.image_enemy)
                size = enemy.get_size()
                y = Random.randint(size[1] / 2, self.screen_size[1] - size[1] / 2)
                pos = [self.screen_size[0] + size[0] / 2, y]
                enemy.set_pos(pos)
                # add sprite to group
                self.actors_list["enemies"].add(enemy)
            elif element.type == "first_aid_kit":
                first_aid = FirstAidKit([0,0], element.life,
                                        [element.speed_x, element.speed_y],
                                        int(element.special),
                                        self.image_first_aid_kit)
                size = first_aid.get_size()
                y = Random.randint(size[1] / 2, self.screen_size[1] - size[1] / 2)
                pos = [self.screen_size[0] + size[0] / 2, y]
                first_aid.set_pos(pos)
                self.actors_list["powerups"].add(first_aid)
            else:
                print "Not an enemy, will be handled soon! ;)"

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
            "powerups" : pygame.sprite.RenderPlain(),
        }

        stage = Stage("stage1.xml")
        stage.buildStage()
        counter = 0

        # loads next music
        self.music_player.load_next()
        # Starts playing music
        self.music_player.play()

        while self.run:
            # miliseconds since last frame
            ms = clock.tick(1000/dt)

            # handle input
            self.handle_events()
            # update all the game elements
            self.actors_update(dt, ms)
            self.actors_act()

            # create enemies based on xml file
            self.manage_elements(stage, counter)

            # draw the elements to the back buffer
            self.actors_draw()
            # flip the front and back buffer
            pygame.display.flip()
            counter += 1
