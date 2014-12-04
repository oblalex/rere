#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from rere import *


class ReReTest(unittest.TestCase):

    def test_raw_regex(self):
        re = RawRegex(r'ab*')

        self.assertEqual(re.pattern, r'ab*')

        self.assertTrue(re.match('a'))
        self.assertTrue(re.match('ab'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('aa'))

        # rere's match function must match the whole string, not just a prefix
        # (like re.match)
        self.assertFalse(re.match('aba'))
        self.assertTrue(re.match_prefix('aba'))

    def test_exactly(self):
        re = Exactly('$2+$2')

        self.assertEqual(re.pattern, r'\$2\+\$2')

        self.assertTrue(re.match('$2+$2'))
        self.assertTrue(re.match_prefix('$2+$2+$1'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('$1+$2+$2'))
        self.assertFalse(re.match('$2+$2+$1'))

    def test_any_char(self):
        re = AnyChar

        self.assertTrue(re.match('a'))
        self.assertTrue(re.match('1'))
        self.assertTrue(re.match(' '))
        self.assertTrue(re.match('\n'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('ab'))

    def test_digit(self):
        re = Digit

        self.assertTrue(re.match('1'))

        self.assertFalse(re.match('11'))
        self.assertFalse(re.match('1a'))
        self.assertFalse(re.match('A'))

    def test_letter(self):
        re = Letter

        self.assertTrue(re.match('a'))
        self.assertTrue(re.match('A'))

        self.assertFalse(re.match('1'))
        self.assertFalse(re.match('a2'))

    def test_whitespace(self):
        re = Whitespace

        self.assertTrue(re.match(' '))
        self.assertTrue(re.match('\n'))

        self.assertFalse(re.match('2'))
        self.assertFalse(re.match('a 3 '))

    def test_anything(self):
        re = Anything

        self.assertTrue(re.match(''))
        self.assertTrue(re.match('ab'))
        self.assertTrue(re.match('ab\n123'))

    def test_multipart_regex(self):
        re = Exactly('123') + Anything + Exactly('a\n')

        self.assertEqual(re.pattern, '123((.|\\n))*a\\\n')

        self.assertTrue(re.match('123456a\n'))
        self.assertTrue(re.match('123a\na\n'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('123'))

    def test_one_or_more(self):
        re = Exactly('puppy').one_or_more

        self.assertEqual(re.pattern, r'(puppy)+')

        self.assertTrue(re.match('puppy'))
        self.assertTrue(re.match('puppypuppy'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('kitten'))

    def test_zero_or_more(self):
        re = Exactly('puppy').zero_or_more

        self.assertEqual(re.pattern, r'(puppy)*')

        self.assertTrue(re.match(''))
        self.assertTrue(re.match('puppy'))
        self.assertTrue(re.match('puppypuppy'))

        self.assertFalse(re.match('kitten'))

    def test_zero_or_one(self):
        re = Exactly('puppy').zero_or_one

        self.assertEqual(re.pattern, r'(puppy)?')

        self.assertTrue(re.match(''))
        self.assertTrue(re.match('puppy'))

        self.assertFalse(re.match('kitten'))
        self.assertFalse(re.match('puppypuppy'))

    def test_repeat_single_exactly_n_times(self):
        re = Exactly('cat') * 3

        self.assertEqual(re.pattern, r'(cat){3}')
        self.assertTrue(re.match('catcatcat'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('cat'))
        self.assertFalse(re.match('catcat'))
        self.assertFalse(re.match('catcatcatcat'))

    def test_repeat_single_at_least_n_times(self):
        re = Exactly('cat') * (2, )

        self.assertEqual(re.pattern, r'(cat){2,}')
        self.assertTrue(re.match('catcat'))
        self.assertTrue(re.match('catcatcat'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('cat'))

    def test_repeat_single_from_n_to_m_times(self):
        re = Exactly('cat') * (2, 3)

        self.assertEqual(re.pattern, r'(cat){2,3}')
        self.assertTrue(re.match('catcat'))
        self.assertTrue(re.match('catcatcat'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('cat'))
        self.assertFalse(re.match('catcatcatcat'))

    def test_repeat_multipart_exactly_n_times(self):
        re = (Exactly('cat') + Exactly('dog')) * 3

        self.assertEqual(re.pattern, r'(catdog){3}')
        self.assertTrue(re.match('catdogcatdogcatdog'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('catdog'))
        self.assertFalse(re.match('catdogcatdog'))
        self.assertFalse(re.match('catdogcatdogcatdogcatdog'))

    def test_repeat_multipart_at_least_n_times(self):
        re = (Exactly('cat') + Exactly('dog')) * (2, )

        self.assertEqual(re.pattern, r'(catdog){2,}')
        self.assertTrue(re.match('catdogcatdog'))
        self.assertTrue(re.match('catdogcatdogcatdogcatdog'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('catdog'))

    def test_repeat_multipart_from_n_to_m_times(self):
        re = (Exactly('cat') + Exactly('dog')) * (2, 3)

        self.assertEqual(re.pattern, r'(catdog){2,3}')
        self.assertTrue(re.match('catdogcatdog'))
        self.assertTrue(re.match('catdogcatdogcatdog'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match('catdog'))
        self.assertFalse(re.match('catdogcatdogcatdogcatdog'))

    def test_or(self):
        re = Exactly('cat') | Exactly('dog') | Exactly('snake')

        self.assertEqual(re.pattern, r'(cat|dog|snake)')

        self.assertTrue(re.match('cat'))
        self.assertTrue(re.match('dog'))
        self.assertTrue(re.match('snake'))

        self.assertFalse(re.match(''))

    def test_group(self):
        re = (
            Letter.one_or_more.as_group('first_name')
            + Whitespace.one_or_more
            + Letter.one_or_more.as_group('last_name')
        )
        self.assertEqual(
            re.pattern,
            r'(?P<first_name>([A-Za-z])+)(\s)+(?P<last_name>([A-Za-z])+)'
        )

        match = re.match('Malea Grubb')

        self.assertTrue(match)
        self.assertEqual(match.group('first_name'), 'Malea')
        self.assertEqual(match.group('last_name'), 'Grubb')

    def test_pattern(self):
        re = Exactly(r'hi') + Whitespace.one_or_more + Exactly(r'there')

        self.assertEqual(re.pattern, r'hi(\s)+there')
        self.assertIs(re.pattern, re.pattern)
        self.assertIsNot(re.re_str(), re.re_str())

    def test_string_start(self):
        re = StringStart + Exactly(r'pony')

        self.assertTrue(re.match('pony'))

        self.assertFalse(re.match(''))
        self.assertFalse(re.match(' pony '))


if __name__ == '__main__':
    unittest.main()
