NAME = musicdb

PIP_NAME = musicdb
PIP_REQ = requirements.txt

PKG_BASE = file://$(shell readlink -f ..)
PKG = core

STATIC_DIRS = conf web

MAIN ?= musicdb.main

