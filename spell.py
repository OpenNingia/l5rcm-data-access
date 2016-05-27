# -*- coding: iso-8859-1 -*-
# Copyright (C) 2014 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from requirements import read_requirements_list
from xmlutils import *
import uuid
from packitem import PackItem


class Spell(PackItem):

    def __init__(self):
        super(Spell, self).__init__()
        self.id    = uuid.uuid1().hex

        self.name     = None
        self.area     = None
        self.mastery  = None
        self.range    = None
        self.duration = None
        self.element  = None
        self.tags     = None
        self.require  = None
        self.desc     = None
        self.elements = []
        self.raises   = []

    @staticmethod
    def build_from_xml(elem):
        f = Spell()
        f.id       = elem.attrib['id']
        f.name     = read_attribute(elem, 'name')
        f.area     = read_attribute(elem, 'area')
        f.mastery  = read_attribute_int(elem, 'mastery')
        f.range    = read_attribute(elem, 'range')
        f.duration = read_attribute(elem, 'duration')
        f.element  = read_attribute(elem, 'element')
        f.tags     = read_spell_tag_list(elem)
        f.require  = read_requirements_list(elem)
        f.desc     = read_sub_element_text(elem, 'Description', "").strip()
        f.elements = []
        f.raises   = []

        if elem.find('Raises') is not None:
            for se in elem.find('Raises').iter():
                if se.tag == 'Raise':
                    f.raises.append(se.text)

        # support for Multi-Element spells
        if elem.find('MultiElement') is not None:
            for se in elem.find('MultiElement').iter():
                if se.tag == 'Element':
                    f.elements.append(se.text)
        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name or self.id

    def __unicode__(self):
        return self.name or self.id

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()

