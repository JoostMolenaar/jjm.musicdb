#!/usr/bin/env python2.7

from distutils.core import setup
from glob import glob

setup(
    name='www-musicdb',
    version='0.1.0',
    packages=['mp3'],
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    #data_files={
    #    'conf/uwsgi': glob('conf/uwsgi/*.ini')
    #},
    #requires=[
    #    'WebOb(==1.2.3)',
    #    'mutagen(==1.2.0)',
    #    'pytz(==2012g)'
    #]
)


