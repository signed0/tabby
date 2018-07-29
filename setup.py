#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'Tabby',
    version = '0.4.0',
    packages = ['tabby'],
    author = 'Nathan Villaescusa',
    author_email = 'nathan@signedzero.com',
    description = 'Reads tabular data and turns it into python dicts',
    keywords = 'csv tsv tabular',
    url = 'http://github.com/signed0/tabby',
    test_suite = 'tabby.tests.tests_all',
    license = 'BSD',
    entry_points = {},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires = [],
    zip_safe=True,
)
