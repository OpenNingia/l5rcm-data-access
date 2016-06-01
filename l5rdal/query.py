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

def get_clan(storage, iid):
    try:
        return [x for x in storage.clans if x.id == iid][0]
    except:
        return None

def get_family(storage, iid):
    try:
        return [x for x in storage.families if x.id == iid][0]
    except:
        return None

def get_school(storage, iid):
    try:
        return [x for x in storage.schools if x.id == iid][0]
    except:
        return None

def get_base_schools(storage):
    def is_base_school(school):
        return (len(school.require) == 0 and
                'advanced' not in school.tags and
                'alternate' not in school.tags)
    try:
        return [x for x in storage.schools if is_base_school(x)]
    except:
        return None

def get_school_tech(school_obj, rank):
    try:
        return [x for x in school_obj.techs if x.rank == rank][0]
    except:
        return None

def get_tech(storage, iid):
    for sc in storage.schools:
        techs = [x for x in sc.techs if x.id == iid]
        if len(techs): return sc, techs[0]
    return None, None

def get_skill(storage, iid):
    try:
        return [x for x in storage.skills if x.id == iid][0]
    except:
        return None

def get_skills(storage, categ):
    return [x for x in storage.skills if x.type == categ]

def get_spells(storage, ring, mastery):
    return [x for x in storage.spells if x.element == ring and x.mastery == mastery]

def get_maho_spells(storage, ring, mastery):
    return [x for x in storage.spells if x.element == ring and x.mastery == mastery and 'maho' in x.tags]

def get_mastery_ability_rule(storage, iid, value):
    try:
        skill = get_skill(storage, iid)
        return [x for x in skill.mastery_abilities if x.rank == value][0].rule
    except:
        return None

def get_kata(storage, iid):
    try:
        return [x for x in storage.katas if x.id == iid][0]
    except:
        return None

def get_kiho(storage, iid):
    try:
        return [x for x in storage.kihos if x.id == iid][0]
    except:
        print(id)
        return None

def get_spell(storage, iid):
    try:
        return [x for x in storage.spells if x.id == iid][0]
    except:
        return None

def get_merit(storage, iid):
    try:
        return [x for x in storage.merits if x.id == iid][0]
    except:
        return None

def get_flaw(storage, iid):
    try:
        return [x for x in storage.flaws if x.id == iid][0]
    except:
        return None

def get_weapon(storage, name):
    try:
        return [x for x in storage.weapons if x.name == name][0]
    except:
        return None

def get_armor(storage, name):
    try:
        return [x for x in storage.armors if x.name == name][0]
    except:
        return None

def get_weapon_effect(storage, iid):
    try:
        return [x for x in storage.weapon_effects if x.id == iid][0]
    except:
        return None

def get_ring(storage, iid):
    try:
        return [x for x in storage.rings if x.id == iid][0]
    except:
        return None

def get_trait(storage, iid):
    try:
        return [x for x in storage.traits if x.id == iid][0]
    except:
        return None