# ./sedater/plotter/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Wed, 09.12.2015 - 23:20:13

from options import CLIParser
from plotter import Plotter

import sys

if __name__ == "__main__":
    cli = CLIParser()
    if not cli.parseForPlotter(sys.argv[1:]):
        sys.exit(2)

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
        plt.plot(inputFile)

