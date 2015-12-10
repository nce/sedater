# ./sedater/plotter/options.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 19:04:41

import argparse

class CLIParser(object):
    """
    Parses the commandline arguments.

    Refer to the source code for available commandline options, or 
    run ``plotter -h``.
    """

    def parseForPlotter(self, arguments):
        """
        :param list arguments: List of commandline arguments
        :return: Indicator of successful cli parsing
        :rtype: bool
        """
        parser = argparse.ArgumentParser(
                description="The plotting utility of the sedater package"
                "\n"
                "\nDocumentation available at:  "
                "http://sedater.readthedocs.org"
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

        self.args = parser.parse_args(arguments)

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
