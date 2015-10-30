# ./sedater/test/test_rawconverter.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Wed, 28.10.2015 - 19:34:06 
# Modified:	Fri, 30.10.2015 - 20:54:57

import unittest
from testfixtures import TempDirectory

from lib import rawvalidation
from lib import shared

class TestSensor(unittest.TestCase):
	def setUp(self):
		self.tmp = TempDirectory()
	def tearDown(self):
		TempDirectory.cleanup_all()
	def test_missing_sensor_calibration_values(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,9")
		self.assertRaises(TypeError, rawvalidation.Sensor, 
				shared.Orientation.left, calibration)
	def test_invalid_sensor_calibration_values(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,2,3\n4,foobar,6\n7,8,9.9")
		self.assertRaises(ValueError, rawvalidation.Sensor, 
				shared.Orientation.left, calibration)
	def test_sensor_calibration_file(self):
		calibration = self.tmp.write('calibration.csv', 
				b"1.1,2,3\n4,5.5,6\n7,8,9.9")
		sens = rawvalidation.Sensor(shared.Orientation.left, calibration)
		self.assertEquals(sens.calibration[1], 2)
		self.assertEquals(sens.calibration[4], 5.5)
		self.assertEquals(sens.calibration[8], 9.9)

class TestRawConverter(unittest.TestCase):
	def setUp(self):
		self.tmp = TempDirectory()
		self.foo = self.tmp.write('foo.csv', b"1,2,3\n4,5,6\n7,8,9")
		self.bar = self.tmp.write('bar.csv', b"9,8,7\n6,5,4\n3,2,1")
	def tearDown(self):
		TempDirectory.cleanup_all()

	def test_sensor_setup(self):
		foo = shared.UninitializedSensor._make([shared.Orientation(1), self.foo])
		bar = shared.UninitializedSensor._make([shared.Orientation(2), self.bar])
		conv = rawvalidation.RawConverter([], [foo, bar])
		conv.processDatFiles()
		self.assertIsInstance(conv.initSensors[
			shared.Orientation(1)], rawvalidation.Sensor)
		self.assertIsInstance(conv.initSensors[
			shared.Orientation(2)], rawvalidation.Sensor)
		self.assertEquals(conv.initSensors[
			shared.Orientation(1)].orientation, shared.Orientation(1))
		self.assertEquals(conv.initSensors[
			shared.Orientation(2)].orientation, shared.Orientation(2))
