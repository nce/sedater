# ./sedater/sedater/test/test_filesystem.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Sun, 11.10.2015 - 20:21:18 
# Modified: Fri, 06.11.2015 - 17:53:03

import unittest
from testfixtures import TempDirectory
from stat import *
import os

from sedater.filesystem import Crawler
from sedater.lib.shared import Sourcefile

class TestFilesystemCrawler(unittest.TestCase):
    filename = 'foobar.txt'
    dirname  = 'barfoo/'
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
        crawler = Crawler()
        ref = Sourcefile._make(
                ['', '', expected[0], expected[1], expected[2]])
        res = crawler._parseFileName(f)
        self.assertEquals(ref[2], res[2])
        self.assertEquals(ref[3], res[3])
        self.assertEquals(ref[4], res[4])

    def test_input_type(self):
        crawler = Crawler()
        self.assertRaises(AttributeError, crawler.crawl, '404')

    def test_input_file_permissions(self):
        os.chmod(self.file, 0)
        crawler = Crawler()
        self.assertRaises(PermissionError, crawler._parseFileName, self.file)

    def test_empty_pairing(self):
        crawler = Crawler()
        self.assertRaises(ValueError, crawler.pair)

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

    def test_correct_pairing(self):
        left  = self.tmp.write(self.dir + 'P01_E2_left.txt', b'')
        right = self.tmp.write(self.dir + 'P01_E2_right.txt', b'')
        crawler = Crawler()
        crawler.crawl(self.dir)
        crawler.pair()
        self.assertEquals(crawler.pairedFiles[0][0].filename, 'P01_E2_left.txt')
        self.assertEquals(crawler.pairedFiles[0][1].filename, 'P01_E2_right.txt')

    def test_one_partner_missing_pairing(self):
        left = self.tmp.write(self.dir + 'P01_E2_left.txt', b'')
        crawler = Crawler()
        crawler.crawl(self.dir)
        try:
            crawler.pair()
        except ValueError:
            pass
        self.assertEquals(crawler.pairedFiles[0][0].filename, 
                crawler.pairedFiles[0][1].filename)

