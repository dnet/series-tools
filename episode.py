#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import series_tools
import copy

def x_SEE(match):
	see = match.group(1)
	return Episode(season = int(see[:-2]), episode = int(see[-2:]))

def x_double_raw(match):
	return Episode(season = int(match.group(1)), episode = int(match.group(2)))

def episode_max(fi1, fi2):
	if (fi1 == None):
		return fi2
	if (fi2 == None):
		return fi1
	if fi1.season == fi2.season:
		return fi1 if fi1.episode > fi2.episode else fi2
	else:
		return fi1 if fi1.season > fi2.season else fi2

def latest(dir):
	return reduce(lambda acc, e: episode_max(Episode.from_file(e), acc),
		filter(lambda e: series_tools.media.search(e) != None,
			os.listdir(dir)), None)

fi_formats = [
	{'re': re.compile('[^x]([0-9]{3,})[^p]'), 'extract': x_SEE},
	{'re': re.compile('[sS]([0-9]+)[eE]([0-9]+)'), 'extract': x_double_raw},
	{'re': re.compile('([0-9]+)[xX]([0-9]+)'), 'extract': x_double_raw}
]

class Episode:
	def __init__(self, season, episode):
		self.season = season
		self.episode = episode

	@classmethod
	def from_file(self, fn):
		for fmt in fi_formats:
			match = fmt['re'].search(fn)
			if (match != None):
				ex = fmt['extract'](match)
				ex.filename = fn
				return ex
		return None

	def next(self):
		retval = copy.deepcopy(self)
		retval.episode = retval.episode + 1
		return retval

	def equals(self, x):
		return self.season == x.season and self.episode == x.episode

	def __str__(self):
		return 'season %d episode %d' % (self.season, self.episode)
