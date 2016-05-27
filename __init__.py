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

from clan import *
from family import *
from school import *
from skill import *
from spell import *
from perk import *
from powers import *
from weapon import *
from generic import *
from requirements import *

import os
import json
import xml.etree.ElementTree
import xml.etree.cElementTree as ET


class DataPackLoadingError(Exception):
    def __init__(self, file_path, err_str):
        self.error_str = err_str
        self.file_path = file_path

    def __str__(self):
        return "file: {file}, error: {error}".format(
            file=self.file_path, error=self.error_str)

class DataManifest(object):
    def __init__(self, d):
        self.id = d['id']
        self.display_name = None
        self.language = None
        self.version = None
        self.update_uri = None
        self.download_uri = None
        self.authors = []
        self.active = True
        self.path = None
        self.min_cm_ver = None

        if 'display_name' in d:
            self.display_name = d['display_name']
        if 'language' in d:
            self.language = d['language']
        if 'authors' in d:
            self.authors = d['authors']
        if 'version' in d:
            self.version = d['version']
        if 'update-uri' in d:
            self.update_uri = d['update-uri']
        if 'download-uri' in d:
            self.download_uri = d['download-uri']
        if 'min-cm-version' in d:
            self.min_cm_ver = d['min-cm-version']


def append_to(collection, item, pack):

    item.source_pack = pack

    if item in collection:
        i = collection.index(item)
        collection[i] = item
    else:
        collection.append(item)


