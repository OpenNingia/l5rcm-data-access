# -*- coding: utf-8 -*-
__author__ = 'Daniele Simonetti'

import unittest
import l5rdal as dal
import l5rdal.query

class TestDal(unittest.TestCase):

    def setUp(self):
        # inject some data
        self.data = dal.Data([], [])

    def tearDown(self):
        pass

    def test_unit_test(self):
        """
        test the unit test framework
        :return:
        """
        self.assertTrue(self.data is not None)

    def test_simple(self):
        xml_ = "<L5RCM></L5RCM>"
        self.data.from_string(xml_)
        self.assertTrue(True)

    def test_clan(self):
        xml_ = "<L5RCM><Clan id='bar' name='foo'/></L5RCM>"
        self.data.from_string(xml_)
        self.assertEqual(1, len(self.data.clans))
        self.assertEqual('bar', self.data.clans[0].id)
        self.assertEqual('foo', self.data.clans[0].name)

    def test_family(self):
        xml_ = """<L5RCM>
        <Family id='bar' name='foo' clanid='baz'>
            <Trait>bau</Trait>
        </Family>
        </L5RCM>"""

        self.data.from_string(xml_)
        self.assertEqual(1, len(self.data.families))
        self.assertEqual('bar', self.data.families[0].id)
        self.assertEqual('foo', self.data.families[0].name)
        self.assertEqual('baz', self.data.families[0].clanid)
        self.assertEqual('bau', self.data.families[0].trait)

    def test_modifier_scalar(self):
        xml_ = """<L5RCM>
        <ModifierDef target='dragon_kitsukis_method' kind='tech'>
            <Mod affects='armor_tn' value='traits.perception'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        self.assertEqual(1, len(self.data.modifier_sets))
        md = self.data.modifier_sets[0]
        self.assertEqual('dragon_kitsukis_method', md.target)
        self.assertEqual('tech', md.kind)
        self.assertFalse(md.partial)
        self.assertEqual(1, len(md.mods))
        mod = md.mods[0]
        self.assertEqual('armor_tn', mod.affects)
        self.assertEqual('traits.perception', mod.value)
        self.assertEqual('add', mod.op)
        self.assertEqual('auto', mod.when)
        self.assertFalse(mod.is_roll)

    def test_modifier_roll_typed(self):
        xml_ = """<L5RCM>
        <ModifierDef target='crane_the_way_of_the_crane' kind='tech'>
            <Mod affects='initiative' value='2 * skills.iaijutsu'/>
            <Mod affects='attack_roll' roll='1' keep='1' bonus='school_rank'
                 when='center_stance'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        md = self.data.modifier_sets[0]
        self.assertEqual(2, len(md.mods))
        atk = md.mods[1]
        self.assertEqual('attack_roll', atk.affects)
        self.assertEqual('1', atk.roll)
        self.assertEqual('1', atk.keep)
        self.assertEqual('school_rank', atk.bonus)
        self.assertEqual('center_stance', atk.when)
        self.assertTrue(atk.is_roll)

    def test_modifier_stacking_same_target(self):
        xml_ = """<L5RCM>
        <ModifierDef target='same' kind='tech'>
            <Mod affects='armor_tn' value='1'/>
        </ModifierDef>
        <ModifierDef target='same' kind='tech'>
            <Mod affects='reduction' value='2'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        # both definitions must be kept (stacking), not overwritten
        self.assertEqual(2, len(self.data.modifier_sets))
        self.assertEqual(2, len(dal.query.get_modifiers_for(self.data, 'same')))

    def test_modifier_requires_and_partial(self):
        xml_ = """<L5RCM>
        <ModifierDef target='lame' kind='flaw' partial='true'>
            <Mod affects='ring_rank' detail='ring:water' op='set' value='1'/>
        </ModifierDef>
        <ModifierDef target='dragon_way_of_the_dragon' kind='tech'>
            <Mod affects='armor_tn' value='school_rank'
                 requires="wielding('daisho')"/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        lame = dal.query.get_modifiers_for(self.data, 'lame')[0]
        self.assertTrue(lame.partial)
        self.assertEqual('set', lame.mods[0].op)
        self.assertEqual('ring:water', lame.mods[0].detail)
        dragon = dal.query.get_modifiers_for(self.data, 'dragon_way_of_the_dragon')[0]
        self.assertEqual("wielding('daisho')", dragon.mods[0].requires)

    def test_modifier_oneof_and_param(self):
        xml_ = """<L5RCM>
        <ModifierDef target='the_power_of_the_mountain' kind='kata'>
            <Param name='x' max='rings.earth'/>
            <Mod affects='armor_tn' value='-x'/>
            <Mod affects='damage_roll' bonus='x'/>
        </ModifierDef>
        <ModifierDef target='tattoo_bear' kind='tattoo'>
            <OneOf>
                <Mod affects='trait_rank' detail='trait:stamina' value='school_rank'/>
                <Mod affects='trait_rank' detail='trait:strength' value='ceil(school_rank/2)'/>
            </OneOf>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        mtn = dal.query.get_modifiers_for(self.data, 'the_power_of_the_mountain')[0]
        self.assertEqual(1, len(mtn.params))
        self.assertEqual('x', mtn.params[0].name)
        self.assertEqual('rings.earth', mtn.params[0].max)
        self.assertEqual(2, len(mtn.mods))
        bear = dal.query.get_modifiers_for(self.data, 'tattoo_bear')[0]
        self.assertEqual(1, len(bear.groups))
        self.assertEqual(2, len(bear.groups[0].options))

    def test_modifier_substitute(self):
        xml_ = """<L5RCM>
        <ModifierDef target='balance_the_elements_style' kind='kata'>
            <Substitute affects='initiative' use='void' instead_of='reflexes'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        md = self.data.modifier_sets[0]
        self.assertEqual(1, len(md.substitutions))
        sub = md.substitutions[0]
        self.assertEqual('initiative', sub.affects)
        self.assertEqual('void', sub.use)
        self.assertEqual('reflexes', sub.instead_of)

    def test_modifier_mastery_rank(self):
        xml_ = """<L5RCM>
        <ModifierDef target='war_fan' kind='mastery' rank='5'>
            <Mod affects='armor_tn' value='1'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        md = self.data.modifier_sets[0]
        self.assertEqual(5, md.rank)
        self.assertEqual('mastery', md.kind)

    def test_modifier_query_kind_filter(self):
        xml_ = """<L5RCM>
        <ModifierDef target='dup' kind='tech'>
            <Mod affects='armor_tn' value='1'/>
        </ModifierDef>
        <ModifierDef target='dup' kind='path'>
            <Mod affects='reduction' value='1'/>
        </ModifierDef>
        </L5RCM>"""
        self.data.from_string(xml_)
        self.assertEqual(2, len(dal.query.get_modifiers_for(self.data, 'dup')))
        self.assertEqual(1, len(dal.query.get_modifiers_for(self.data, 'dup', kind='path')))