# -*- coding: utf-8 -*-
"""
rere: regex redone
------------------

    from rere import *

    money_regex = Exactly('$') + Digit*2 + (Exactly('.') + Digit*2).zero_or_one

    regex.match('$23.95') # ==> MatchObject(...)

Isn't this better than `regex.compile('\\\\$\\\\d\\\\d(\\\\.\\\\d\\\\d)?')`?

"""

import re


class RegexBase(object):
    """Base class for smart regex"""

    def match(self, string):
        """Returns Python MatchObject if FULL match.

        This is not just a prefix match as in Python's re library. For example,
        "cat" will not match "catastrophe". For that, use the match_prefix()
        function.

        """
        return re.match(self.pattern + '$', string)

    def match_prefix(self, string):
        """Returns Python MatchObject if prefix match.

        This function offers the same functionality as Python's re library's
        re.match(). For example, "cat" will match "catapult."

        """
        return re.match(self.pattern, string)

    def search(self, string):
        """Scans through string looking for match.

        If a match is found, returns MatchObject, otherwise returns None.

        """
        return re.search(self.pattern, string)

    def re_str(self):
        """This function is used to convert a string to a regex string pattern.

        This should NOT be called in this base class with proper usage. It is
        implemented in subclasses and handled there.

        """
        raise NotImplementedError('subclass must implement own re_str()')

    def __add__(self, friend):
        """Use + to chain together multiple RegexBases"""
        return MultipartRegex([self, friend])

    def __mul__(self, amt):
        """Use * to repeat RegexBase amt number of times"""
        return RepeatableRegex(self, amt)

    def __or__(self, friend):
        """Use | for "or" functionality:

        For example: Exactly('cat') | Exactly('fish')

        """
        return OrRegex([self, friend])

    def as_group(self, name):
        """Define a regex part as a group

        This function calls the Group() class.

        For example: r = letter.one_or_more.as_group('firstname')
                     r2 = letter.one_or_more.as_group('lastname')
                     new_r = r + r2
        m = new_r.match("Malea Grubb")
        m.group('firstname') # ==> "Malea"
        m.group('lastname') # ==> "Grubb"
        """
        return Group(self, name)

    @property
    def pattern(self):
        """Show final cached regex pattern.
        """
        _pattern = getattr(self, '_pattern', None)
        if _pattern is None:
            _pattern = self.re_str()
            self._pattern = _pattern
        return _pattern

    @property
    def one_or_more(self):
        """Use to specify chain length requirement (one or more)

        In other words, this returns a new regex that matches one or more
        repetitions of this one pattern. This calls the OneOrMoreRegex
        class.

        For example, if you want Exactly('cat'), but want at least one match
        and up to any amount following, call Exactly('cat').one_or_more. This
        will call OneorMore(Exactly('cat'))

        """
        return OneOrMoreRegex(self)

    @property
    def zero_or_more(self):
        """Used to specify chain length requirement (zero or more)

        In other words, this returns a new regex that matches any number of
        repetitions of this one, including an empty string (no repetitions).

        For example, if you want Exactly('cat'), but it does not NEED to be
        included but could be there any number of times, use
        Exactly('cat').zero_or_more, which will call ZeroOrMore(Exactly('cat'))
        """
        return ZeroOrMoreRegex(self)

    @property
    def zero_or_one(self):
        """Used to specify chain length requirement (zero or one)

        In other words, this returns a new regex that matches either this one
        or an empty string.

        For example, if you want Exactly('cat') as an option, but it is either
        there once or not at all, use Exactly('cat').zero_or_one, which will
        call ZeroOrOne(Exactly('cat'))
        """
        return ZeroOrOneRegex(self)


class RawRegex(RegexBase):
    """Match a user specified raw regex"""

    def __init__(self, pattern):
        self._pattern = pattern

    def re_str(self):
        return self._pattern


