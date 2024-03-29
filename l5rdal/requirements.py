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

from .xmlutils import *
from .packitem import PackItem
import logging


class RINGS:
    EARTH = 0
    AIR = 1
    WATER = 2
    FIRE = 3
    VOID = 4

    _names = dict(earth=0, air=1, water=2, fire=3, void=4)
    _ids = ['earth', 'air', 'water', 'fire', 'void']


def ring_from_name(name):
    if name in RINGS._names:
        return RINGS._names[name]
    return -1


def ring_name_from_id(ring_id):
    if 0 <= ring_id < len(RINGS._ids):
        return RINGS._ids[ring_id]


class ATTRIBS:
    # earth ring
    STAMINA = 0
    WILLPOWER = 1

    # air ring
    REFLEXES = 2
    AWARENESS = 3

    # water ring
    STRENGTH = 4
    PERCEPTION = 5

    # fire ring
    AGILITY = 6
    INTELLIGENCE = 7

    _names = dict(stamina=0, willpower=1, reflexes=2, awareness=3,
                  strength=4, perception=5, agility=6, intelligence=7)
    _ids = ['stamina', 'willpower', 'reflexes', 'awareness', 'strength',
            'perception', 'agility', 'intelligence']


def attrib_from_name(name):
    if name in ATTRIBS._names:
        return ATTRIBS._names[name]
    return -1


def attrib_name_from_id(attrib_id):
    if 0 <= attrib_id < len(ATTRIBS._ids):
        return ATTRIBS._ids[attrib_id]
    else:
        print("unknown trait_id: {0}".format(attrib_id))
        return None

class Requirement(PackItem):

    def __init__(self):
        super(Requirement, self).__init__()

        self.field = None
        self.type  = None
        self.min   = None
        self.max   = None
        self.trg   = None
        self.text  = None

    @staticmethod
    def build_from_xml(elem):
        f = Requirement()
        f.field = read_attribute    ( elem, 'field'   )
        f.type  = read_attribute    ( elem, 'type'    )
        f.min   = read_attribute_int( elem, 'min', -1 )
        f.max   = read_attribute_int( elem, 'max', 999)
        f.trg   = read_attribute    ( elem, 'trg'     )
        f.text = elem.text
        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text

    def in_range(self, value):
        return self.min <= value <= self.max

    def match(self, pc, dstore):

        if self.field:
            if self.field.startswith('*'):
                return self.match_wildcard(pc, dstore)
            if self.field == 'honor':
                return self.in_range(pc.get_honor())
            if self.field == 'status':
                return self.in_range(pc.get_status())
            if self.field == 'glory':
                return self.in_range(pc.get_glory())

        if self.type == 'ring':
            return self.in_range(pc.get_ring_rank(self.field))
        if self.type == 'trait':
            return self.in_range(pc.get_trait_rank(self.field))
        if self.type == 'skill':
            skill_id = self.field
            if not skill_id: return True
            if self.trg and self.trg not in pc.get_skill_emphases(skill_id):
                return False  # missing emphases
            if (skill_id not in pc.get_skills() or
                    not self.in_range(pc.get_skill_rank(skill_id))):
                return False
            pc.set_skill_rank(skill_id, 0)
            return True
        if self.type == 'tag':
            return pc.has_tag(self.field)
        if self.type == 'rule':
            return pc.has_rule(self.field)
        if self.type == 'school':
            return self.has_school(pc, self.field)
        if self.type == 'rank':
            return self.in_range(pc.get_insight_rank())
        return True

    def has_school(self, pc, school_id):

        log = logging.getLogger('data')

        school_rank_ = pc.get_school_rank(school_id)
        log.debug(u"check school requirement. id: %s, min rank: %d, max rank: %d. character value: %d",
                      school_id, self.min, self.max, school_rank_)
        return self.in_range(school_rank_)

    def match_wc_ring(self, pc, dstore):
        r = False
        if self.field == '*any': # any ring
            for i in range(0, 5):
                ring_id = ring_name_from_id(i)
                if self.in_range( pc.get_ring_rank(ring_id) ):
                    pc.set_ring_rank(ring_id, 0)
                    r = True
                    break
        return r

    def match_wc_trait(self, pc, dstore):
        r = False
        if self.field == '*any': # any trait
            for i in range(0, 8):
                trait_id = attrib_name_from_id(i)
                if self.in_range( pc.get_trait_rank(trait_id) ):
                    pc.set_trait_rank(trait_id, 0)
                    r = True
                    break
        return r

    def match_wc_skill(self, pc, dstore):
        r = False
        if self.field == '*any': # any skills
            for k in pc.get_skills():
                if self.in_range( pc.get_skill_rank(k) ):
                    r = True
                    pc.set_skill_rank(k, 0)
        else:
            import l5rdal as dal
            import l5rdal.query

            tag = self.field[1:]
            for k in pc.get_skills():
                sk = dal.query.get_skill(dstore, k)
                if tag not in sk.tags:
                    continue
                if self.in_range( pc.get_skill_rank(k) ):
                    r = True
                    pc.set_skill_rank(k, 0)
                    break
        return r

    def match_wc_school(self, pc, dstore):

        print('need a school {} of rank in range {}-{}'.format(self.field, self.min, self.max))

        r = False
        if self.field == '*any': # any school
            for k in pc.get_schools():
                if self.in_range( pc.get_school_rank(k) ):
                    r = True
                    pc.set_school_rank(k, 0)
        else:
            import l5rdal as dal
            import l5rdal.query

            tag = self.field[1:]
            for k in pc.get_schools():
                sk = dal.query.get_school(dstore, k)
                if not sk:
                    print('school not found', k)
                    continue
                if tag not in sk.tags:
                    print(tag, 'not in', sk.tags)
                    continue
                if self.in_range( pc.get_school_rank(k) ):
                    r = True
                    #pc.set_school_rank(k, 0)
                    break
        return r

    def match_wildcard(self, model, dstore):
        got_req = -1
        if self.type == 'ring':
            return self.match_wc_ring(model, dstore)
        if self.type == 'trait':
            return self.match_wc_trait(model, dstore)
        if self.type == 'skill':
            return self.match_wc_skill(model, dstore)
        if self.type == 'school':
            return self.match_wc_school(model, dstore)
        return True


class RequirementOption(PackItem):

    def __init__(self):
        super(RequirementOption, self).__init__()
        self.require = []
        self.type    = None
        self.text    = None

    @staticmethod
    def build_from_xml(elem):
        f = RequirementOption()
        f.require = []
        f.type    = 'option'
        f.text = elem.attrib['text'] if ('text' in elem.attrib) else ''
        for se in elem.iter():
            if se.tag == 'Requirement':
                f.require.append(Requirement.build_from_xml(se))
        return f

    def write_into(self, elem):
        pass

    def match(self, model, dstore):
        # at least one should match
        for r in self.require:
            if r.match(model, dstore):
                return True
        return False

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text

def read_requirements_list(xml_element):
    # requirements
    require = []
    el      = xml_element.find('Requirements')
    if el:
        for se in el:
            if se.tag == 'Requirement':
                require.append(Requirement.build_from_xml(se))
            if se.tag == 'RequirementOption':
                require.append(RequirementOption.build_from_xml(se))

    return require
