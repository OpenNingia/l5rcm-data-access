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

# Declarative stat-modifier records (schema v1).
#
# This module is intentionally *dumb*: it parses the XML faithfully and keeps
# every computed value as a raw expression string. Sandboxed evaluation of
# those expressions (the value DSL and the `requires` predicates) lives in the
# application layer, not here. See MODIFIERS_SCHEMA.md in the datapack repo for
# the authoritative schema.

from .packitem import PackItem
from .xmlutils import *


class Mod(object):
    """A single additive / overriding `<Mod>` entry."""

    def __init__(self):
        self.affects = None     # target statistic (e.g. 'armor_tn', 'attack_roll')
        self.value = None       # expression, for scalar affects
        self.roll = None        # expression, for roll affects (r component)
        self.keep = None        # expression, for roll affects (k component)
        self.bonus = None       # expression, for roll affects (flat bonus)
        self.op = 'add'         # add | set | min | max
        self.detail = None      # qualified selector: 'skill:', 'weapon:', 'trait:', 'ring:', 'tag:'
        self.requires = None    # auto-evaluable predicate (gear/state), None = always
        self.when = 'auto'      # situational combat flag, 'auto' = no manual toggle
        self.default = None     # 'on' / 'off' (None = inferred from when/requires)
        self.reason = None      # display label (None = source record name)

    @staticmethod
    def build_from_xml(elem):
        m = Mod()
        m.affects = read_attribute(elem, 'affects')
        m.value = read_attribute(elem, 'value')
        m.roll = read_attribute(elem, 'roll')
        m.keep = read_attribute(elem, 'keep')
        m.bonus = read_attribute(elem, 'bonus')
        m.op = read_attribute(elem, 'op', 'add')
        m.detail = read_attribute(elem, 'detail')
        m.requires = read_attribute(elem, 'requires')
        m.when = read_attribute(elem, 'when', 'auto')
        m.default = read_attribute(elem, 'default')
        m.reason = read_attribute(elem, 'reason')
        return m

    @property
    def is_roll(self):
        """True when this Mod carries a roll/keep/bonus triple."""
        return any(x is not None for x in (self.roll, self.keep, self.bonus))

    def __str__(self):
        return "Mod(affects={0}, op={1})".format(self.affects, self.op)


class OneOf(object):
    """A `<OneOf>` group: the player picks exactly one of `options`."""

    def __init__(self):
        self.options = []   # list[Mod]

    @staticmethod
    def build_from_xml(elem):
        g = OneOf()
        for se in elem:
            if se.tag == 'Mod':
                g.options.append(Mod.build_from_xml(se))
        return g

    def __str__(self):
        return "OneOf({0} options)".format(len(self.options))


class Param(object):
    """A `<Param>`: a player-chosen magnitude (0..max) referenced by name in
    sibling Mod expressions."""

    def __init__(self):
        self.name = None
        self.max = None     # expression

    @staticmethod
    def build_from_xml(elem):
        p = Param()
        p.name = read_attribute(elem, 'name')
        p.max = read_attribute(elem, 'max')
        return p

    def __str__(self):
        return "Param({0})".format(self.name)


class Substitution(object):
    """A `<Substitute>`: use trait/ring `use` instead of `instead_of` in the
    calculation of `affects`."""

    def __init__(self):
        self.affects = None
        self.use = None
        self.instead_of = None
        self.requires = None
        self.when = 'auto'

    @staticmethod
    def build_from_xml(elem):
        s = Substitution()
        s.affects = read_attribute(elem, 'affects')
        s.use = read_attribute(elem, 'use')
        s.instead_of = read_attribute(elem, 'instead_of')
        s.requires = read_attribute(elem, 'requires')
        s.when = read_attribute(elem, 'when', 'auto')
        return s

    def __str__(self):
        return "Substitution({0}: {1}<-{2})".format(
            self.affects, self.use, self.instead_of)


class ModifierDef(PackItem):
    """A set of stat modifiers attached to a source record by id.

    Several ModifierDef may share a `target`; their effects stack. Identity is
    deliberately left object-based (no __eq__/__hash__) so the loader appends
    every definition rather than overwriting on duplicate target.
    """

    def __init__(self):
        super(ModifierDef, self).__init__()

        self.target = None      # slug of the source record
        self.kind = None        # tech | kata | kiho | tattoo | merit | flaw |
                                # ancestor | path | mastery | weapon_effect | armor
        self.rank = None        # int, only meaningful for kind == 'mastery'
        self.partial = False    # honesty flag: record has unmodeled stat clauses

        self.params = []        # list[Param]
        self.mods = []          # list[Mod]  (top-level)
        self.groups = []        # list[OneOf]
        self.substitutions = [] # list[Substitution]

    @staticmethod
    def build_from_xml(elem):
        d = ModifierDef()
        d.target = read_attribute(elem, 'target')
        d.kind = read_attribute(elem, 'kind')
        rank = read_attribute(elem, 'rank')
        d.rank = int(rank) if rank is not None else None
        partial = read_attribute(elem, 'partial', '')
        d.partial = partial.strip().lower() in ('true', '1', 'yes')

        for se in elem:
            if se.tag == 'Param':
                d.params.append(Param.build_from_xml(se))
            elif se.tag == 'Mod':
                d.mods.append(Mod.build_from_xml(se))
            elif se.tag == 'OneOf':
                d.groups.append(OneOf.build_from_xml(se))
            elif se.tag == 'Substitute':
                d.substitutions.append(Substitution.build_from_xml(se))

        return d

    def write_into(self, elem):
        pass

    def __str__(self):
        return "ModifierDef(target={0}, kind={1})".format(self.target, self.kind)
