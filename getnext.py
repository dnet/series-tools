#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import shutil
import subprocess
import sys
from episode import *
import series_tools

discard = re.compile('([sS]ample|\.nfo$)')

def h_copy(fn):
	print 'Copying', fn
	shutil.copyfile(fn, os.path.basename(fn))

def h_unrar(fn):
	print 'Unpacking from RAR', fn
	subprocess.call(['unrar', 'x', fn])

handlers = [
	{'re': series_tools.media, 'handler': h_copy},
	{'re': re.compile('\.rar$'), 'handler': h_unrar}
]

def get_episode(fi):
	dn = '.src'
	print 'About to download', fi
	ls = os.listdir(dn)
	for fn in ls:
		cfi = Episode.from_file(fn)
		if (cfi != None and cfi.equals(fi)):
			if cp_episode(os.path.join(dn, fn)):
				break
	else:
		print 'Episode not found'
		return

def cp_episode(path):
	if (discard.search(path) != None):
		return
	if os.path.isfile(path):
		for handler in handlers:
			match = handler['re'].search(path)
			if (match == None):
				continue
			print 'Found file:', path
			handler['handler'](path)
			return True
	elif os.path.isdir(path):
		print 'Found directory:', path
		ls = os.listdir(path)
		retval = False
		for fn in ls:
			retval |= cp_episode(os.path.join(path, fn))
		return retval
	else:
		print 'WTF', fn
		return False

e = latest('.')

if e is None:
	print "Couldn't find any video files related to a series"
	sys.exit(1)

print 'Latest one is', e
try:
	get_episode(e.next())
except:
	print 'Failed to download next episode'
