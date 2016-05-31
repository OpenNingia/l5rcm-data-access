# -*- coding: utf-8 -*-
# Copyright (C) 2014 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import l5rdal
import os
from collections import OrderedDict

try:
    # setup jinja2
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('l5rcm', 'templates'))

    class ReportBuilder(object):
        '''Build an HTML summary of the dal contents'''
        def __init__(self, in_path, out_path):
            self.out_path = out_path
            self.in_path  = in_path
            self.data     = None

        def build(self):
            # load _all_ the packs
            self.data = dal.Data( [self.in_path] )

            data_map = {}

            core_pack = [ x for x in self.data.packs if x.id == 'core' ]
            pack_list = sorted([ x for x in self.data.packs if x.id != 'core' ], cmp=lambda x,y: cmp(x.display_name, y.display_name) )

            for p in self.data.packs:
                # build content summary for each pack in different files
                data_map[ p.id ] = self.get_pack_data(p)

            # finally build the index
            self.build_index(core_pack + pack_list, data_map)

        def build_index(self, packs, pack_data):
            o = os.path.join(self.out_path, "index.html")
            tmpl = env.get_template('index.thtml')

            with open(o, 'wt') as fobj:
                fobj.write( tmpl.render(packs = packs, pack_data = pack_data) )

        def build_pack_report(self, pack):
            o = os.path.join(self.out_path, pack.id + ".html")
            tmpl = env.get_template('pack.thtml')

            # load a single package
            dp = dal.Data( [pack.path] )
            print(dp.__dict__)

            with open(o, 'wt') as fobj:
                fobj.write( tmpl.render(pack = pack, data = dp) )

        def get_pack_data(self, pack):
            # load a single package
            return dal.Data( [pack.path] )
except:
    pass


