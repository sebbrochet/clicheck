#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from clicheck import __version__, __author__
from distutils.core import setup

setup(name='clicheck',
      version=__version__,
      description='CLI acceptance testing based on output comparison',
      long_description='This command-line tool lets you run acceptance tests on a CLI application',
      author=__author__,
      author_email='contact@sebbrochet.com',
      url='https://github.com/sebbrochet/clicheck',
      platforms=['linux'],
      license='MIT License',
      install_requires=['argparse, pyyaml'],
      package_dir={'clicheck': 'lib/clicheck'},
      packages=['clicheck'],
      scripts=['bin/clicheck'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Quality Assurance',
          ],
      )
