#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# setup.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from glob import glob

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hw-railroad',
    description='Railroad hardware objects',
    long_description=long_description,
    url='https://github.com/geoff-coppertop/python-hw-railroad',
    author='Geoffrey Thomas',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='railroad',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    use_scm_version=True,
    setup_requires=[
        'setuptools_scm'
    ],
    # install_requires=[
    #     'hw_low_level',
    # ],
    # dependency_links=[
    #     'git+https://github.com/geoff-coppertop/python-hw-low-level#egg=hw_low_level',
    # ],
    project_urls={
        'Bug Reports': 'https://github.com/geoff-coppertop/python-hw-railroad/issues',
        'Source': 'https://github.com/geoff-coppertop/python-hw-railroad',
    },
)