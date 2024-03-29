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
from power_up import PowerUp

class Game:
    screen = None
    screen_size = None
    run = True
    actors_list = None
    player = None
    player_firing = False
    player_charging = 0
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
        if preferences.screen_fullscreen:
            flags |= FULLSCREEN
        # create display
        self.screen = pygame.display.set_mode(preferences.screen_resolution, flags)
        self.screen_size = self.screen.get_size()

        # make mouse cursor invisible
        pygame.mouse.set_visible(False)
        # grabs the mouse, so pygame has complete control over it
        pygame.event.set_grab(True)
        # set title windows and icon
        win_icon = self.load_image("win_icon.png")
        pygame.display.set_caption('Dead Channel')
        pygame.display.set_icon(win_icon)

        # initialize joysticks
        self.init_joysticks()
        # load all images TODO: it could display a "loading" screen
        self.load_images()

    def init_joysticks(self):
        """
        Initialize all joysticks found
        """
        for j in xrange(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(j)
            joystick.init()

    def load_image(self, filename):
        img = pygame.image.load(os.path.join('graphic', filename))
        # disable alpha, it the image contains an alpha layer
        img.set_alpha(None, RLEACCEL)
        img = img.convert()
        # colorkey is the color value that will be reference transparency
        img.set_colorkey((255,255,255), RLEACCEL)
        return img

    def load_images(self):
        """
        Load all image files and convert, setting the colorkey
        """
        self.image_player = []
        for image in ["player_0.png", "player_45.png", "player_90.png",
                      "player_135.png", "player_180.png", "player_225.png",
                      "player_270.png", "player_315.png"]:
            self.image_player.append(self.load_image(image))
        self.image_enemy = self.load_image("enemy.png")
        self.image_enemy_fire = self.load_image("enemy_fire.png")
        self.image_life = self.load_image("life.png")
        self.image_powerup = {}
        for image in ["first_aid_kit", "sw_mult", "sw_frag", "sw_guided",
                      "sw_elet"]:
            self.image_powerup[image] = self.load_image(image+".png")
        self.image_player_fire = {}
        for image in ["fire", "sw_mult", "sw_frag", "sw_guided", "sw_elet"]:
            self.image_player_fire[image] = self.load_image("player_"+image+".png")

    def handle_events(self, ms):
        """
        Handle user's events.
        """
        player = self.player
        preferences = self.preferences
        player_fire = False
        self.player_charging += ms

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

            if preferences.general_input in ("mouse", "keyboard"):
                if type == KEYDOWN:
                    if key == preferences.keyboard_up:
                        player.accel_top()
                    elif key == preferences.keyboard_down:
                        player.accel_bottom()
                    elif key == preferences.keyboard_right:
                        player.accel_right()
                    elif key == preferences.keyboard_left:
                        player.accel_left()
                    elif key == preferences.keyboard_player_play:
                        self.music_player.play()
                    elif key == preferences.keyboard_player_stop:
                        self.music_player.stop()
                    elif key == preferences.keyboard_player_next_track:
                        self.music_player.next_track()
                    elif key == preferences.keyboard_prev_secondary_weapon:
                        player.prev_secondary_weapon()
                    elif key == preferences.keyboard_next_secondary_weapon:
                        player.next_secondary_weapon()
                    elif key == preferences.keyboard_toogle_fullscreen:
                        pygame.display.toggle_fullscreen()
                elif type == KEYUP:
                    if key == preferences.keyboard_down:
                        player.accel_top()
                    elif key == preferences.keyboard_up:
                        player.accel_bottom()
                    elif key == preferences.keyboard_left:
                        player.accel_right()
                    elif key == preferences.keyboard_right:
                        player.accel_left()

                if preferences.general_input == "keyboard":
                    if type == KEYDOWN:
                        if key == preferences.keyboard_fire:
                            player_fire = True
                            self.player_firing = True
                        elif key == preferences.keyboard_secondary_fire:
                            self.player_charging = 0
                        elif key == preferences.keyboard_rot_clock:
                            player.rotate_clock(self.rot_accel)
                        elif key == preferences.keyboard_rot_anti_clock:
                            player.rotate_clock(-self.rot_accel)
                    elif type == KEYUP:
                        if key == preferences.keyboard_rot_clock:
                            player.rotate_clock(-self.rot_accel)
                        elif key == preferences.keyboard_rot_anti_clock:
                            player.rotate_clock(self.rot_accel)
                        elif key == preferences.keyboard_fire:
                            self.player_firing = False
                        elif key == preferences.keyboard_secondary_fire:
                            sw = player.get_selected_secondary_weapon()
                            if sw == None:
                                continue
                            player.fire(self.actors_list["fire"],
                                self.image_player_fire[sw.get_type()], False,
                                self.actors_list["enemies"],
                                self.player_charging)

                elif preferences.general_input == "mouse":
                    if type == MOUSEBUTTONDOWN:
                        # mouse left button is 1, middle is 2, and right is 3
                        if button == preferences.mouse_fire:
                            player_fire = True
                            self.player_firing = True
                        elif button == preferences.mouse_secondary_fire:
                            self.player_charging = 0
                        elif button == preferences.mouse_prev_secondary_weapon:
                            player.prev_secondary_weapon()
                        elif button == preferences.mouse_next_secondary_weapon:
                            player.next_secondary_weapon()
                    elif type == MOUSEBUTTONUP:
                        if button == preferences.mouse_fire:
                            self.player_firing = False
                        elif button == preferences.mouse_secondary_fire:
                            sw = player.get_selected_secondary_weapon()
                            if sw == None:
                                continue
                            player.fire(self.actors_list["fire"],
                                self.image_player_fire[sw.get_type()], False,
                                self.actors_list["enemies"],
                                self.player_charging)

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

            elif preferences.general_input in ("joystick_analogic",
                                       "joystick_d-pad"):
                if type == JOYBUTTONDOWN and joy_id == preferences.joystick_id:
                    if button == preferences.joystick_fire:
                        player_fire = True
                        self.player_firing = True
                    elif button == preferences.joystick_secondary_fire:
                        self.player_charging = 0
                    elif button == preferences.joystick_player_play:
                        self.music_player.play()
                    elif button == preferences.joystick_player_stop:
                        self.music_player.stop()
                    elif button == preferences.joystick_player_next_track:
                        self.music_player.next_track()
                    elif button == preferences.joystick_prev_secondary_weapon:
                        player.prev_secondary_weapon()
                    elif button == preferences.joystick_next_secondary_weapon:
                        player.next_secondary_weapon()
                elif type == JOYBUTTONUP and joy_id == preferences.joystick_id:
                    if button == preferences.joystick_fire:
                        self.player_firing = False
                    elif button == preferences.joystick_secondary_fire:
                        sw = player.get_selected_secondary_weapon()
                        if sw == None:
                            continue
                        player.fire(self.actors_list["fire"],
                            self.image_player_fire[sw.get_type()], False,
                            self.actors_list["enemies"],
                            self.player_charging)


                if preferences.general_input == "joystick_analogic":
                    if type == JOYAXISMOTION and joy_id == preferences.joystick_id:
                        if axis == preferences.j_axis_x:
                            if abs(value) > preferences.joystick_deadzone:
                                h_speed = value * preferences.joystick_sensitivity
                            else:
                                h_speed = 0
                            player.set_speed([h_speed, player.get_speed()[1]])
                        elif axis == preferences.j_axis_y:
                            if abs(value) > preferences.joystick_deadzone:
                                v_speed = value * preferences.joystick_sensitivity
                            else:
                                v_speed = 0
                            player.set_speed([player.get_speed()[0], v_speed])
                        elif axis == preferences.j_axis_z:
                            if abs(value) < preferences.joystick_deadzone:
                                value = 0
                            rot_speed = int(value* preferences.joystick_sensitivity)
                            player.set_rotation_speed(rot_speed)

                elif preferences.general_input == "joystick_d-pad":
                    if type == JOYHATMOTION and joy_id == preferences.joystick_id:
                        accel = player.get_accel()
                        speed = [value[0] * accel[0], -value[1] * accel[1]]
                        player.set_speed(speed)
                    elif type == JOYBUTTONDOWN and \
                         joy_id == preferences.joystick_id:
                        if button == preferences.joystick_rot_clock:
                                player.rotate_clock(self.rot_accel)
                        elif button == preferences.joystick_rot_anti_clock:
                                player.rotate_clock(-self.rot_accel)
                    elif type == JOYBUTTONUP and joy_id == preferences.joystick_id:
                        if button == preferences.joystick_rot_clock:
                                player.rotate_clock(-self.rot_accel)
                        elif button == preferences.joystick_rot_anti_clock:
                                player.rotate_clock(self.rot_accel)

        if player_fire or self.player_firing:
            player.fire(self.actors_list["fire"],
                        self.image_player_fire["fire"])

    def actors_update(self, dt, ms):
        """
        Updates actors and background
        """
        self.background.update(dt)

        x, y = self.player.get_pos()

        for actor in self.actors_list.values():
            actor.update(dt, ms, self.counter, x, y)

        self.hud.update(self.screen, ms)

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
            hitted = pygame.sprite.groupcollide(actor, actors_list, 0, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            for o in hitted.keys():
                o.do_collision()
            return hitted

        # check if the actor is a sprite
        elif isinstance(actor, pygame.sprite.Sprite):
            # third argument is dokill (if true the object will be killed)
            collided_list = pygame.sprite.spritecollide(actor, actors_list, 0)
            for obj in collided_list:
                if isinstance(obj, PowerUp):
                    if action(obj.get_type(), obj.get_pu_attr()):
                        obj.kill()
                else:
                    action()
                    obj.kill()
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

    def manage_elements(self, stage):
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
        L = stage.pop(self.counter)
        for element in L:
            if element.type == "enemy":
                # FIX: Create enemies and itens similarly (create a generic class)
                enemy = Enemy([0, 0], 0, int(element.life), element.behaviour,
                              0, self.image_enemy)
                size = enemy.get_size()
                # FIX: Should random y be kept like below?
                y = int(element.pos_y)
                if y == 0:
                    y = Random.randint(size[1] / 2, self.screen_size[1] - size[1] / 2)
                pos = [self.screen_size[0] + size[0] / 2, y]
                enemy.set_pos(pos)
                # add sprite to group
                self.actors_list["enemies"].add(enemy)
            elif element.type in ["first_aid_kit", "sw_mult", "sw_frag",
                                  "sw_guided", "sw_elet"]:
                powerup = PowerUp([0,0], int(element.time),
                                  [int(element.speed_x), int(element.speed_y)],
                                  element.type, element.pu_attr,
                                  self.image_powerup[element.type])
                size = powerup.get_size()
                y = Random.randint(size[1] / 2, self.screen_size[1] - size[1] / 2)
                pos = [self.screen_size[0] + size[0] / 2, y]
                powerup.set_pos(pos)
                self.actors_list["powerups"].add(powerup)
            elif element.type == "background":
                self.background.nextTile(element.image, 1)

    def loop(self):
        """
        Main loop
        """

        # loads stage configuration
        stage = Stage("stage1.xml")
        stage.buildStage()
        self.counter = 0

        # creates the background
        self.background = Background("earth.jpg", "321.png")

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

        # loads music player
        self.music_player = Music_player(self.hud,
            self.preferences.general_music_volume,
            self.preferences.general_use_default_setlist,
            self.preferences.general_music_dir)
        # loads next music
        self.music_player.load_next()
        # Starts playing music
        self.music_player.play()

        while self.run:
            # miliseconds since last frame
            ms = clock.tick(1000/dt)

            # handle input
            self.handle_events(ms)
            # update all the game elements
            self.actors_update(dt, ms)
            self.actors_act()

            # create enemies based on xml file
            self.manage_elements(stage)

            # draw the elements to the back buffer
            self.actors_draw()
            # flip the front and back buffer
            pygame.display.flip()
            self.counter += 1
