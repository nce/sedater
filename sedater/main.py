# ./sedater/sedater/main.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Modified: Thu, 10.12.2015 - 15:48:42

import sys, os

from options import CLIParser

from filesystem import Crawler
from rawvalidation import RawConverter
from txtvalidation import TxtConverter
from export import CSVExporter
from export import XMLExporter

from lib.shared import UninitializedSensor
from lib.shared import Orientation

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

