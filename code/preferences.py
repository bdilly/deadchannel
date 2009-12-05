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
import os, re
import shutil

class Preferences(object):
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

        # autogenerate the attributes for each item on the config file.
        self.autogen_attributes()

    def copy_default(self, default_filename, filename):
        try:
            shutil.copy(default_filename, filename)
            self.__init__(filename, default_filename)
        except IOError:
            print "Warning: preferences file couldn't be created"

    def parse_config_item(self, value):
        """
        Gather the type we're dealing with and return the value
        on its real type.
        """
        resolution_type = lambda s: [ int(s.split("x")[0]),
                                      int(s.split("x")[1]) ]

        patterns = [ [resolution_type, re.compile("[0-9]+x[0-9]+")],
                     [float, re.compile("[0-9]+\.[0-9]+")],
                     [int, re.compile("[0-9]+")],
                     [str, re.compile(".*")] ]

        for ty, regex in patterns:
            if regex.match(value):
                return ty(value)

    def autogen_attributes(self):
        """
        Get tuples from ConfigParser and autogenerate attributes
        based on the section and preference name, example:
          [keyboard]
            up = 273
            down = ...
        This should turn into:
          self.keyboard_up = 273
          self.keyboard_down = ...
        """
        for section in self.conf.sections():
            for item, value in self.conf.items(section):
                attr_name   = "%s_%s" % (section, item)
                attr_value  = self.parse_config_item(value)
                self.__setattr__(attr_name, attr_value)
                print section, item, attr_value

