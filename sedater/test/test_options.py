# ./sedater/test/test_options.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Mon, 05.10.2015 - 12:59:56 
# Modified:	Mon, 05.10.2015 - 15:40:44

import unittest
import logging as log

from lib import options

class TestCommandLineParameters(unittest.TestCase):
	def setUp(self):
		self.cli = options.CLIParser()

	def test_default_settings(self):
		self.cli.parseForSedater(None)
		self.assertEquals(self.cli.hasVerbose, False)
		self.assertEquals(self.cli.hasDebug, False)
		self.assertEquals(self.cli.hasPlot, False)
	def test_verbose_mode_on(self):
		self.cli.parseForSedater(['-v'])
		self.assertEquals(self.cli.hasVerbose, True)
		self.cli.parseForSedater(['--verbose'])
		self.assertEquals(self.cli.hasVerbose, True)

		self.assertEquals(self.cli.log.getEffectiveLevel(), log.INFO)
	def test_debug_mode_on(self):
		self.cli.parseForSedater(['-d'])
		self.assertEquals(self.cli.hasDebug, True)
		self.cli.parseForSedater(['--debug'])
		self.assertEquals(self.cli.hasDebug, True)

		self.assertEquals(self.cli.log.getEffectiveLevel(), log.DEBUG)
	def test_headers_on(self):
		self.cli.parseForSedater(['-t'])
		self.assertEquals(self.cli.hasCsvHeader, True)
		self.cli.parseForSedater(['--csv-header'])
		self.assertEquals(self.cli.hasCsvHeader, True)