class MultipartRegex(RegexBase):
    """Container of RegexParts"""

    def __init__(self, parts):
        self.parts = parts

    def re_str(self):
        """Generate regex as a string"""
        multi = [part.re_str() for part in self.parts]
        return ''.join(multi)

    def __add__(self, friend):
        """Add a Regex part to a MultipartRegex"""
        return MultipartRegex(self.parts + [friend])


class OrRegex(RegexBase):
    """This class is called when the user uses | to specify "or"

    For example, Exactly('cat') | Exactly('dog')

    """
    def __init__(self, parts):
        self.parts = parts

    def re_str(self):
        """Generate regex as a string"""
        return '({})'.format('|'.join(part.re_str() for part in self.parts))

    def __or__(self, friend):
        """Use | to use or"""
        return OrRegex(self.parts + [friend])


class OneOrMoreRegex(RegexBase):
    """This should not ever be called by the user.

    It is returned by the .one_or_more property of the base class
    and contains a reference to the calling regex

    For example, Exactly('cat').one_or_more <--> OneOrMoreRegex(Exactly('cat'))
    They both would create the regex: ((cat)+)
    """

    def __init__(self, part):
        self.part = part

    def re_str(self):
        return '({})+'.format(self.part.re_str())


class ZeroOrMoreRegex(RegexBase):
    """This should not ever be called by the user.

    It is returned by the .zero_or_more property of the base class
    and contains a reference to the calling regex

    For example, Exactly('cat').zero_or_more is equivalent to
    ZeroOrMoreRegex(Exactly('cat')).  They both would create the regex:
    "(cat)*".

    """
    def __init__(self, part):
        self.part = part

    def re_str(self):
        return '({})*'.format(self.part.re_str())


class ZeroOrOneRegex(RegexBase):
    """This should not ever be called by the user.

    It is returned by the .zero_or_one property of the base class
    and contains a reference to the calling regex

    For example, Exactly('cat').zero_or_one <--> ZeroOrOneRegex(Exactly('cat'))
    They both would create the regex: ((cat)?)
    """

    def __init__(self, part):
        self.part = part

    def re_str(self):
        return '({})?'.format(self.part.re_str())


class RepeatableRegex(RegexBase):
    """Defines how much times Regex must be repeated"""

    def __init__(self, base, times):
        self.base = base
        self.times = times

    def re_str(self):
        """Generate regex as a string"""
        times = self.times

        if isinstance(times, (tuple, list)):
            try:
                # X{n,m} case (at least n but not more than m times)
                times = "{},{}".format(*times)
            except IndexError:
                # X{n,} case (at least n times)
                times = str(times[0]) + ","

        return '({}){{{}}}'.format(self.base.re_str(), times)


class Exactly(RegexBase):
    """Allows a user to specify the exactly string they want matched against"""

    def __init__(self, string):
        self.string = string

    def re_str(self):
        return re.escape(self.string)


class Group(RegexBase):
    """Specify a group name for a regex part

    This is returned by the as_group function.

    """
    def __init__(self, part, name):
        self.part = part
        self.name = name

    def re_str(self):
        return '(?P<{}>{})'.format(self.name, self.part.re_str())

# Module-level constants should be ALL_CAPS, but that might make the API more
# confusing for users (at least it would for me, so this is the assumption I'm
# running with. So I'm disabling pylint checking for the following constants.
# pylint: disable=invalid-name

# Shortcut for matching any character, including newline
AnyChar = RawRegex(r'(.|\n)')

# Shortcut for matching any digit (0-9)
Digit = RawRegex(r'\d')

# Shortcut for matching any letter (case insensitive)
Letter = RawRegex(r'[A-Za-z]')

# Shortcut for matching whitespace
Whitespace = RawRegex(r'\s')

# Shortcut to match any string of any length (not just one char)
Anything = AnyChar.zero_or_more

# Shortcut to match beginning of string
StringStart = RawRegex(r'^')

# Shortcut to match end of string
StringEnd = RawRegex(r'$')

# Re-enable checks for later code.
# pylint: enable=invalid-name
