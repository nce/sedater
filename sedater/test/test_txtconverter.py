# ./sedater/test/test_txtconverter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 20:04:24 
# Modified: Tue, 10.11.2015 - 20:21:23

import unittest
from testfixtures import TempDirectory

from sedater.txtvalidation import TxtConverter
from sedater.lib import shared

import sys

class TestTxtConverter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.ref = self.tmp.write('txtvalidation.txt', 
                b"Foo, Bar\nFaz, Baz\n1,2\n3,4")
        self.reffile = shared.Sourcefile._make([self.ref, 'txtvalidation.txt', '', '', ''])
    def tearDown(self):
        TempDirectory.cleanup_all()
    def _test_correct_txt_file(self):
        conv = TxtConverter([])
        print(conv.parseTxtFile(self.reffile), file=sys.stderr)
