#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from distutils.core import setup
from io import open

long_description = open(os.path.join(os.path.dirname(__file__), "README.md"), encoding='utf-8').read()

setup(
      name='everysport',
      version='1.2.0',
      packages=['everysport'],
      description='A Python wrapper for the Everysport API',
      author='Peter Stark',
      author_email='peterstark72@gmail.com',
      url='https://github.com/peterstark72/everysport',
      keywords = "python everysport API sport",
      long_description = long_description,
      classifiers=[
      	  'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: Free for non-commercial use',
          'Natural Language :: English',
          'Natural Language :: Swedish',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities'
          ],
      )