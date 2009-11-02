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
        # convert the image so it won't be done every blit
        # it improves the performance
        image = pygame.image.load(image).convert()
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
        if DEBUG:
            print "BACKGROUND POSITION: " + str(self.pos[0])

    def draw(self,screen):
        """
        Draws the background
        """
        screen.blit(self.image, self.pos)


class Game:
    screen = None
    screen_size = None
    run = True

    def __init__(self, size, fullscreen):
        """
        Starts pygamge, defines resolution, sets caption, disable mouse cursor.
        """
        actors = {}
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

    def handle_events(self):
        """
        Handle user's events.
        """
        for event in pygame.event.get():
            type = event.type
            if type in (KEYDOWN, KEYUP):
                key = event.key
            if type == QUIT:
                self.run = False
            elif type == KEYDOWN and key == K_ESCAPE:
                self.run = False

    def actors_update(self, dt):
        self.background.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)

    def loop(self):
        """
        Main loop
        """
        # creates the background
        self.background = Background("tile.png")

        #starts clock
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            clock.tick(1000/dt)

            # handle input
            self.handle_events()
            # update all the game elements
            self.actors_update(dt)
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

