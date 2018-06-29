#!/usr/bin/env python


from distutils.core import setup
from cmspubstyle.__init__ import __version__


setup(name='cmspubstyle',
      version=__version__,
      description='Check CMS publications against PubComm rules',
      author='Robin Aggleton',
      url='https://github.com/raggleton/CMS-grammar-checker',
      packages=['cmspubstyle'],
      scripts=['cmspubstyle/pubcheck.py'],
     )
