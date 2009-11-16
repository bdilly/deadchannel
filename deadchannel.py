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
    print "\t%s [-h|--help]" % prog
    print

def parse_opts(argv):
    """
    Parses the command line argument
    """
    # get options and arguments using getopt
    try:
        opts, args = getopt.gnu_getopt(argv[1 :], "h", ["help"])
    except getopt.GetoptError:
        # if command line is wrong, print usage info and exit
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            help()
            sys.exit(0)

def main(argv):
    """
    Gets command line options and starts the game
    """
    # set directories and files
    abspath = os.path.abspath(argv[0])
    dir = os.path.dirname(abspath)
    DATADIR = os.path.join(dir, 'data')
    CODEDIR = os.path.join(dir, 'code')
    DEFPREFFILE = os.path.join(DATADIR, 'default_preferences.cfg')
    if os.name == 'posix':
        HOMEDIR = os.environ['HOME']
        GAMEDIR = os.path.join(HOMEDIR, '.deadchannel')
        if not os.path.isdir(GAMEDIR):
            try:
                os.mkdir(GAMEDIR, 0755)
            except OSError:
                GAMEDIR = HOMEDIR
        PREFFILE = os.path.join(GAMEDIR, 'preferences.cfg')
    else:
        PREFFILE = os.path.join('data', 'preferences.cfg')
    # change to the correct directory to find resources
    os.chdir(DATADIR)
    sys.path.insert(0, CODEDIR)

    parse_opts(argv)

    from game import Game
    from preferences import Preferences
    preferences = Preferences(PREFFILE, DEFPREFFILE)
    game = Game(preferences)
    # starts game's main loop
    game.loop()


# only executes code when a file is invoked as a script and not just imported
# calls main if the script is executed
if __name__ == '__main__':
    main(sys.argv)

