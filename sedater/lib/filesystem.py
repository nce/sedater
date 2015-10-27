# ./sedater/sedater/lib/filesystem.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Sat, 10.10.2015 - 12:00:05 
# Modified:	Tue, 27.10.2015 - 19:02:42

import os
import re
from collections import namedtuple

class Crawler(object):
	inputSource = ''
	inputSourceIsDir  = False
	inputSourceIsFile = False
	existingFiles = []

	def __init__(self, inputSource):
		self.inputSourceIsDir = True if os.path.isdir(inputSource) else False
		self.inputSourceIsFile = True if os.path.isfile(inputSource) else False
		if not self.inputSourceIsFile and not self.inputSourceIsDir:
			raise AttributeError('No file or directory supplied as input source')
			return False
		self.inputSource = inputSource

	def crawl(self):
		"""
		Crawls all directories under supplied path and stores files 
		matching a certain filename criteria for further processing
		"""
		if self.inputIsFile:
			try:
				validFile = self._parseFileName(self.inputSource)
			except PermissionError:
				# TODO: log it
				pass

			if validFile:
				self.existingFiles.append(validFile)
		else:
			self._crawlDir(self.inputSource)

		if not self.files:
			return False

	def _crawlDir(self):
		# TODO: implement
		pass

	def _parseFileName(self, f):
		"""
		Apply a RegEx on a filename to extract foot orientation and session ID
		(aka patient) and an exercise id, if available.
		"""
		if not os.access(f, os.R_OK):
			raise PermissionError("No read access granted on '{}', skipping file")
			return False

		attr = [''] * 5                     # create list for file attributes
		attr[0], attr[1] = os.path.split(f) # 0: fullpath 1:filename

		# list of regexes we run the filename against
		## orientation is either left or right 
		## exercise is prefixed by 'E' and sometimes followed by the orientation
		## session is either prefixed by 'P', 'GA', 'GAstd' or 'Pat'
		orientation = re.compile("(left|right)", re.IGNORECASE|re.M)
		exercise    = re.compile("E([A-Za-z0-9]+)(?:left|right)?", re.M)
		session     = re.compile("P([0-9]+)E?|GA([0-9]+)|GAstd([0-9a-z]+)(?:left|right)|Pat([0-9a-z]+)(?:left|right)", re.IGNORECASE|re.M)

		orientationMatch = orientation.search(attr[1])
		exerciseMatch    = exercise.search(attr[1])
		sessionMatch     = session.search(attr[1])

		# extract the matches
		if orientationMatch: 
			attr[4] = orientationMatch.group(1).lower()
		if exerciseMatch: 
			attr[3] = exerciseMatch.group(1)
		if sessionMatch:
			for i in range(1, len(sessionMatch.groups()) + 1):
				if sessionMatch.group(i):
					attr[2] = sessionMatch.group(i)
					break
		return Fileattributes._make(attr)

Fileattributes = namedtuple('Fileattributes', 
		['path', 'filename', 'session', 'exercise', 'orientation'])
