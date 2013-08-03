#!/usr/bin/env python2.7
from distutils.core import setup
setup(
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    name='musicdb',
    packages=[
        'musicdb', 
        'musicdb.model', 
        'musicdb.view', 
        'musicdb.ctrl'
    ],
    url='https://github.com/JoostMolenaar/musicdb',
    version='0.1.0'
)


