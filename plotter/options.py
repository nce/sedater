# ./sedater/plotter/options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Wed, 09.12.2015 - 23:23:25

import sys, os
import getopt, logging

import argparse
class CLIParser(object):

    def parseForPlotter(self, arguments):
        parser = argparse.ArgumentParser(
                description="The plotting utility of the sedater package"
                "\n"
                "\nDocumentation available at:  "
                "http://sedater.readthedocs.org/en/latest/index.html"
                "\nLatest Version available at: "
                "https://github.com/nce/sedater"
                "\n"
                "\nThis tool plots csv files to vector graphics. You can pass an "
                "optional Annotationfile which values will create an overlay of "
                "the plot."
                , formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('plottingSourceFile'
                , nargs='+'
                , help='Rawvalidation CSV file which should be plotted')
        parser.add_argument('-c', '--csv-headers'
                , action='store_true'
                , help='Specify if the plottingSourcefile has a comment head line')
        parser.add_argument('-x', '--xml'
                , default=False
                , help='Provide a XML-Annotationfile from which the Gold Standard '
                    'overlay is generated')
        parser.add_argument('-y', '--remove-overlay'
                , action='store_false'
                , help='Remove the Gold Standard overlay (can only be generated if'
                    ' an Annotationfile is provided with --xml')
        parser.add_argument('-g', '--graph'
                , action='append'
                , help="Specify which graphs to plot. Available options for GRAPH:\n"
                    "For the Acceleration plot:\n"
                    "\t - accelX\n"
                    "\t - accelY\n"
                    "\t - accelZ\n"
                    "For the Gyroscope plot:\n"
                    "\t - gyroX\n"
                    "\t - gyroY\n"
                    "\t - gyroZ\n"
                    "(default: graph all parameters)"
                , choices=[
                      'accelX'
                    , 'accelY'
                    , 'accelZ'
                    , 'gyroX'
                    , 'gyroY'
                    , 'gyroZ'
                ])
        parser.add_argument('-o', '--output-dir'
                , help='directory where the image files will be placed '
                    '(default: same directory as the input file)')

        self.args = parser.parse_args()

        # allow different graphs to be plotted
        defaultAccel = ['accelX', 'accelY', 'accelZ']
        defaultGyro  = ['gyroX', 'gyroY', 'gyroZ']
        # check if customization is wanted
        if self.args.graph:
            plotAccel = []
            plotGyro  = []
            for graph in self.args.graph:
                # check if acceleration graph should be modified
                if graph in defaultAccel:
                    plotAccel.append(graph)
                # check if gyroscope graph should be modified
                if graph in defaultGyro:
                    plotGyro.append(graph)
            if not plotAccel: plotAccel = defaultAccel
            if not plotGyro: plotGyro = defaultGyro
            self.args.graph = [plotAccel, plotGyro]
        else:
            self.args.graph = [defaultAccel, defaultGyro]

        return True

class CLIParserDep(object):
    def __init__(self):
        annotationFile = ''
        isXML = False
        outputDirPrefix = ''

    def parseForPlotter(self, arguments):
        _availableOpts = ['xo:',
                    [
                        'xml'
                      , 'output-dir='
                    ]
                ]
        opts = self._initParse(arguments, _availableOpts)

        if not opts:
            self._plotterUsage()
            return False

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self._plotterUsage()
                return False
            elif opt in ('-x', '--xml'):
                self.isXML = True
            elif opt in ('-o', '--output-dir'):
                dir = arg.lstrip().rstrip()
                if os.path.isabs(dir):
                    self.outputDirPrefix = dir + '/'
                else:
                    self.outputDirPrefix += dir + '/'



    def _plotterUsage(self):
        #TODO: implement help func
        pass

    def _initParse(self, arguments, optsAvail):
        try:
            opts, args = getopt.getopt(arguments, optsAvail[0], optsAvail[1])
        except getopt.GetoptError as error:
            print(error)
            return False

        return opts