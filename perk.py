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

from xmlutils import *
import uuid
import lxml.etree as ET

class PerkCateg(object):

    def __init__(self):
        self.id     = uuid.uuid1().hex
        self.name   = None

    @staticmethod
    def build_from_xml(elem):
        f = PerkCateg()
        f.id   = elem.attrib['id']
        f.name = elem.text
        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()

class PerkException(object):

    def __init__(self):
        self.tag   = None
        self.value = None

    @staticmethod
    def build_from_xml(elem):
        f = PerkException()
        f.tag   = elem.attrib['tag']
        f.value = int(elem.attrib['value'])
        return f

    def write_into(self, elem):
        ec = ET.SubElement(elem, "Exception",
            {
              'tag'   : self.tag,
              'value' : str(self.value),
            })

class PerkRank(object):

    def __init__(self):
        self.id         = None
        self.value      = None
        self.exceptions = []

    @staticmethod
    def build_from_xml(elem):
        f = PerkRank()
        f.id    = int(elem.attrib['id'])
        f.value = int(elem.attrib['value'])
        f.exceptions = []
        for se in elem.iter():
            if se.tag == 'Exception':
                f.exceptions.append(PerkException.build_from_xml(se))

        return f

    def write_into(self, elem):
        ec = ET.SubElement(elem, "Rank",
            {
              'id'    : str(self.id),
              'value' : str(self.value),
            })

        for e in self.exceptions:
            e.write_into( ec )

class Perk(object):

    def __init__(self):
        self.id    = uuid.uuid1().hex
        self.name  = None
        self.type  = None
        self.rule  = None
        self.desc  = None
        self.ranks = []

    @staticmethod
    def build_from_xml(elem):
        f = Perk()
        f.name  = elem.attrib['name']
        f.id    = elem.attrib['id']
        f.type  = elem.attrib['type']
        f.rule  = elem.attrib['rule'] if ('rule' in elem.attrib) else f.id
        f.desc  = read_sub_element_text(elem, 'Description', "")
        f.ranks = []
        for se in elem.iter():
            if se.tag == 'Rank':
                f.ranks.append(PerkRank.build_from_xml(se))
        return f

    def write_into(self, name, elem):
        ec = ET.SubElement(elem, name,
            { 'name'  : self.name,
              'id'    : self.id,
              'type'  : self.type,
              'rule'  : self.rule
            })

        for r in self.ranks:
            r.write_into( ec )

        ET.SubElement(ec, 'Description').text = self.desc

    def get_rank_value(self, rank):
        for r in self.ranks:
            if r.id == rank: return r.value
        return None

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