# ./sedater/test/test_exporter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 08.11.2015 - 23:09:28 
# Modified: Thu, 10.12.2015 - 00:40:45

import unittest
import os
from testfixtures import TempDirectory

import sys

from sedater.export import CSVExporter

from sedater.export import XMLExporter
from xml.etree import ElementTree as et

from sedater.lib import shared as lib

class TestXMLExporter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.dir = self.tmp.makedir('foobar')
        self.exp = XMLExporter(self.dir)
    def tearDown(self):
        TempDirectory.cleanup_all()

    def test_creation_of_meta_info_file(self):
        filename = 'barfoo.xml'
        status = self.exp._exportMetaInformationToXML('', '', filename)
        self.assertTrue(os.path.isfile(self.dir+'metainformation.xml'))
        self.assertTrue(status)
    def test_content_of_meta_info_file(self):
        filename = 'barfoo.xml'
        status = self.exp._exportMetaInformationToXML('01', '02', filename)
        tree = et.parse(self.dir+'metainformation.xml')
        xml = tree.getroot()
        session = xml.find('Session')
        exercise = xml.find('Exercise')
        annotation = xml.find('Annotationfile')
        self.assertEquals('01', session.text)
        self.assertEquals('02', exercise.text)
        self.assertEquals('barfoo.xml', annotation.text)
    def DISABLEDtest_content_of_xml_export_file(self):
        src = lib.Sourcefile._make(['', '', '', '', lib.Orientation.left])
        input = lib.Validationfile._make([src, 'Gold', [['Foo', 'Bar']], 
            [{ 'Fu': '1', 'Baz': '2'}, {'Fu': '3', 'Baz': '4'}]])
        self.assertTrue(self.exp.export(input))
        tree = et.parse(self.dir + 'annotation.xml')
        xml = tree.getroot()
        validation = xml.find('Validation')
        self.assertEquals(validation.attrib, {'Type': 'Gold'})
        sensor = validation.find('Sensor')
        self.assertEquals(sensor.attrib, {'Orientation': 'left'})
        meta = sensor.find('Meta')
        self.assertEquals(meta[0].tag, 'Foo')
        self.assertEquals(meta[0].text, 'Bar')
        content = sensor.find('Content')
        self.assertEquals(content[0].tag,     'No1')
        self.assertEquals(content[0][0].tag,  'Fu')
        self.assertEquals(content[0][0].text, '1')
        self.assertEquals(content[0][1].tag,  'Baz')
        self.assertEquals(content[0][1].text, '2')
        self.assertEquals(content[1][0].tag,  'Fu')
        self.assertEquals(content[1][0].text, '3')
        self.assertEquals(content[1][1].tag,  'Baz')
        self.assertEquals(content[1][1].text, '4')

class TestCSVExporter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.dir = self.tmp.makedir('foobar')
        self.exp = CSVExporter()
    def tearDown(self):
        TempDirectory.cleanup_all()
    def test_creation_of_export_file(self):
        filename = 'foobar.csv'
        values = [lib.Sensorsegment._make([0] * 6)]
        status = self.exp.export(values, self.dir+filename)
        self.assertTrue(os.path.isfile(self.dir+filename))
        self.assertTrue(status)
    def test_content_of_export_file(self):
        filename = 'foobar.csv'
        values = [lib.Sensorsegment._make([0] * 6),
                lib.Sensorsegment._make([1] * 6)
                ]
        self.exp.export(values, self.dir+filename, False, False)
        res = self.tmp.read(self.dir+filename)
        ref = b'0,0,0,0,0,0\r\n1,1,1,1,1,1\r\n'
        self.assertEqual(ref, res)
    def test_content_with_header_with_indices(self):
        filename = 'foobar.csv'
        values = [lib.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, True, True)
        res = self.tmp.read(self.dir+filename)
        ref = b'Index,accelX,accelY,accelZ,gyroX,gyroY,gyroZ\r\n1,0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)
    def test_content_with_header_without_indices(self):
        filename = 'foobar.csv'
        values = [lib.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, True, False)
        res = self.tmp.read(self.dir+filename)
        ref = b'accelX,accelY,accelZ,gyroX,gyroY,gyroZ\r\n0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)
    def test_content_without_header_with_indices(self):
        filename = 'foobar.csv'
        values = [lib.Sensorsegment._make([0] * 6)]
        self.exp.export(values, self.dir+filename, False, True)
        res = self.tmp.read(self.dir+filename)
        ref = b'1,0,0,0,0,0,0\r\n'
        self.assertEqual(ref, res)