class ContentToMarkDown(object):

    '''Build an HTML summary of the dal contents'''
    def __init__(self, in_path, out_path):
        self.out_path = out_path
        self.in_path  = in_path
        self.data     = None

    def build(self):
        # load _all_ the packs
        self.data = dal.Data( [self.in_path] )

        with open( self.out_path, 'wb' ) as self.fp:

            self.md_h1( self.data.packs[0].display_name )

            self.build_clan_list    ()
            self.build_family_list  ()
            self.build_school_list  ()
            self.build_advanced_school_list  ()
            self.build_alternate_path_list   ()
            self.build_skill_list   ()
            self.build_spell_list   ()

            self.build_merit_list   ()
            self.build_flaw_list    ()
            self.build_kata_list    ()
            self.build_kiho_list    ()

    def md_sethext( self, text, char ):
        self.fp.write( u"\n" + text + u"\n" )
        self.fp.write( char*len(text) + u"\n" )

    def md_atx( self, text, n ):
        self.fp.write( u"\n{} {}\n".format( u"#"*n, text ) )

    def md_h1( self, text ):
        self.md_sethext( text, u'=' )

    def md_h2( self, text ):
        self.md_sethext( text, u'-' )

    def md_h3( self, text ):
        self.md_atx( text, 3 )

    def md_h4( self, text ):
        self.md_atx( text, 4 )

    def md_h5( self, text ):
        self.md_atx( text, 5 )

    def md_h6( self, text ):
        self.md_atx( text, 6 )

    def md_bullet( self, text ):
        self.fp.write( u"* " + text + u"\n" )

    def fmt_anchor( self, text, anchor ):
        return "[{}](#{})".format(text, anchor)

    def build_clan_list(self):

        if len( self.data.clans ) == 0:
            return

        self.md_h2( u"Clans" )

        for c in sorted( self.data.clans, key = lambda x: x.name ):
            self.md_bullet( c.name )

        #self.fp.write( u"\n" )

    def build_family_list(self):

        clans = OrderedDict.fromkeys( [ x.clanid for x in self.data.families ] ).keys()

        if len( clans ) == 0:
            return

        self.md_h2( u"Families" )

        for c in sorted(clans):
            clan_families = [ x.name for x in self.data.families if x.clanid == c ]
            self.md_h3( u"[{}]".format(c) )

            for f in sorted(clan_families):
                try:
                    self.md_bullet( f.decode('utf-8') )
                except:
                    print('cannot write', f)

            #self.fp.write( u"\n" )


    def __build_school_list(self, caption, slist):

        clans = OrderedDict.fromkeys( [ x.clanid for x in slist ] ).keys()

        if len( clans ) == 0:
            return

        self.md_h2( caption )

        for c in sorted(clans):
            clan_schools = [ x.name for x in slist if x.clanid == c ]

            self.md_h3( u"[{}]".format(c) )

            for f in sorted(clan_schools):
                try:
                    self.md_bullet( f.decode('utf-8') )
                except:
                    print('cannot write', f)

            #self.fp.write( "\n" )

    def build_school_list(self):

        base_schools = [ x for x in self.data.schools if 'advanced' not in x.tags and 'alternate' not in x.tags ]
        self.__build_school_list( u'Schools', base_schools )

    def build_advanced_school_list(self):

        adv_schools = [ x for x in self.data.schools if 'advanced' in x.tags ]
        self.__build_school_list( u'Advanced Schools', adv_schools )

    def build_alternate_path_list(self):

        alt_schools = [ x for x in self.data.schools if 'alternate' in x.tags ]
        self.__build_school_list( u'Alternate Paths', alt_schools )

    def build_skill_list(self):

        categs = OrderedDict.fromkeys( [ x.type for x in self.data.skills ] ).keys()

        self.md_h2( u"Skills" )

        for c in sorted(categs):

            skills = [ x.name for x in self.data.skills if x.type == c ]

            self.md_h3( u"[{}]".format(c) )

            for f in sorted(skills):
                try:
                    self.md_bullet( f.decode('utf-8') )
                except:
                    print('cannot write', f)

    def build_spell_list(self):

        categs = OrderedDict.fromkeys( [ x.element for x in self.data.spells ] ).keys()

        self.md_h2( u"Spells" )

        for c in sorted(categs):

            spells = [ x for x in self.data.spells if x.element == c ]
            self.md_h3( u"[{}]".format(c) )

            for i in range(1, 10):
                spells_rank = [ x.name for x in spells if x.mastery == i ]

                if len( spells_rank ) > 0:

                    self.md_h4( u"[Mastery {}]".format(i) )

                    for f in sorted(spells_rank):
                        try:
                            self.md_bullet( f.decode('utf-8') )
                        except:
                            print('cannot write', f)

    def build_perk_list( self, caption, plist ):

        categs = OrderedDict.fromkeys( [ x.type for x in plist ] ).keys()

        self.md_h2( caption )

        for c in sorted(categs):

            perks = [ x.name for x in plist if x.type == c ]

            self.md_h3( u"[{}]".format(c) )

            for f in sorted(perks):
                try:
                    self.md_bullet( f.decode('utf-8') )
                except:
                    print('cannot write', f)

    def build_merit_list( self ):
        self.build_perk_list( u'Advantages', self.data.merits )

    def build_flaw_list( self ):
        self.build_perk_list( u'Disadvantages', self.data.flaws )


    def build_power_list( self, caption, plist ):

        categs = OrderedDict.fromkeys( [ x.element for x in plist ] ).keys()

        self.md_h2( caption )

        for c in sorted(categs):

            powers = [ x for x in plist if x.element == c ]
            self.md_h3( u"[{}]".format(c) )

            for i in range(1, 10):
                powers_rank = [ x.name for x in powers if x.mastery == i ]

                if len( powers_rank ) > 0:

                    self.md_h4( u"[Mastery {}]".format(i) )

                    for f in sorted(powers_rank):
                        try:
                            self.md_bullet( f.decode('utf-8') )
                        except:
                            print('cannot write', f)

    def build_kata_list(self):
        self.build_power_list( u"Kata", self.data.katas )

    def build_kiho_list(self):
        self.build_power_list( u"Kiho", self.data.kihos )