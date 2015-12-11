# ./sedater/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Fri, 11.12.2015 - 01:23:01

import sys, os
sys.path.insert(0, os.getcwd())

from sedater.options import CLIParser

from sedater.filesystem import Crawler
from sedater.rawvalidation import RawConverter
from sedater.txtvalidation import TxtConverter
from sedater.export import CSVExporter
from sedater.export import XMLExporter

from sedater.lib.shared import UninitializedSensor
from sedater.lib.shared import Orientation

if __name__ == "__main__":
    cli = CLIParser()
    if not cli.parseForSedater(sys.argv[1:]):
        sys.exit(2)

    importer = Crawler()
    for source in cli.args.inputSource:
        # Data Export preparations
        if cli.args.output_dir:
            outputDir = cli.args.output_dir + '/'
        else:
            outputDir = os.path.dirname(source) + '/'

        # Data Import
        importer.crawl(source)

    # All input sources are crawled
    # now pair all files together
    importer.pair()

    # Raw Data Conversion and Normalization
    sensLeft = UninitializedSensor._make([
              Orientation.left
            , cli.args.left_calibration
            ])
    sensRight = UninitializedSensor._make([
              Orientation.right
            , cli.args.right_calibration
            ])
    for pair in importer.pairedFiles:
        # skip all non .dat files
        # TODO: this is ugly.
        # cleanup
        if '.dat' != os.path.splitext(pair[0].filename)[1]: continue
        raw = RawConverter([pair], [sensLeft, sensRight])
        raw.processDatFiles()
        leftRawValidationSegments = raw.initSensors[Orientation.left.name]\
                .normalizedSensorSegments
        rightRawValidationSegments = raw.initSensors[Orientation.right.name]\
                .normalizedSensorSegments
        currentSession = raw.sessionIdentifier
        currentExercise = raw.exerciseIdentifier


        # Raw Data Export
        rawValidation = CSVExporter()
        location = rawValidation.prepareOutputDir(
                        outputDir
                        , currentSession
                        , currentExercise)
        rawValidation.export(
                leftRawValidationSegments
                , location + 'leftSensorNormalized.csv'
                , cli.args.csv_headers)
        rawValidation.export(
                rightRawValidationSegments
                , location + 'rightSensorNormalized.csv'
                , cli.args.csv_headers)

    # Text Data Conversion
    txt = TxtConverter(importer.pairedFiles)
    txt.processTxtFiles()

    # Txt Data Export
    txtValidation = XMLExporter(outputDir)
    for validationFile in txt.validationData:
        txtValidation.export(validationFile)

