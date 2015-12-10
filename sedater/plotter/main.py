# ./sedater/plotter/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 20:25:10

import sys,os
sys.path.insert(0, os.getcwd())

import re

from sedater.plotter.options import CLIParser
from sedater.plotter.plotter import Plotter


if __name__ == "__main__":
    cli = CLIParser()
    if not cli.parseForPlotter(sys.argv[1:]):
        sys.exit(2)

    # to draw a correct Gold Standard overlay, we need to know which 
    # sensor to extract from the Annotationfile
    availableOrientation = ['left', 'right']
    orientationRE = ".*(" + "|".join(availableOrientation) + ").*"

    # only graph the Gold Standard overlay if we have an Annotationfile and 
    # the user hasn't disabled the overlay option
    if cli.args.xml and cli.args.remove_overlay:
        overlay = cli.args.xml
    else:
        overlay = False

    plt = Plotter(
              cli.args.graph
            , overlay
            , cli.args.output_dir
            , cli.args.csv_headers)

    for inputFile in cli.args.plottingSourceFile:
        m = re.match(orientationRE, inputFile)
        if m:
            plt.plot(inputFile, m.group(1))
        else:
            raise AttributeError("Inputfile '{}' has no indication in its "
                    "filename which sensor"
                    " to plot. Sensor identification has to be contained in the"
                    " filename. Available identifications are: {}"
                    .format(inputFile, availableOrientation))

