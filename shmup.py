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


# imports module that provides access to some objects used or maintained
# by the interpreter. Useful to get argv and path.
import sys
# operational system routines
import os
# imports parser for command line arguments in sys.argv
import getopt
# random will be useful for lots of things, as position where enemies will be
# placed
import random as Random
# imports all the available pygame modules
import pygame
# puts set of constants and functions very handy into the global namespace
# of our script
from pygame.locals import *

# sets resources directories
data_dir = os.path.join(".","data")
images_dir = os.path.join(data_dir, "graphic")
audio_dir = os.path.join(data_dir, "audio")
music_dir = os.path.join(data_dir, "music")

# DEBUG enable debug output
DEBUG = True


class GameObject(pygame.sprite.Sprite):
    """
    Base class that represents all the objects in game.
    It inherits from Sprite and has a rect that makes easy to move the image
    """
    def __init__(self, image, position, speed = None):
        """
        Load the object image, create a rect, set position and
        speed (static by default).
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.set_pos(position)
        self.set_speed(speed or (0,0))

    def update(self, dt):
        """
        Updates the position and destroy the object if it's out of the screen
        """
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
        if (self.rect.right < self.area.left) or \
            (self.rect.bottom < self.area.top) or \
            (self.rect.top > self.area.bottom):
            self.kill()

    def get_speed(self):
        """
        Return object speed
        """
        return self.speed

    def set_speed(self, speed):
        """
        Set object speed
        """
        self.speed = speed

    def get_pos(self):
        """
        Return object position
        """
        return (self.rect.center[0],
                self.rect.center[1])

    def set_pos(self,pos):
        """
        Set object position
        """
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        """
        Get image size
        """
        return self.image.get_size()


class Bullet(GameObject):
    """
    Class for bullets.
    """
    def __init__(self, position, speed=None, image=None, list=None):
        GameObject.__init__( self, image, position, speed )
        if list != None:
            self.add( list )


class Actor(GameObject):
    """
    Base class for all characters
    """
    def __init__(self, position, life=1, speed=[0,0], image=None):
        """
        Set acceleration and image
        """
        self.acceleration = [3,3]
        GameObject.__init__(self, image, position, speed)
        self.set_life(life)

    def get_life(self):
        """
        Return the enemy's life
        """
        return self.life

    def set_life(self, life):
        """
        Set the character's life
        """
        self.life = life

    def do_collision(self):
        """
        Kill object if life reaches 0 when colliding
        """
        if self.get_life() == 0:
            self.kill()
        else:
            self.set_life(self.get_life() -1)
        if DEBUG:
            print "Collision detected. Life remaining: " + str(self.get_life())

    def is_dead(self):
        """
        Return true if the object's life reached 0
        """
        return self.get_life() == 0

    def accel_top(self):
        """
        Reduce vertical speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        """
        Increase vertical speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        """
        Reduce horizontal speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        """
        Increase horizontal speed
        """
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))

    def fire(self, fire_list, image):
        """
        Fire a bullet in the same position with double speed.
        """
        # create a list with speed in axis x and y
        speed = list(self.get_speed())
        # double horizontal speed
        speed[0] *= 2
        Bullet(self.get_pos(), speed, image, fire_list)


class Enemy(Actor):
    """
    Class for enemy characters
    """
    def __init__(self, position, life=1, speed=None, image=None):
        """
        Creates an enemy character
        """
        Actor.__init__(self, position, life, speed, image)


class Player(Actor):
    """
    Represents the player avatar.
    """
    def __init__(self, position, life=10, image=None):
        """
        Initialize object, setting position, life, xp, gold
        """
        Actor.__init__(self, position, life, [0, 0], image)
        self.set_xp(0)
        self.set_gold(0)

    def update(self, dt):
        """
        Override GameObjecte update()
        Keep the player inside the screen instead of killing it
        """
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

    def get_gold(self):
        """
        Return gold
        """
        return self.gold

    def set_gold(self, gold):
        """
        Set gold
        """
        self.gold = gold

    def fire(self, fire_list, image):
        """
        Fire a bullet with double speed
        """
        pos = self.get_pos()
        Bullet(pos, [8, 0], image, fire_list)


