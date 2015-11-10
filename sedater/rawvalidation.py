# ./sedater/rawvalidation.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Wed, 28.10.2015 - 18:58:05 
# Modified: Tue, 10.11.2015 - 13:57:56

import os
import csv
import typing
import struct

from sedater.lib import shared

class RawConverter(object):
    """
    Convert binary-Sensorfiles to readable CSV

    Note: Conversation is currently limited to '.dat' files, to eliminate 
    the chance of processing accidently misplaced files 
    """

    def __init__(self, filesToConvert, sensors):
        """
        :param filesToConvert: list (array) of raw files which 
                should be converted
        :type filesToConvert: list of tuples of 
                :class:`sedater.lib.shared.Sourcefile`
        :param sensors: the uninitialized sensors
        :type sensors: list of :class:`sedater.lib.shared.UninitializedSensor`
        """
        self.filesToConvert   = filesToConvert
        self.availableSensors = sensors
        # initialized sensors
        self.initSensors      = {}

        # if not self.leftSensorCalibrationFile or \
        #       not self.rightSensorCalibrationFile:
        #   raise AttributeError("No or just one sensor calibration file \
        #           have been specified. This might introduce a remarkable \
        #           error in the Validationdata. Proceed with caution.")

    def processDatFiles(self):
        for i in self.availableSensors:
            if not isinstance(i, tuple):
                raise TypeError("Wrong type supplied, should be of type '{}', "
                        "is type: '{}'".format(type(shared.UninitializedSensor), type(i)))

            self.initSensors[i.orientation.name] = Sensor(
                    i.orientation, i.calibrationFile)

        for rawPair in self.filesToConvert:
            if not isinstance(rawPair, tuple):
                raise TypeError("Wrong type supplied, should be of type '{}', "
                        "is type: '{}'".format('tuple',type(rawPair)))
            # parse all files associated with current pair
            for i in range(len(rawPair)):
                # skip all non '.dat' files
                if '.dat' != os.path.splitext(rawPair[i].filename)[1]: continue
                self.initSensors[rawPair[i].orientation.name].parseAndNormalizeRawFile(
                        rawPair[i].path + "/" + rawPair[i].filename)

class Sensor(object):
    """
    The sensor is used to normalize and convert the raw data it recorded

    Every sensor has a individual calibration file which is parsed and later
    used to normalize the recorded raw data.

    """
    def __init__(self, orientation, calibrationFile):
        self.calibration = ''
        self.orientation = orientation
        self._parseCalibrationFile(calibrationFile)
        self.normalizedSensorSegments = []

    def _parseCalibrationFile(self, file):
        """
        Parses a given calibration file

        The format of the CSV should precisly match the given structure:
            AccelerometerX_plusG, AccelerometerY_plusG, AccelerometerZ_plusG
            AccelerometerX_minusG, AccelerometerY_minusG, AccelerometerZ_minusG
            GyroscopeX_restingMean, GyroscopeY_restingMean, GyroscopeZ_restingMean

        Please make sure there are no header lines; whitespaces are stripped

        :param file: Path to the sensor calibration file
        :type file: str

        """

        with open(file, 'r') as calibration:
            # open csv calibration file
            csvList = list(csv.reader(calibration))
            # parse all csv entries into a flat list of floats
            try:
                tmp = list(map(float, [val for sublist in csvList for val in sublist]))
            except ValueError:
                raise ValueError("The given calibration file '{}' contains a "
                        "value which is not convertable to a number, make sure "
                        "the file only consists of comma seperated numbers (int "
                        "or float). Refer to the help message for further "
                        "assistance".format(file))
            try:
                self.calibration = shared.SensorCalibration._make(tmp)
            except TypeError as e:
                raise TypeError("The given calibration file '{}' doesn't adhere"
                        " to the requested format specified in the help "
                        "message. Please recheck the syntax of the file. "
                        "The detailed error was: {}".format(file, str(e)))

    def parseAndNormalizeRawFile(self, file):
        """
        Converts the binary in 12B-datasets (ushort) and normalizes the data 

        Conversion is done in sets of 12B, each 2B tuple as 16bit unsigned 
        integers (nativ endian) and stored as one complete sensor segment.
        The Sensorsegments are then normalized (with the sensor
        calibration data)

        :param file: path to the raw file
        :type file: str
        """

        with open(file, 'rb') as rawFile:
            structFmt = '=HHHHHH'   # native endian; 6x unsigned 16bit integer
            structLen = struct.calcsize(structFmt) # calculate struct size

            while True:
                data = rawFile.read(structLen) # read structLen bytes from binary
                if not data: break

                dataset = struct.unpack(structFmt, data) # Unpack binary data
                rawSegment = shared.Sensorsegment._make(list(dataset))
                self.normalizedSensorSegments.append(self._normalizeRawSegment(rawSegment))
            # TODO: return as Segment maybe?

    def _normalizeRawSegment(self, rawSegment):
        """
        Normalizes the sensor data by applying the individual calibration file 
        for each sensor.

        The normalization process is done by the following mathematical algorithm:

        *Acceleration parameters:*
            (Rawvalue - ((plusG - minusG)/2)) / ((plusG - minusG)/2)
        *Gyrometer parameters:*
            (Rawvalue - restingMean) / 2.731
        with:
            - Rawvalue    := the value given in the raw data file
            - plusG       := the direction specific plus value of the calibration file
            - minusG      := the direction specific minus value of the calibration file
            - restingMean := the direction specific reastingMean value of the calibration file

        :param rawSegment: the converted raw sensor dataset, which should be normalized
        :type rawSegment: :class:`sedater.lib.shared.Sensorsegment`
        :return: the normalized Segment
        :rtype: :class:`sedater.lib.shared.Sensorsegment`

        """
        normSegment = [None] * 6

        try:
            for i in range(3):
                normSegment[i] = (rawSegment[i] - ((self.calibration[i] + self.calibration[3 + i])/2)) \
                        / ((self.calibration[i] - self.calibration[3 + i])/2)
                normSegment[i + 3] = (rawSegment[i + 3] - self.calibration[i + 6])/2.731
        except Exception as e:
            raise e

        return shared.Sensorsegment._make(normSegment)


