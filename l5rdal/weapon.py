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
from .packitem import PackItem


class WeaponEffect(PackItem):

    def __init__(self):
        super(WeaponEffect, self).__init__()
        self.id    = uuid.uuid1().hex
        self.text  = None

    @staticmethod
    def build_from_xml(elem):
        f = WeaponEffect()
        f.id   = elem.attrib['id']
        f.text = elem.text
        return f

    def write_into(self, elem):
        pass

    # Identity by id so Data.append_to() overrides an existing effect
    # instead of appending a duplicate when a pack is revisited (mirrors
    # Skill/SkillCateg). Without this the load is not idempotent.
    def __eq__(self, obj):
        return obj is not None and getattr(obj, 'id', None) == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(self.id)


class Armor(PackItem):

    def __init__(self):
        super(Armor, self).__init__()
        self.name     = None
        self.tn       = None
        self.rd       = None
        self.cost     = None
        self.effectid = None

    @staticmethod
    def build_from_xml(elem):
        f = Armor()
        f.name   = elem.attrib['name']
        f.tn     = int(elem.attrib['tn'])
        f.rd     = int(elem.attrib['rd'])
        f.cost   = elem.attrib['cost']

        f.effectid = None
        eff = elem.find('Effect')
        if eff is not None: f.effectid = eff.attrib['id']
        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # Identity by name (the key get_armor() resolves by) so the load is
    # idempotent: revisiting a pack overrides the armor rather than
    # appending a duplicate. Mirrors Skill/SkillCateg.
    def __eq__(self, obj):
        return obj is not None and getattr(obj, 'name', None) == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(self.name)


class Weapon(PackItem):

    def __init__(self):
        super(Weapon, self).__init__()
        self.name         = None
        self.skill        = None
        self.cost         = None
        self.dr           = None
        self.dr2          = None
        self.range        = None
        self.strength     = None
        self.min_strength = None
        self.effectid     = None

        self.tags  = []

    @staticmethod
    def build_from_xml(elem):
        f = Weapon()
        f.name     = elem.attrib['name']
        f.skill    = elem.attrib['skill'] if ( 'skill' in elem.attrib ) else None
        f.cost     = elem.attrib['cost'] if ( 'cost' in elem.attrib ) else None
        f.dr       = elem.attrib['dr'] if ( 'dr' in elem.attrib ) else None
        f.dr2      = elem.attrib['dr_alt'] if ( 'dr_alt' in elem.attrib ) else None
        f.range    = elem.attrib['range'] if ( 'range' in elem.attrib ) else None
        f.strength = int(elem.attrib['strength']) if ( 'strength' in elem.attrib ) else None
        f.min_strength = int(elem.attrib['min_strength']) if ( 'min_strength' in elem.attrib ) else None

        f.tags  = []
        for se in elem.find('Tags').iter():
            if se.tag == 'Tag':
                f.tags.append(se.text)

        f.effectid = None
        eff = elem.find('Effect')
        if eff: f.effectid = eff.attrib['id']

        return f

    def write_into(self, elem):
        pass

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # Identity by name (the key get_weapon() resolves by) so the load is
    # idempotent: revisiting a pack overrides the weapon rather than
    # appending a duplicate. This was the cause of weapons listing twice
    # (Katana, Kusarigama, every arrow…) -- Weapon, alone among the
    # catalogue item types, lacked the __eq__ that append_to() relies on.
    def __eq__(self, obj):
        return obj is not None and getattr(obj, 'name', None) == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(self.name)