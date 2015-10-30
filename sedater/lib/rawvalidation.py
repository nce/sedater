# ./sedater/lib/rawvalidation.py
# Author:	Ulli Goschler <ulligoschler@gmail.com>
# Created:	Wed, 28.10.2015 - 18:58:05 
# Modified:	Fri, 30.10.2015 - 20:49:51

import os
import csv
import typing

import shared

class RawConverter(object):
	"""
	Convert binary-Sensorfiles to readable CSV

	Conversation is currently limited to '.dat' files, to eliminate 
	the chance of including accidently misplaced files in the directory
	"""

	def __init__(self, filesToConvert, sensors, csvHeaders = False):
		self.filesToConvert   = filesToConvert
		# 'sensors' has to be of type: UninitialziedSensor
		self.availableSensors = sensors
		self.initSensors      = {}
		self.withHeaders      = csvHeaders

		# if not self.leftSensorCalibrationFile or \
		# 		not self.rightSensorCalibrationFile:
		# 	raise AttributeError("No or just one sensor calibration file \
		# 			have been specified. This might introduce a remarkable \
		# 			error in the Validationdata. Proceed with caution.")

	def processDatFiles(self):
		for i in self.availableSensors:
			if not isinstance(i, tuple):
				raise TypeError("Wrong type supplied, should be of type '{}', "
						"is type: '{}'".format(type(shared.UninitializedSensor), type(i)))

			self.initSensors[i.orientation] = Sensor(i.orientation, i.calibrationFile)


		for raw in self.filesToConvert:
			# skip all non '.dat' files
			if '.dat' != os.path.splitext(raw[0].filename)[1]: continue

class Sensor(object):
	"""
	The sensor is used to normalize and convert the Raw Data it recorded

	Every sensor has a individual calibration file which is parsed and later
	used to normalize the recorded raw data.
	"""
	def __init__(self, orientation, calibrationFile):
		self.orientation = orientation
		self._parseCalibrationFile(calibrationFile)

	def _parseCalibrationFile(self, file):
		"""
		Parses a given calibration file

		The format of the CSV should precisly match the given structure:
			AccelerometerX_plusG, AccelerometerY_plusG, AccelerometerZ_plusG
			AccelerometerX_minusG, AccelerometerY_minusG, AccelerometerZ_minusG
			GyroscopeX_restingMean, GyroscopeY_restingMean, GyroscopeZ_restingMean
		Please make sure there are no header lines, whitespaces are stripped
		"""

		with open(file, 'r', newline='') as calibration:
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

