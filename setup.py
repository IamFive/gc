# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-3-19
#

from setuptools import setup, find_packages
from guildconnections import version

# Stops exit traceback on tests
try:
    import multiprocessing
except:
    pass


# read requirements from requirements.txt
with open('requirements.txt') as f:
    requireds = f.read().splitlines()


# copy raw files for deploy
data_files = [
]

setup(
      name="guideconnections",
      version=version(),
      description="Guide Connections",
      author="Woo cupid",
      author_email="xmufive@gmail.com",
      license="LGPL",
      data_files=data_files,
      packages=find_packages(),
      install_requires=requireds,
#      test_suite='nose.collector',
#      setup_requires=['nose', 'coverage=2.85', 'NoseXUnit'],
      platforms='any',
      zip_safe=False
)
