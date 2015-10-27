# ./sedater/sedater/test/test_filesystem.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Sun, 11.10.2015 - 20:21:18 
# Modified:	Tue, 27.10.2015 - 18:51:37

import unittest
from testfixtures import TempDirectory
from stat import *
import os

from lib import filesystem

class TestFilesystemCrawler(unittest.TestCase):
	filename = 'foobar.txt'
	dirname  = 'barfoo'
	file = ''
	dir = ''

	def setUp(self):
		self.tmp = TempDirectory()
		self.dir = self.tmp.makedir(self.dirname)
		self.file = self.tmp.write(self.filename, b'foo')
	def tearDown(self):
		TempDirectory.cleanup_all()
	def dummyFile(self, filename, expected):
		f = self.tmp.write(filename, b'EOF')
		crawler = filesystem.Crawler(f)
		ref = filesystem.Fileattributes._make(
				['', '', expected[0], expected[1], expected[2]])
		res = crawler._parseFileName(f)
		self.assertEquals(ref[2], res[2])
		self.assertEquals(ref[3], res[3])
		self.assertEquals(ref[4], res[4])

	def test_input_type(self):
		crawler = filesystem.Crawler(self.file)
		self.assertEquals(crawler.inputSourceIsFile, True)
		self.assertEquals(crawler.inputSourceIsDir, False)
		self.assertRaises(AttributeError, filesystem.Crawler, '404')

	def test_input_file_permissions(self):
		os.chmod(self.file, 0)
		crawler = filesystem.Crawler(self.file)
		self.assertRaises(PermissionError, crawler._parseFileName, self.file)

	# Pxx_Eyy_right|left (eGaitDatabase)
	def test_S_E_O_format(self):
		self.dummyFile('P01_E2_right.dat', ['01', '2', 'right'])

	# GAxxEyy_right|left (eGaitDatabase3/Controls)
	def test_SE_O_format(self):
		self.dummyFile('GA112030E3_left.txt', ['112030', '3', 'left'])

	# PxxEyy_right|left (eGaitDatabase3/Geriatrics)
	def test_SE_O_format2(self):
		self.dummyFile('P50E6_left.txt', ['50', '6', 'left'])

	# PatxxWald(left|right)Foot_Sensor_Date (eGaitDatabase3/GeriatricsGSTD/4MW)
	def test_SO_format(self):
		self.dummyFile('Pat1WaldrightFoot_1eea_20140325133006.dat', 
				['1Wald', '', 'right'])

	# GAxx_(Left|Right)Foot_Sensor_Date (eGaitDatabase3/Controls/4MW)
	def test_SO_format2(self):
		self.dummyFile('GA214026LeftFoot_1eea_20140428110132.dat', 
				['214026', '', 'left'])

	# GAstdxx_(Left|Right)Foot_Sensor_Date (eGaitDatabase3/Controls/4MW)
	def test_SO_format3(self):
		self.dummyFile('GAstd45jwRightFoot_1d68_20140506123332.dat', 
				['45jw', '', 'right'])



