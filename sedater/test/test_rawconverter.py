# ./sedater/test/test_rawconverter.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Wed, 28.10.2015 - 19:34:06 
# Modified:	Fri, 06.11.2015 - 17:11:54

import unittest
import os
from testfixtures import TempDirectory

from sedater.rawvalidation import Sensor, RawConverter
from sedater.lib import shared

class TestSensor(unittest.TestCase):
	def setUp(self):
		self.tmp = TempDirectory()
	def tearDown(self):
		TempDirectory.cleanup_all()
	def test_missing_sensor_calibration_values(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,9")
		self.assertRaises(TypeError, Sensor, 
				shared.Orientation.left, calibration)
	def test_invalid_sensor_calibration_values(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,2,3\n4,foobar,6\n7,8,9.9")
		self.assertRaises(ValueError, Sensor, 
				shared.Orientation.left, calibration)
	def test_sensor_calibration_file(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,2,3\n4,5.5,6\n7,8,9.9")
		sens = Sensor(shared.Orientation.left, calibration)
		self.assertEquals(sens.calibration[1], 2)
		self.assertEquals(sens.calibration[4], 5.5)
		self.assertEquals(sens.calibration[8], 9.9)

class TestRawConverter(unittest.TestCase):
	def setUp(self):
		self.tmp = TempDirectory()
		foo = self.tmp.write('foo.csv', b"1,2,3\n4,5,6\n7,8,9")
		bar = self.tmp.write('bar.csv', b"9,8,7\n6,5,4\n3,2,1")
		self.rawleft = self.tmp.write('P01_E1_left.dat', 
				b'\x05\x07\x3d\x08\xdd\x07\xf1\x06\x98\x06\x3a\x07')
		self.rawright = self.tmp.write('P01_E1_right.dat', 
				b'\xe2\x06\x6b\x08\xe8\x07\x39\x07\xb1\x06\x48\x07')
		self.foo = shared.UninitializedSensor._make([shared.Orientation(1), foo])
		self.bar = shared.UninitializedSensor._make([shared.Orientation(2), bar])
	def tearDown(self):
		TempDirectory.cleanup_all()

	def test_sensor_setup(self):
		conv = RawConverter([], [self.foo, self.bar])
		conv.processDatFiles()
		self.assertIsInstance(conv.initSensors[
			shared.Orientation(1).name], Sensor)
		self.assertIsInstance(conv.initSensors[
			shared.Orientation(2).name], Sensor)
		self.assertEquals(conv.initSensors[
			shared.Orientation(1).name].orientation, shared.Orientation(1))
		self.assertEquals(conv.initSensors[
			shared.Orientation(2).name].orientation, shared.Orientation(2))
	def test_invalid_filesToConvert_parameter(self):
		conv = RawConverter(
				[self.rawleft, self.rawright], [self.foo, self.bar])
		self.assertRaises(TypeError, conv.processDatFiles)
	def aest_dat_file_processing(self):
		first = shared.Sourcefile._make(
				[os.path.dirname(self.rawleft), 'P01_E1_left.dat', '01', '01', shared.Orientation(1)])
		second = shared.Sourcefile._make(
				[os.path.dirname(self.rawright), 'P01_E1_right.dat', '01', '01', shared.Orientation(2)])
		conv = RawConverter(
				[(first, second)], [self.foo, self.bar])
		conv.processDatFiles()
		#TODO: continue
