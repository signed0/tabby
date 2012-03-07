#!/usr/bin/env python

import os.path
from setuptools import setup

setup(
    name = 'Tabby',
    version = '0.2',
    packages = ['tabby'],
    author = 'Nathan Villaescusa',
    author_email = 'nathan@signedzero.com',
    description = 'Reads tabular data and turns it into python dicts',
    keywords = 'csv tsv tabular',
    url = 'http://github.com/signed0/tabby',
    license = 'BSD',
    entry_points = {},
    classifiers = ['Development Status :: 3 - Alpha',
                   'Operating System :: OS Independent',
                   'License :: OSI Approved :: BSD License'
                   ],
    install_requires = [],
    zip_safe=True,
)
