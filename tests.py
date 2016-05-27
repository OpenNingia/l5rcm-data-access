# -*- coding: utf-8 -*-
__author__ = 'Daniele Simonetti'

import unittest
import l5rdal as dal

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
        self.assertEquals(1, len(self.data.clans))
        self.assertEquals('bar', self.data.clans[0].id)
        self.assertEquals('foo', self.data.clans[0].name)

    def test_family(self):
        xml_ = """<L5RCM>
        <Family id='bar' name='foo' clanid='baz'>
            <Trait>bau</Trait>
        </Family>
        </L5RCM>"""

        self.data.from_string(xml_)
        self.assertEquals(1, len(self.data.families))
        self.assertEquals('bar', self.data.families[0].id)
        self.assertEquals('foo', self.data.families[0].name)
        self.assertEquals('baz', self.data.families[0].clanid)
        self.assertEquals('bau', self.data.families[0].trait)