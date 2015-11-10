# ./sedater/test/test_txtconverter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 20:04:24 
# Modified: Tue, 10.11.2015 - 23:44:24

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
    def test_correct_txt_file(self):
        reffile = self.tmp.write('txtvalidation.txt', 
                b"Foo, Bar\nFaz, Baz\n1,2\n3,4")
        refsource = shared.Sourcefile._make([reffile, 
            'txtvalidation.txt', '', '', ''])
        ref = ([['Foo', ' Bar']], [{' Baz': '2', 'Faz': '1'}, 
            {' Baz': '4', 'Faz': '3'}])
        conv = TxtConverter([])
        res = conv.parseTxtFile(refsource)
        self.assertEqual(ref,res)
