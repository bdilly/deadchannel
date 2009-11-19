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
    def __init__(self, x, y, speed_x, speed_y, rot, rotspeed, life, image,
                 type, behaviour, special):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rot = rot
        self.rotspeed = rotspeed
        self.life = life
        self.image = image
        self.type = type
        self.behaviour = behaviour
        self.special = special

class Stage:

    L = list()

    def __init__(self, file):
        self.data = xml.dom.minidom.parse(file)

    def __cmp__(self, other):
        return cmp(self.x, other.x)

    def getNextX(self):
        if len(self.L) > 0:
            item = self.L[len(self.L) - 1]
            return item.x
        else:
            return -1

    def include(self, item):
        self.L.append(item)

    def pop(self, position):
        subList = list()
        nextx = self.getNextX()
        while nextx == position:
            subList.append(self.L.pop())
            nextx = self.getNextX()   
        return subList

    def buildStage(self):
        for nodes in self.data.getElementsByTagName("item"):
            itemType = nodes.getElementsByTagName("type")[0].childNodes[0].nodeValue
            x = int(nodes.getElementsByTagName("x")[0].childNodes[0].nodeValue)
            image = nodes.getElementsByTagName("image")[0].childNodes[0].nodeValue

            if itemType == "background":
                item = Item(x, "", "", "", "", "", "", image, itemType, "", "")

            else:

                life = int(nodes.getElementsByTagName("life")[0].childNodes[0].nodeValue)
                y = int(nodes.getElementsByTagName("y")[0].childNodes[0].nodeValue)
                speed_x = int(nodes.getElementsByTagName("speed_x")[0].childNodes[0].nodeValue)
                speed_y = int(nodes.getElementsByTagName("speed_y")[0].childNodes[0].nodeValue)
                rot = int(nodes.getElementsByTagName("rot")[0].childNodes[0].nodeValue)
                rotspeed = int(nodes.getElementsByTagName("rotspeed")[0].childNodes[0].nodeValue)
                life = int(nodes.getElementsByTagName("life")[0].childNodes[0].nodeValue)
                behaviour = nodes.getElementsByTagName("behaviour")[0].childNodes[0].nodeValue
                special = nodes.getElementsByTagName("special")[0].childNodes[0].nodeValue
                item = Item(x, y, speed_x, speed_y, rot, rotspeed, life, image, itemType, behaviour, special)
            self.include(item)
        #below is some black magic I'm not sure how to deal with... but works
        #taken from stackoverflow.org
        self.L.sort(key=lambda item: item.x, reverse=True)
