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
# imports parser for command line arguments in sys.argv
import getopt
# imports all the available pygame modules
import pygame
# puts set of constants and functions very handy into the global namespace
# of our script
from pygame.locals import *

# DEBUG enable debug output
DEBUG = True


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

    def loop(self):
        """
        Main loop
        """
        #starts clock
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            clock.tick(1000/dt)

            self.handle_events()
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
    options = {"fullscreen": False, "resolution": (640,480)}

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
    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    # starts game's main loop
    game.loop()


# only executes code when a file is invoked as a script and not just imported
# calls main if the script is executed
if __name__ == '__main__':
    main(sys.argv)

