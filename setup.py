#!/usr/bin/env python2.7
from distutils.core import setup
setup(
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    name='jjm.musicdb',
    packages=[
        'jjm.musicdb', 
        'jjm.musicdb.model', 
        'jjm.musicdb.view', 
        'jjm.musicdb.ctrl'
    ],
    url='https://github.com/JoostMolenaar/musicdb',
    version='0.1.0'
)


