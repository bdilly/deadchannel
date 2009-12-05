#!/usr/bin/env python
# -*- coding: utf-8 (i think) -*-

#----------------------------------------------------------------------
# Author:
#   João Corrêa <joao@livewire.com.br>
#   Bruno Dilly <bruno.dilly@brunodilly.org>
#
# Copyright (C) 2009 João Corrêa
#
# Released under GNU GPL, read the file 'COPYING' for more information
# ----------------------------------------------------------------------

import xml
import xml.dom
import xml.dom.minidom

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Item:
    def __init__(self, node):
        for tag in ['type', 'cc']:
            setattr(self, tag, self.get_element(tag, node))

    def get_element(self, tag, node):
        return node.getElementsByTagName(tag)[0].childNodes[0].nodeValue

class Backg(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        for tag in ['image', 'layer']:
            setattr(self, tag, self.get_element(tag, node))

class Enemy(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        for tag in ['pos_x', 'pos_y', 'behaviour', 'life', 'image', 'speed']:
            setattr(self, tag, self.get_element(tag, node))

class PU(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        for tag in ['pos_x', 'pos_y', 'speed_x', 'speed_y', 'time']:
            setattr(self, tag, self.get_element(tag, node))
        self.pu_attr = {}

class Sw(PU):
    def __init__(self, node):
        PU.__init__(self, node)
        for tag in ['name', 'ammo', 'max_ammo', 'cooldown', 'heating',
                    'max_charge', 'distance']:
            self.pu_attr[tag] = self.get_element(tag, node)

class Mult(Sw):
    def __init__(self, node):
        Sw.__init__(self, node)
        for tag in ['radius', 'simultaneous_shoots']:
            self.pu_attr[tag] = self.get_element(tag, node)

class Frag(Sw):
    def __init__(self, node):
        Sw.__init__(self, node)
        for tag in ['fragments']:
            self.pu_attr[tag] = self.get_element(tag, node)

class FirstAidKit(PU):
    def __init__(self, node):
        PU.__init__(self, node)
        for tag in ['life']:
            self.pu_attr[tag] = self.get_element(tag, node)

class Stage:
    L = list()

    def __init__(self, file):
        self.data = xml.dom.minidom.parse(file)

    def __cmp__(self, other):
        return cmp(self.cc, other.cc)

    def getNextX(self):
        if len(self.L) > 0:
            item = self.L[len(self.L) - 1]
            return item.cc
        else:
            return -1

    def include(self, item):
        self.L.append(item)

    def pop(self, position):
        subList = list()
        nextx = int(self.getNextX())
        while nextx == position:
            subList.append(self.L.pop())
            nextx = int(self.getNextX())
        return subList

    def buildStage(self):
        for node in self.data.getElementsByTagName("item"):
            type = node.getElementsByTagName("type")[0].childNodes[0].nodeValue
            if type == "background":
                item = Backg(node)
            elif type == "enemy":
                item = Enemy(node)
            elif type == "sw_mult":
                item = Mult(node)
            elif type == "sw_frag":
                item = Frag(node)
            elif type in ["sw_guided", "sw_elet"]:
                item = Sw(node)
            elif type == "first_aid_kit":
                item = FirstAidKit(node)
            self.include(item)
        #below is some black magic I'm not sure how to deal with... but works
        #taken from stackoverflow.org
        self.L.sort(key=lambda item: int(item.cc), reverse=True)
