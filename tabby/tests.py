# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division, absolute_import

import unittest, datetime
from decimal import Decimal

from tabby.base import TabbyError
from tabby.fields import StringField, UnicodeField, BoolField, IntField, FloatField, DecimalField, DateTimeField
from tabby.fields import DateField, TimeField, ColorField, HumanTimespanField

class TabbyTest(unittest.TestCase):
    
    def test_string(self):
        self.assertEqual(StringField().parse('fõõ'.encode('UTF-8')), 'fõõ'.encode('UTF-8'))
        self.assertEqual(StringField().parse('\tfõõ    '.encode('UTF-8')), 'fõõ'.encode('UTF-8'))
        self.assertRaises(AttributeError, StringField().parse, 0)

    def test_unicode(self):
        self.assertEqual(UnicodeField().parse('fõõ'.encode('UTF-8')), 'fõõ')
        self.assertEqual(UnicodeField().parse('\tfõõ    '.encode('UTF-8')), 'fõõ')
        self.assertRaises(AttributeError, UnicodeField().parse, 0)

    def test_boolean(self):
        self.assertEqual(BoolField().parse('false'.encode('UTF-8')), False)
        self.assertEqual(BoolField().parse('f'.encode('UTF-8')), False)
        self.assertEqual(BoolField().parse('0'.encode('UTF-8')), False)
        
        self.assertEqual(BoolField().parse('1'.encode('UTF-8')), True)
        self.assertEqual(BoolField().parse('true'.encode('UTF-8')), True)
        self.assertEqual(BoolField().parse('t'.encode('UTF-8')), True)
        self.assertEqual(BoolField().parse('abra-cadabra'.encode('UTF-8')), True)

    def test_int(self):
        self.assertEqual(IntField().parse('0'.encode('UTF-8')), 0)
        self.assertEqual(IntField().parse('1'.encode('UTF-8')), 1)
        self.assertEqual(IntField().parse('501235'.encode('UTF-8')), 501235)
        self.assertEqual(IntField().parse('501235345623'.encode('UTF-8')), 501235345623)
        
        self.assertRaises(TabbyError, IntField().parse, 'asdf'.encode('UTF-8'))
        self.assertRaises(TabbyError, IntField().parse, '13.5'.encode('UTF-8'))

    def test_float(self):
        self.assertEqual(FloatField().parse('0'.encode('UTF-8')), float(0))
        self.assertEqual(FloatField().parse('1'.encode('UTF-8')), float(1))
        self.assertEqual(FloatField().parse('3.14159'.encode('UTF-8')), 3.14159)
        
        self.assertRaises(TabbyError, FloatField().parse, 'asdf'.encode('UTF-8'))

    def test_decimal(self):
        self.assertEqual(DecimalField().parse('0'.encode('UTF-8')), float(0))
        self.assertEqual(DecimalField().parse('1'.encode('UTF-8')), float(1))
        self.assertEqual(DecimalField().parse('3.14159'.encode('UTF-8')), Decimal('3.14159'))
        
        self.assertRaises(TabbyError, DecimalField().parse, 'asdf'.encode('UTF-8'))

    def test_datetime(self):
        self.assertEqual(DateTimeField().parse('1999-3-23T11:44:55'.encode('UTF-8')), datetime.datetime(1999, 3, 23, 11, 44, 55))
        self.assertEqual(DateTimeField(fmt='%m/%d/%Y').parse('3/23/1999'.encode('UTF-8')), datetime.datetime(1999, 3, 23))
        
        self.assertRaises(TabbyError, DateTimeField().parse, 'asdf'.encode('UTF-8'))

    def test_date(self):
        self.assertEqual(DateField(fmt='%m/%d/%Y').parse('3/23/1999'.encode('UTF-8')), datetime.date(1999, 3, 23))
        
        self.assertRaises(TabbyError, DateField().parse, 'asdf'.encode('UTF-8'))

    def test_time(self):
        self.assertEqual(TimeField().parse('11:44:55'.encode('UTF-8')), datetime.time(11, 44, 55))
        
        self.assertRaises(TabbyError, TimeField().parse, 'asdf'.encode('UTF-8'))

    def test_color(self):
        self.assertEqual(ColorField().parse('cc1122'.encode('UTF-8')), 'cc1122')
        self.assertEqual(ColorField().parse('fab'.encode('UTF-8')), 'ffaabb')
        
        self.assertRaises(TabbyError, ColorField().parse, 'asdf'.encode('UTF-8'))
        self.assertRaises(TabbyError, ColorField().parse, 'aabb'.encode('UTF-8'))
        self.assertRaises(TabbyError, ColorField().parse, '00000x'.encode('UTF-8'))

    def test_human_timespan(self):
        self.assertEqual(HumanTimespanField().parse('1 hour 3 minutes'.encode('UTF-8')), 3780)
        self.assertEqual(HumanTimespanField().parse('2 hour'.encode('UTF-8')), 7200)
        self.assertEqual(HumanTimespanField().parse('2 hour 1 minute'.encode('UTF-8')), 7260)

tests_all = unittest.TestLoader().loadTestsFromTestCase(TabbyTest)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(tests_all)
