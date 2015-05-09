#!/usr/bin/env python2.7

repo_names = ['core']
dist_names = ['pygraphviz']
static_dirs = ['web']

import os
from setuptools import setup

try:
    with open('musicdb.egg-info/version.txt', 'r') as f:
        version = f.read()
except:
    version = None

setup(
    name='musicdb',
    version=version,
    version_command=('git describe', 'pep440-git'),
    url='https://github.com/j0057/musicdb',
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    packages=[
        'musicdb',
        'musicdb.ctrl',
        'musicdb.model',
        'musicdb.view' ],
    data_files=[ (root, map(lambda f: root + '/' + f, files))
                 for src_dir in static_dirs
                 for (root, dirs, files) in os.walk(src_dir) ],
    install_requires=dist_names+repo_names,
    custom_metadata={
        'x_repo_names': repo_names,
        'x_dist_names': dist_names,
        'x_static_dirs': static_dirs })
