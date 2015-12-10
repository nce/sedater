# ./sedater/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 19:56:13

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
            outputDir = cli.args.output_dir
        else:
            outputDir = os.path.dirname(source)

        # Data Import
        importer.crawl(source)
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
        raw = RawConverter(importer.pairedFiles, [sensLeft, sensRight])
        raw.processDatFiles()
        leftRawValidationSegments = raw.initSensors[Orientation.left.name]\
                .normalizedSensorSegments
        rightRawValidationSegments = raw.initSensors[Orientation.right.name]\
                .normalizedSensorSegments
        currentSession = raw.sessionIdentifier
        currentExercise = raw.exerciseIdentifier

        # Text Data Conversion
        txt = TxtConverter(importer.pairedFiles)
        txt.processTxtFiles()

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

        # Txt Data Export
        txtValidation = XMLExporter(location)
        for validationFile in txt.validationData:
            txtValidation.export(validationFile)

