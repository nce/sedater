# ./sedater/test/test_rawconverter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Wed, 28.10.2015 - 19:34:06 
# Modified: Sun, 08.11.2015 - 01:12:59

import unittest
import os
from testfixtures import TempDirectory

from sedater.rawvalidation import Sensor, RawConverter
from sedater.lib import shared

class TestSensor(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.calibration = self.tmp.write('calibration.csv', 
                b"1.1,2,3\n4,5.5,6\n7,8,9.9")
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
    def test_normalizing_return(self):
        sens = Sensor(shared.Orientation(1).name, self.calibration)
        foo = shared.Sensorsegment._make([1,2,3,4,5,6])
        bar = sens._normalizeRawSegment(foo)
        self.assertIsInstance(foo, type(foo))
    def test_normalizing(self):
        # eGaiT_database/P100_E4_left.dat
        # A917.csv
        calibrationLeft = self.tmp.write('left.csv', 
                b"2367.1,2274.9,2271.2\n1871.8,1795.5,1753.1\n1785.8,1684.4,1855.4")
        # A6DF.csv
        calibrationRight = self.tmp.write('right.csv', 
                b"2403.5,2254.8,2266.1\n1899.7,1769.3,1773.2\n1835.2, 1709.6,1860.5")
        # first 12 bytes of P100_E4_left.dat
        rawRight = shared.Sensorsegment._make([1762, 2155, 2024, 1849, 1713, 1864])
        # first 12 bytes of P100_E4_right.dat
        rawLeft = shared.Sensorsegment._make([1797, 2109, 2013, 1777, 1688, 1850])
        # expected left end results
        resL = shared.Sensorsegment._make([-1.3020391681808998,0.30788485607008736,0.003281219841729923,-3.2222629073599247,1.318198462101761,-1.9772976931527246])
        # expected right end results
        resR = shared.Sensorsegment._make([-1.5466454942437473,0.5888774459320278,0.01765063907486269,5.053094104723528,1.2449652142072833,1.2815818381545223])
        sensL = Sensor(shared.Orientation.left, calibrationLeft)
        sensR = Sensor(shared.Orientation.right, calibrationRight)
        bar = sensL._normalizeRawSegment(rawLeft)
        foo = sensR._normalizeRawSegment(rawRight)
        self.assertEqual(resL, bar)
        self.assertEqual(resR, foo)

class TestRawConverter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        foo = self.tmp.write('foo.csv', b"1,2,3\n4,5,6\n7,8,9")
        bar = self.tmp.write('bar.csv', b"9,8,7\n6,5,4\n3,2,1")
        self.rawleft = self.tmp.write('P100_E4_left.dat', 
                b'\x05\x07\x3d\x08\xdd\x07\xf1\x06\x98\x06\x3a\x07')
        self.rawright = self.tmp.write('P100_E4_right.dat', 
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
    def test_dat_file_processing(self):
        first = shared.Sourcefile._make(
                [os.path.dirname(self.rawleft), 'P100_E4_left.dat', '01', '01', shared.Orientation(1)])
        second = shared.Sourcefile._make(
                [os.path.dirname(self.rawright), 'P100_E4_right.dat', '01', '01', shared.Orientation(2)])
        conv = RawConverter(
                [(first, second)], [self.foo, self.bar])
        conv.processDatFiles()
        #TODO: continue
