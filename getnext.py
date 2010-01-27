#!/usr/bin/env python

import re
import os
import shutil
import subprocess

fmt_SEE   = re.compile('[^x]([0-9]{3,})[^p]')
fmt_sSeEE = re.compile('[sS]([0-9]+)[eE]([0-9]+)')
fmt_SxEE  = re.compile('([0-9]+)[xX]([0-9]+)')

discard = re.compile('([sS]ample|\.nfo$)')
media = re.compile('\.(mkv|avi|mpg|wmv|ogg)$')

def h_copy(fn):
	print 'Copying', fn
	shutil.copyfile(fn, os.path.basename(fn))

def h_unrar(fn):
	print 'Unpacking from RAR', fn
	subprocess.call(['unrar', 'x', fn])

handlers = [
	{'re': media, 'handler': h_copy},
	{'re': re.compile('\.rar$'), 'handler': h_unrar}
]

def extract_file_info(fn):
	match = fmt_SEE.search(fn)
	if (match == None):
		match = fmt_sSeEE.search(fn)
		if (match == None):
			match = fmt_SxEE.search(fn)
			if (match == None):
				return None
			else:
				return {'season': int(match.group(1)), 'episode': int(match.group(2))}
		else:
			return {'season': int(match.group(1)), 'episode': int(match.group(2))}
	else:
		see = match.group(1)
		return {'season': int(see[:-2]), 'episode': int(see[-2:])}

def fi_gt(fi1, fi2):
	if fi1['season'] == fi2['season']:
		return fi1['episode'] > fi2['episode']
	else:
		return fi1['season'] > fi2['season']

def fi_eq(fi1, fi2):
	return fi1['season'] == fi2['season'] and fi1['episode'] == fi2['episode']

def fi_inc(fi):
	retval = fi
	retval['episode'] = retval['episode'] + 1
	return retval

def get_episode(fi):
	dn = '.src'
	print 'About to download season', fi['season'], 'episode', fi['episode']
	ls = os.listdir(dn)
	for fn in ls:
		cfi = extract_file_info(fn)
		if (cfi != None and fi_eq(cfi, fi)):
			break
	else:
		print 'Episode not found'
		return
	cp_episode(os.path.join(dn, fn))

def cp_episode(path):
	dmatch = discard.search(path)
	if (dmatch != None):
		return
	if os.path.isfile(path):
		for handler in handlers:
			match = handler['re'].search(path)
			if (match == None):
				continue
			print 'Found file:', path
			handler['handler'](path)
	elif os.path.isdir(path):
		print 'Found directory:', path
		ls = os.listdir(path)
		for fn in ls:
			cp_episode(os.path.join(path, fn))
	else:
		print 'WTF', fn

ls = os.listdir('.')
fi = nfi = {'season': 0, 'episode': 0}
for fn in ls:
	if (media.search(fn) == None):
		continue
	cfi = extract_file_info(fn)
	if cfi != None and fi_gt(cfi, fi):
		fi = cfi

if (fi == nfi):
	print "Couldn't find any video files related to a series"
	sys.exit(1)

print 'Latest one is season', fi['season'], 'episode', fi['episode']
try:
	get_episode(fi_inc(fi))
except:
	print 'Failed to download next episode'
