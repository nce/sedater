# ./sedater/sedater/lib/options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Fri, 02.10.2015 - 15:57:02 
# Modified: Fri, 06.11.2015 - 17:54:21

import sys, os
import getopt, logging

class CLIParser(object):
    def __init__(self):
        pass

    def parseForSedater(self, arguments):
        _availableOpts = ['tl:r:o:dvh', ['csv-header',
                'left-calibration=', 'right-calibration=', 'output-dir=',
                'debug', 'verbose', 'help']]
        opts = self._initParse(arguments, _availableOpts)
        self.hasVerbose = False
        self.hasDebug   = False
        self.hasCsvHeader = False
        self.outputDirPrefix = './'

        if not opts:
            self._sedaterUsage()
            return False

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self._sedaterUsage()
                return False
            elif opt in ('-v', '--verbose'):
                self.hasVerbose = True
            elif opt in ('-d', '--debug'):
                self.hasDebug = True
            elif opt in ('-t', '--csv-header'):
                self.hasCsvHeader = True
            elif opt in ('-o', '--output-dir'):
                dir = arg.lstrip().rstrip()
                if os.path.isabs(dir):
                    self.outputDirPrefix = dir + '/'
                else:
                    self.outputDirPrefix += dir + '/'


        self._initLogging()

    def _sedaterUsage(self):
# implement help func
        pass

    def _initLogging(self):
        logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(message)s")
        self.log = logging.getLogger()
        if self.hasDebug:
            self.log.setLevel(logging.DEBUG)
            self.log.debug("Debug logging enabled")
        elif self.hasVerbose:
            self.log.setLevel(logging.INFO)
            self.log.info("Verbose logging enabled")

    def _initParse(self, arguments, optsAvail):
        try:
            opts, args = getopt.getopt(arguments, optsAvail[0], optsAvail[1])
        except getopt.GetoptError as error:
            print(error)
            return False

        return opts