class Background:
    """
    It's the animated game background created with tiles.
    """
    image = None
    pos = None

    def __init__(self, image):
        """
        Creates a surface with tiles repeated until cover the entire screen.
        """
        # sets the absolute path
        image = os.path.join(images_dir, image)
        # loads the image
        image = pygame.image.load(image)
        # disables alpha
        image.set_alpha(None, RLEACCEL)
        # converts the image so it won't be done every blit
        # it improves the performance
        image = image.convert()
        self.size = image.get_size()
        self.pos = [0, 0]
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        # ceil returns the ceiling of x as a float
        # we want the size of the screen plus a tile
        w = (ceil(float(screen_size[0]) / self.size[0]) + 1) * self.size[0]
        h = (ceil(float(screen_size[1]) / self.size[1]) + 1) * self.size[1]

        # creates a surface with width w and height h
        back = pygame.Surface((w, h))

        # covers the entire screen
        for i in range((back.get_size()[0]/self.size[0])):
            for j in range((back.get_size()[1]/self.size[1])):
                back.blit(image, (i * self.size[0], j * self.size[1]))

        self.image = back

    def update(self, dt):
        """
        Moves the background to the left
        """
        self.pos[0] -= 1
        # when it reaches the end, moves the background for the start point
        if (self.pos[0] < -self.size[0]):
            self.pos[0] += self.size[0]

    def draw(self,screen):
        """
        Draws the background
        """
        screen.blit(self.image, self.pos)


class Game:
    screen = None
    screen_size = None
    run = True
    actors_list = None
    player = None
    interval = 0

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
        # change the title windows to "schump++"
        pygame.display.set_caption('schmup++');

        # load all images TODO: it could display a "loading" screen
        self.load_images()

    def load_images(self):
        """
        Load all image files and convert, setting the colorkey
        """
        def load_image(filename):
            img = pygame.image.load(os.path.join(images_dir, filename))
            # disable alpha, it the image contains an alpha layer
            img.set_alpha(None, RLEACCEL)
            img = img.convert()
            # colorkey is the color value that will be reference transparency
            img.set_colorkey((255,255,255), RLEACCEL)
            return img

        self.image_player = load_image("player.png")
        self.image_player_fire = load_image("player_fire.png")
        self.image_enemy = load_image("enemy.png")
        self.image_enemy_fire = load_image("enemy_fire.png")

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
                elif key == K_SPACE:
                    self.interval = 0
                    player.fire(self.actors_list["fire"],
                                self.image_player_fire)
                elif key == K_UP:
                    player.accel_top()
                elif key == K_DOWN:
                    player.accel_bottom()
                elif key == K_RIGHT:
                    player.accel_right()
                elif key == K_LEFT:
                    player.accel_left()

            elif type == KEYUP:
                if key == K_DOWN:
                    player.accel_top()
                elif key == K_UP:
                    player.accel_bottom()
                elif key == K_LEFT:
                    player.accel_right()
                elif key == K_RIGHT:
                    player.accel_left()

            keys = pygame.key.get_pressed()
            if self.interval > 10:
                self.interval = 0
                if keys[K_SPACE]:
                    player.fire(self.actors_list["fire"],
                                self.image_player_fire)

    def actors_update(self, dt):
        """
        Updates actors and background
        """
        self.background.update(dt)

        for actor in self.actors_list.values():
            actor.update(dt)

    def actors_draw(self):
        """
        Draw actors and background
        """
        self.background.draw(self.screen)

        for actor in self.actors_list.values():
            actor.draw(self.screen)

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
            enemy = Enemy([0, 0], 1, [-4, 0], self.image_enemy)
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

        # the player starts from the left center point of the screen
        pos = [0, self.screen_size[1] / 2]
        self.player = Player(pos, 5, self.image_player)
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

            if DEBUG:
                print "FPS: %0.2f" % clock.get_fps()


def help():
    """
    Prints basic help for this game.
    """
    print "Commands:"
    print "\tESC\tQuit game"

def usage():
    """
    Prints usage info for this game.
    """
    prog = sys.argv[0]
    print "Usage:"
    print "\t%s [-f|--fullscreen] [-r <YxZ>|--resolution=<YxZ>]" % prog
    print

def parse_opts(argv):
    """
    Parses the command line argument and return the options
    """
    # get options and arguments using getopt
    try:
        opts, args = getopt.gnu_getopt(argv[1 :], "hfr:",
                                       ["help", "fullscreen", "resolution="])
    except getopt.GetoptError:
        # if command line is wrong, print usage info and exit
        usage()
        sys.exit(2)

    # default options
    options = {"fullscreen": False, "resolution": (800,600)}

    for o, a in opts:
        if o in ("-f", "--fullscreen"):
            options["fullscreen"] = True
        elif o in ("-h", "--help"):
            usage()
            help()
            sys.exit(0)
        elif o in ("-r", "--resolution"):
            # the resolution can be providded as 1x1 1X1 1,1 1:1
            a = a.lower()
            resolution = a.split("x")
            if len(resolution) == 2 :
                options["resolution"] = [ int(resolution[0]),
                                          int(resolution[1])]
    return options

def main(argv):
    """
    Gets command line options and starts the game
    """
    # change to the correct directory to find graphical resources and others
    abspath = os.path.abspath(argv[0])
    dir = os.path.dirname(abspath)
    os.chdir(dir)

    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    # starts game's main loop
    game.loop()


# only executes code when a file is invoked as a script and not just imported
# calls main if the script is executed
if __name__ == '__main__':
    main(sys.argv)

