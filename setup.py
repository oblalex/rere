# -*- coding: utf-8 -*-
"""
rere: regex redone
------------------

    from rere import *

    money_regex = Exactly('$') + Digit*2 + (Exactly('.') + Digit*2).zero_or_one

    regex.match('$23.95') # ==> MatchObject(...)

Isn't this better than `regex.compile('\\\\$\\\\d\\\\d(\\\\.\\\\d\\\\d)?')`?

"""

from setuptools import setup


setup(
    name='rere',
    version='0.1.0',
    description='regex redone',
    long_description=__doc__,
    keywords=['re', 'regex', 'regular', 'expression', ],
    url='http://www.maleagrubb.com/rere',
    license='Apache 2',
    author='Malea Grubb',
    author_email='maleangrubb@gmail.com',
    py_modules=['rere'],
    platforms=['any'],
)
