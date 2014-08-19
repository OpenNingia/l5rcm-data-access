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

from requirements import Requirement, RequirementOption, read_requirements_list
from xmlutils import *
import uuid
import lxml.etree as ET

class Kiho(object):

    def __init__(self):
        self.id     = uuid.uuid1().hex
        self.name    = None
        self.element = None
        self.type    = None
        self.mastery = None
        self.desc    = None
        self.require = None
        self.tags    = None

    @staticmethod
    def build_from_xml(elem):
        f = Kiho()
        f.id      = elem.attrib['id']
        f.name    = read_attribute(elem, 'name')
        f.element = read_attribute(elem, 'element')
        f.type    = read_attribute(elem, 'type')
        f.mastery = read_attribute_int(elem, 'mastery')
        f.desc    = read_sub_element_text(elem, 'Description', "")
        f.require = read_requirements_list(elem)
        f.tags    = read_tag_list(elem)

        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name or self.id

    def __unicode__(self):
        return self.name

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()

class Kata(object):

    def __init__(self):
        self.id     = uuid.uuid1().hex
        self.name    = None
        self.element = None
        self.mastery = None
        self.desc    = None
        self.require = None
        self.tags    = None

    @staticmethod
    def build_from_xml(elem):
        f = Kata()
        f.id      = elem.attrib['id']
        f.name    = read_attribute(elem, 'name')
        f.element = read_attribute(elem, 'element')
        f.mastery = read_attribute_int(elem, 'mastery')
        f.desc    = read_sub_element_text(elem, 'Description', "")
        f.require = read_requirements_list(elem)
        f.tags  = read_tag_list(elem)
        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name or self.id

    def __unicode__(self):
        return self.name

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()

