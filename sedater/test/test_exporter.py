# ./sedater/test/test_exporter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 23:09:28 
# Modified: Mon, 09.11.2015 - 12:11:25

import unittest
import os
from testfixtures import TempDirectory

import sys

from sedater.export import CSVExporter
from sedater.lib import shared

class TestCSVExporter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.dir = self.tmp.makedir('foobar')
        self.exp = CSVExporter()
    def tearDown(self):
        TempDirectory.cleanup_all()
    def test_creation_of_export_file(self):
        filename = 'foobar.csv'
        values = [shared.Sensorsegment._make([0] * 6)]
        status = self.exp.export(values, self.dir+filename)
        self.assertTrue(os.path.isfile(self.dir+filename))
        self.assertTrue(status)
    def test_content_of_export_file(self):
        filename = 'foobar.csv'
        values = [shared.Sensorsegment._make([0] * 6),
                shared.Sensorsegment._make([1] * 6)
                ]
        self.exp.export(values, self.dir+filename, False, False)
        res = self.tmp.read(self.dir+filename)
        ref = b'0,0,0,0,0,0\r\n1,1,1,1,1,1\r\n'
        self.assertEqual(ref, res)
    def test_content_with_header_with_indices(self):
        filename = 'foobar.csv'
        values = [shared.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, True, True)
        res = self.tmp.read(self.dir+filename)
        ref = b'Index,accelX,accelY,accelZ,gyroX,gyroY,gyroZ\r\n1,0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)
    def test_content_with_header_without_indices(self):
        filename = 'foobar.csv'
        values = [shared.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, True, False)
        res = self.tmp.read(self.dir+filename)
        ref = b'accelX,accelY,accelZ,gyroX,gyroY,gyroZ\r\n0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)
    def test_content_without_header_with_indices(self):
        filename = 'foobar.csv'
        values = [shared.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, False, True)
        res = self.tmp.read(self.dir+filename)
        ref = b'1,0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)

