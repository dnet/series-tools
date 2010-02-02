#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import episode

fi = episode.latest('.')

if (fi == None):
	print "Couldn't find any video files related to a series"
	sys.exit(1)

try:
	os.startfile(fi.filename)
except:
	os.system('kfmclient exec %s' % fi.filename)