class Data(object):
    def __init__(self, data_dirs=None, blacklist=None, log=True):
        if not blacklist:
            blacklist = []
        if not data_dirs:
            data_dirs = []

        self.enable_log = log
        self.data_dirs = data_dirs
        self.blacklist = blacklist

        self.packs = []
        self.clans = []
        self.families = []
        self.schools = []
        self.spells = []
        self.skills = []
        self.merits = []
        self.flaws = []
        self.katas = []
        self.kihos = []
        self.weapons = []
        self.armors = []
        self.skcategs = []
        self.perktypes = []
        self.weapon_effects = []
        self.rings = []
        self.traits = []

        self.rebuild(data_dirs, blacklist)

    def rebuild(self, data_dirs=None, blacklist=None):
        if not blacklist:
            blacklist = []
        if not data_dirs:
            data_dirs = []

        self.data_dirs = data_dirs

        self.blacklist = blacklist
        self.packs = []
        self.clans = []
        self.families = []
        self.schools = []
        self.spells = []
        self.skills = []
        self.merits = []
        self.flaws = []
        self.katas = []
        self.kihos = []
        self.weapons = []
        self.armors = []
        self.skcategs = []
        self.perktypes = []
        self.weapon_effects = []
        self.rings = []
        self.traits = []

        for d in data_dirs:
            if d and os.path.exists(d):
                self.load_data(d)

    def get_packs(self):
        return self.packs

    def scan_data_folder_for_packs(self, data_path):
        for path, dirs, files in os.walk(data_path):
            dirn = os.path.basename(path)

            if dirn.startswith('.'):
                continue

            try:
                manifest_path = os.path.join(path, 'manifest')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as manifest_fp:
                        dm = DataManifest(json.load(manifest_fp))
                        if dm.id in self.blacklist:
                            dm.active = False
                        dm.path = path
                        self.packs.append(dm)

                        if self.enable_log:
                            print('DATA PACK', dm.id, dm.display_name)
            except Exception as ex:
                print(ex)

    def load_data_from_pack(self, pack):

        if not pack:
            return

        if not pack.active:
            if self.enable_log:
                print('{0} is blacklisted'.format(pack.id))
            return

        for path, dirs, files in os.walk(pack.path):

            for file_ in files:
                if file_.startswith('.') or file_.endswith('~'):
                    continue
                if not file_.endswith('.xml'):
                    continue
                try:
                    self.__load_xml(os.path.join(path, file_), pack)
                except Exception as e:
                    if self.enable_log:
                        print("cannot parse file {0}".format(file_))
                        import traceback
                        traceback.print_exc()
                    else:
                        raise DataPackLoadingError(file_, str(e))

    def load_data(self, data_path):
        # iter through all the data tree and import all xml files

        self.scan_data_folder_for_packs(data_path)

        for p in self.packs:
            self.load_data_from_pack(p)

        if self.enable_log:
            self.__log_imported_data(data_path)

    def load_from_file(self, path):
        self.rebuild()
        return self.__load_xml(path)

    def __load_xml(self, xml_file, pack=None):
        # print('load data from {0}'.format(xml_file))
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root is None or root.tag != 'L5RCM':
            raise Exception("Not an L5RCM data file")
        for elem in list(root):
            if elem.tag == 'Clan':
                append_to(self.clans, Clan.build_from_xml(elem), pack)
            elif elem.tag == 'Family':
                append_to(self.families, Family.build_from_xml(elem), pack)
            elif elem.tag == 'School':
                append_to(self.schools, School.build_from_xml(elem), pack)
            elif elem.tag == 'SkillDef':
                append_to(self.skills, Skill.build_from_xml(elem), pack)
            elif elem.tag == 'SpellDef':
                append_to(self.spells, Spell.build_from_xml(elem), pack)
            elif elem.tag == 'Merit':
                append_to(self.merits, Perk.build_from_xml(elem), pack)
            elif elem.tag == 'Flaw':
                append_to(self.flaws, Perk.build_from_xml(elem), pack)
            elif elem.tag == 'SkillCateg':
                append_to(self.skcategs, SkillCateg.build_from_xml(elem), pack)
            elif elem.tag == 'KataDef':
                append_to(self.katas, Kata.build_from_xml(elem), pack)
            elif elem.tag == 'KihoDef':
                append_to(self.kihos, Kiho.build_from_xml(elem), pack)
            elif elem.tag == 'PerkCateg':
                append_to(self.perktypes, PerkCateg.build_from_xml(elem), pack)
            elif elem.tag == 'EffectDef':
                append_to(self.weapon_effects, WeaponEffect.build_from_xml(elem), pack)
            elif elem.tag == 'Weapon':
                append_to(self.weapons, Weapon.build_from_xml(elem), pack)
            elif elem.tag == 'Armor':
                append_to(self.armors, Armor.build_from_xml(elem), pack)
            elif elem.tag == 'RingDef':
                append_to(self.rings, GenericId.build_from_xml(elem), pack)
            elif elem.tag == 'TraitDef':
                append_to(self.traits, GenericId.build_from_xml(elem), pack)

        del root
        del tree

    def __log_imported_data(self, source):
        map_ = {'clans': self.clans,
                'families': self.families,
                'schools': self.schools,
                'spells': self.spells,
                'skills': self.skills,
                'merits': self.merits,
                'flaws': self.flaws,
                'katas': self.katas,
                'kihos': self.kihos,
                'weapons': self.weapons,
                'armors': self.armors,
                'skcategs': self.skcategs,
                'perktypes': self.perktypes,
                'weapon_effects': self.weapon_effects}

        print('IMPORTED DATA', source)
        for k in map_:
            print("imported {0} {1}".format(len(map_[k]), k))


class DataFile(Data):
    def __init__(self, fp=None):
        super(DataFile, self).__init__()

        self.path = None
        if fp is not None:
            self.load_from_file(fp)

    def save(self, new_path=None):

        if new_path:
            self.path = new_path

        print('saving to', self.path)

        import lxml.etree as XML
        root = XML.Element('L5RCM')

        stuff = (self.clans + self.families + self.schools + self.spells +
                 self.skills + self.katas + self.kihos + self.weapons +
                 self.armors + self.skcategs + self.perktypes + self.weapon_effects)

        for e in stuff:
            e.write_into(root)

        for m in self.merits:
            m.write_into("Merit", root)

        for f in self.flaws:
            f.write_into("Flaw", root)

        for r in self.rings:
            f.write_into("RingDef", root)

        for t in self.rings:
            f.write_into("TraitDef", root)

        try:
            XML.ElementTree(root).write(self.path, pretty_print=True, encoding='UTF-8', xml_declaration=True)
        except Exception as ex:
            print('save failed', ex)
