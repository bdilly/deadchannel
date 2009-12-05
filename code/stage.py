#!/usr/bin/env python
# -*- coding: utf-8 (i think) -*-

#----------------------------------------------------------------------
# Author:
#   João Corrêa <joao@livewire.com.br>
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
        self.type = node.getElementsByTagName("type")[0].childNodes[0].nodeValue
        self.cc = int(node.getElementsByTagName("cc")[0].childNodes[0].nodeValue)

class Backg(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        self.image = node.getElementsByTagName("image")[0].childNodes[0].nodeValue
        self.layer = node.getElementsByTagName("layer")[0].childNodes[0].nodeValue

class Enemy(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        self.pos_x = node.getElementsByTagName("pos_x")[0].childNodes[0].nodeValue
        self.pos_y = node.getElementsByTagName("pos_y")[0].childNodes[0].nodeValue
        self.behaviour = node.getElementsByTagName("behaviour")[0].childNodes[0].nodeValue
        self.life = node.getElementsByTagName("life")[0].childNodes[0].nodeValue
        self.image = node.getElementsByTagName("image")[0].childNodes[0].nodeValue
        self.speed = node.getElementsByTagName("speed")[0].childNodes[0].nodeValue

class Sw(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        self.pos_x = node.getElementsByTagName("pos_x")[0].childNodes[0].nodeValue
        self.pos_y = node.getElementsByTagName("pos_y")[0].childNodes[0].nodeValue
        self.speed_x = node.getElementsByTagName("speed_y")[0].childNodes[0].nodeValue
        self.speed_y = node.getElementsByTagName("speed_x")[0].childNodes[0].nodeValue
        self.name = node.getElementsByTagName("name")[0].childNodes[0].nodeValue
        self.ammo = node.getElementsByTagName("ammo")[0].childNodes[0].nodeValue
        self.max_ammo = node.getElementsByTagName("max_ammo")[0].childNodes[0].nodeValue
        self.cooldown = node.getElementsByTagName("cooldown")[0].childNodes[0].nodeValue
        self.heating = node.getElementsByTagName("heating")[0].childNodes[0].nodeValue
        self.time = node.getElementsByTagName("time")[0].childNodes[0].nodeValue

class Mult(Sw):
    def __init__(self, node):
        Sw.__init__(self, node)
        self.special1 = node.getElementsByTagName("special1")[0].childNodes[0].nodeValue
        self.special2 = node.getElementsByTagName("special2")[0].childNodes[0].nodeValue

class Frag(Sw):
    def __init__(self, node):
        Sw.__init__(self, node)
        self.special1 = node.getElementsByTagName("special1")[0].childNodes[0].nodeValue
        self.max_charge = node.getElementsByTagName("max_charge")[0].childNodes[0].nodeValue 

class Guided(Sw):
    def __init__(self, node):
        Sw.__init__(self, node)
        self.special1 = node.getElementsByTagName("special1")[0].childNodes[0].nodeValue
        self.special2 = node.getElementsByTagName("special2")[0].childNodes[0].nodeValue

class FirstAidKit(Item):
    def __init__(self, node):
        Item.__init__(self, node)
        self.pos_x = node.getElementsByTagName("pos_x")[0].childNodes[0].nodeValue
        self.pos_y = node.getElementsByTagName("pos_y")[0].childNodes[0].nodeValue
        self.speed_x = node.getElementsByTagName("speed_x")[0].childNodes[0].nodeValue
        self.speed_y = node.getElementsByTagName("speed_y")[0].childNodes[0].nodeValue
        self.life = node.getElementsByTagName("life")[0].childNodes[0].nodeValue
        self.time = node.getElementsByTagName("time")[0].childNodes[0].nodeValue

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
            nextx = self.getNextX()
            print(len(subList))
            print(len(self.L))
            print(position)
            print(nextx)
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
            elif type == "sw_guided":
                item = Guided(node)
            elif type == "first_aid_kit":
                item = FirstAidKit(node)
            elif type == "sw_mult":
                item = Mult(node)

            print(item.cc)
            self.include(item)
        #below is some black magic I'm not sure how to deal with... but works
        #taken from stackoverflow.org
        self.L.sort(key=lambda item: item.cc, reverse=True)
