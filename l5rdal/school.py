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

import uuid
from .xmlutils import *
from .packitem import PackItem
from .requirements import read_requirements_list

class SchoolSkill(PackItem):

    def __init__(self):
        super(SchoolSkill, self).__init__()
        self.id     = uuid.uuid1().hex
        self.rank   = None
        self.emph   = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolSkill()
        f.id   = read_attribute    ( elem, 'id'       )
        f.rank = read_attribute_int( elem, 'rank'     )
        f.emph = read_attribute    ( elem, 'emphases' )
        return f

    def write_into(self, elem):
        pass

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()


class SchoolSkillWildcard(PackItem):

    def __init__(self):
        super(SchoolSkillWildcard, self).__init__()
        self.value    = None
        self.modifier = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolSkillWildcard()
        f.value    = elem.text
        f.modifier = read_attribute( elem, 'modifier', 'or' )
        return f

    def write_into(self, elem):
        pass


class SchoolSkillWildcardSet(PackItem):

    def __init__(self):
        super(SchoolSkillWildcardSet, self).__init__()
        self.rank      = None
        self.wildcards = []

    @staticmethod
    def build_from_xml(elem):
        f = SchoolSkillWildcardSet()
        f.rank = read_attribute_int( elem, 'rank' )
        f.wildcards = []
        for se in elem.iter():
            if se.tag == 'Wildcard':
                f.wildcards.append(SchoolSkillWildcard.build_from_xml(se))
        return f

    def write_into(self, elem):
        pass


class SchoolTech(PackItem):

    def __init__(self):
        super(SchoolTech, self).__init__()
        self.id     = uuid.uuid1().hex
        self.name   = None
        self.rank   = None
        self.desc   = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolTech()
        f.id   = read_attribute       ( elem, 'id'       )
        f.name = read_attribute       ( elem, 'name', '' )
        f.rank = read_attribute_int   ( elem, 'rank'     )
        f.desc = read_sub_element_text(elem, 'Description', "").strip()

        # HACK. remove eol to allow exporters to be in charge of the text wrapping
        f.desc = f.desc.replace('\n', '')

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


class SchoolSpell(PackItem):

    def __init__(self):
        super(SchoolSpell, self).__init__()
        self.id     = uuid.uuid1().hex

    @staticmethod
    def build_from_xml(elem):
        f = SchoolSpell()
        f.id = read_attribute( elem, 'id' )
        return f

    def write_into(self, elem):
        pass

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return self.id.__hash__()


class SchoolSpellWildcard(PackItem):

    def __init__(self):
        super(SchoolSpellWildcard, self).__init__()
        self.count   = None
        self.element = None
        self.tag     = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolSpellWildcard()
        f.count   = read_attribute_int( elem, 'count'   )
        f.element = read_attribute    ( elem, 'element' )
        f.tag     = read_attribute    ( elem, 'tag'     )
        return f

    def write_into(self, elem):
        pass


class SchoolKiho(PackItem):

    def __init__(self):
        super(SchoolKiho, self).__init__()
        self.count = None
        self.text  = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolKiho()
        f.count   = read_attribute_int( elem, 'count' )
        f.text    = elem.text
        return f

    def write_into(self, elem):
        pass


class SchoolTattoo(PackItem):

    def __init__(self):
        super(SchoolTattoo, self).__init__()
        self.count   = None
        self.allowed = None
        self.text    = None

    @staticmethod
    def build_from_xml(elem):
        f = SchoolTattoo()
        f.count   = read_attribute_int ( elem, 'count'   )
        f.allowed = read_attribute_bool( elem, 'allowed' )
        f.text    = elem.text
        return f

    def write_into(self, elem):
        pass


class SchoolPerk(PackItem):

    def __init__(self):
        super(SchoolPerk, self).__init__()
        self.id = None
        self.rank = 0

    @staticmethod
    def build_from_xml(elem):
        f = SchoolPerk()
        f.rank = read_attribute_int (elem, 'rank')
        f.id = read_attribute(elem, 'id')
        return f

    def write_into(self, elem):
        pass


class School(PackItem):

    def __init__(self):
        super(School, self).__init__()
        self.id     = uuid.uuid1().hex
        self.name   = None
        self.clanid = None
        self.trait  = None

        self.affinity    = None
        self.deficiency  = None
        self.honor       = None
        self.kihos       = None
        self.tattoos     = None

        self.tags       = []
        self.skills     = []
        self.skills_pc  = []
        self.techs      = []
        self.spells     = []
        self.spells_pc  = []
        self.outfit     = []
        self.money      = [0]*3 # koku, bu, zeni
        self.require    = []
        self.perks      = []

    @staticmethod
    def build_from_xml(elem):
        f = School()
        f.id     = read_attribute( elem, 'id'     )
        f.name   = read_attribute( elem, 'name'   )
        f.clanid = read_attribute( elem, 'clanid' )

        f.trait  = read_sub_element_text( elem, 'Trait' )

        f.tags  = []
        for se in elem.find('Tags').iter():
            if se.tag == 'Tag':
                f.tags.append(se.text)

        f.affinity    = read_sub_element_text( elem, 'Affinity'   )
        f.deficiency  = read_sub_element_text( elem, 'Deficiency' )
        f.honor       = float( read_sub_element_text( elem, 'Honor', "0.0" ) )

        # school skills
        f.skills     = []
        f.skills_pc  = []
        for se in elem.find('Skills').iter():
            if se.tag == 'Skill':
                f.skills.append(SchoolSkill.build_from_xml(se))
            elif se.tag == 'PlayerChoose':
                f.skills_pc.append(SchoolSkillWildcardSet.build_from_xml(se))

        # school techs
        f.techs = []
        for se in elem.find('Techs').iter():
            if se.tag == 'Tech':
                f.techs.append(SchoolTech.build_from_xml(se))

        # school spells
        f.spells    = []
        f.spells_pc = []
        for se in elem.find('Spells').iter():
            if se.tag == 'PlayerChoose':
                f.spells_pc.append(SchoolSpellWildcard.build_from_xml(se))
            elif se.tag == 'Spell':
                f.spells.append(SchoolSpell.build_from_xml(se))

        f.outfit    = [ ]
        f.money     = [0]*3 # koku, bu, zeni
        outfit_elem = elem.find('Outfit')
        if outfit_elem:
            for se in outfit_elem.iter():
                if se.tag == 'Item':
                    f.outfit.append(se.text)
            f.money[0] = read_attribute_int(outfit_elem, 'koku')
            f.money[1] = read_attribute_int(outfit_elem, 'bu')
            f.money[2] = read_attribute_int(outfit_elem, 'zeni')
        #elif 'advanced' not in f.tags and 'alternate' not in f.tags:
        #    print('missing outfit: {school_id}'.format(school_id=f.id))

        f.require = read_requirements_list(elem)

        # kihos and tattoos
        f.kihos   = None
        f.tattoos = None
        if elem.find('Kihos') is not None:
            f.kihos = SchoolKiho.build_from_xml( elem.find('Kihos') )
        if elem.find('Tattoos') is not None:
            f.tattoos = SchoolTattoo.build_from_xml( elem.find('Tattoos') )

        # starting Merit and Flaws
        f.perks = []
        if elem.find('Perks') is not None:
            for se in elem.find('Perks').iter():
                if se.tag == 'Perk':
                    f.perks.append(SchoolPerk.build_from_xml(se))

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


