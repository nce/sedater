# ./sedater/test/test_txtconverter.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Tue, 10.11.2015 - 20:04:24 
# Modified: Thu, 10.12.2015 - 19:46:09

import unittest
from testfixtures import TempDirectory

from sedater.txtvalidation import TxtConverter
from sedater.lib import shared as lib

import os

class TestTxtConverter(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDirectory()
        self.ref = self.tmp.write('txtvalidation.txt', 
                b"Foo, Bar\nFaz, Baz\n1,2\n3,4")
        self.reffile = lib.Sourcefile._make([
            self.ref
            , 'txtvalidation.txt'
            , ''
            , ''
            , ''
            ])
    def tearDown(self):
        TempDirectory.cleanup_all()
    def test_correct_txt_file(self):
        inFile = self.tmp.write('txtvalidation.txt', 
                b"Foo, Bar\nFaz, Baz\n1,2\n3,4")
        inFile = os.path.dirname(inFile)
        inSource = lib.Sourcefile._make([inFile, 
            'txtvalidation.txt', '', '', ''])
        ref = lib.Validationfile._make([inSource, '', [
                      ['Foo', 'Bar']
                ], [
                      {'Baz': '2', 'Faz': '1'}
                    , {'Baz': '4', 'Faz': '3'}
                    ]
                ])
        conv = TxtConverter([])
        res = conv.parseTxtFile(inSource)
        self.assertEqual(ref,res)
