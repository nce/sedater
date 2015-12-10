# ./sedater/test/test_options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Mon, 05.10.2015 - 12:59:56 
# Modified: Thu, 10.12.2015 - 19:41:38

import unittest

from sedater.options import CLIParser

class TestCommandLineParameters(unittest.TestCase):
    def setUp(self):
        self.cli = CLIParser()

    def test_default_settings(self):
        self.cli.parseForSedater(['foo'])
        self.assertFalse(self.cli.args.csv_headers)
        self.assertFalse(self.cli.args.left_calibration)
        self.assertFalse(self.cli.args.right_calibration)
        self.assertFalse(self.cli.args.output_dir)
    def test_toggle_csv_header(self):
        self.cli.parseForSedater(['foo'])
        self.assertFalse(self.cli.args.csv_headers)
        self.cli.parseForSedater(['-c', 'foo'])
        self.assertTrue(self.cli.args.csv_headers)
        self.cli.parseForSedater(['--csv-headers', 'foo'])
        self.assertTrue(self.cli.args.csv_headers)
    def test_left_calibration_file(self):
        ref = res = 'foobar'
        self.cli.parseForSedater(['-l', ref, 'barfoo'])
        self.assertEquals(self.cli.args.left_calibration, res)
        self.cli.parseForSedater(['--left-calibration', ref, 'barfoo'])
        self.assertEquals(self.cli.args.left_calibration, res)
    def test_right_calibration_file(self):
        ref = res = 'foobar'
        self.cli.parseForSedater(['-r', ref, 'barfoo'])
        self.assertEquals(self.cli.args.right_calibration, res)
        self.cli.parseForSedater(['--right-calibration', ref, 'barfoo'])
        self.assertEquals(self.cli.args.right_calibration, res)
    def test_output_dir(self):
        ref = res = 'foobar'
        self.cli.parseForSedater(['-o', ref, 'barfoo'])
        self.assertEquals(self.cli.args.output_dir, res)
        self.cli.parseForSedater(['--output-dir', ref, 'barfoo'])
        self.assertEquals(self.cli.args.output_dir, res)
    def test_input_source_arguments(self):
        ref = res = ['foo', 'bar', 'foobar', 'barfoo']
        self.cli.parseForSedater(ref)
        self.assertEquals(self.cli.args.inputSource, ref)


