# ./sedater/sedater/lib/options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Fri, 02.10.2015 - 15:57:02 
# Modified: Mon, 05.10.2015 - 15:49:38

import sys
import getopt, logging

class CLIParser(object):
	def __init__(self):
		pass

	def parseForSedater(self, arguments):
		_availableOpts = ['ptl:r:o:dvh', ['plot', 'csv-header',
				'left-calibration=', 'right-calibration=', 'output-dir=',
				'debug', 'verbose', 'help']]
		opts = self._initParse(arguments, _availableOpts)

		self.hasVerbose = False
		self.hasDebug   = False
		self.hasCsvHeader = False
		for opt, arg in opts:
			if opt in ('-h', '--help'):
				self._usage()
				return False
			elif opt in ('-v', '--verbose'):
				self.hasVerbose = True
			elif opt in ('-d', '--debug'):
				self.hasDebug = True
			elif opt in ('-t', '--csv-header'):
				self.hasCsvHeader = True

		self._initLogging()

	def _initLogging(self):
		logging.basicConfig(stream=sys.stdout, format="%(levelname)s - %(name)s")
		self.log = logging.getLogger()
		if self.hasDebug:
			self.log.setLevel(logging.DEBUG)
			self.log.debug("Debug logging enabled")
		elif self.hasVerbose:
			self.log.setLevel(logging.INFO)
			self.log.info("Verbose logging enabled")

	def _initParse(self, arguments, optsAvail):
		try:
			opts, args = getopt.getopt(arguments, optsAvail[0], optsAvail[1])
		except getopt.GetoptError as error:
			print(error)
			return False

		return opts
