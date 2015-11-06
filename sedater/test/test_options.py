# ./sedater/test/test_options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Mon, 05.10.2015 - 12:59:56 
# Modified: Fri, 06.11.2015 - 17:53:25

import unittest
import logging as log

from sedater import options

class TestCommandLineParameters(unittest.TestCase):
    def setUp(self):
        self.cli = options.CLIParser()

    def test_default_settings(self):
        self.cli.parseForSedater(None)
        self.assertEquals(self.cli.hasVerbose, False)
        self.assertEquals(self.cli.hasDebug, False)
        self.assertEquals(self.cli.outputDirPrefix, './')
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
    def test_output_dir_setting(self):
        self.cli.parseForSedater(['-o /foo'])
        self.assertEquals(self.cli.outputDirPrefix, '/foo/')
        self.cli.parseForSedater(['--output-dir=/bar/'])
        self.assertEquals(self.cli.outputDirPrefix, '/bar//')
        self.cli.parseForSedater(['-o foo'])
        self.assertEquals(self.cli.outputDirPrefix, './foo/')
    def test_logging_setup(self):
        self.cli.parseForSedater(['-v'])
        self.assertEquals(self.cli.log.getEffectiveLevel(), log.INFO)
        self.cli.parseForSedater(['-d'])
        self.assertEquals(self.cli.log.getEffectiveLevel(), log.DEBUG)


