# ./sedater/lib/shared.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Thu, 29.10.2015 - 19:05:20 
# Modified: Sat, 05.12.2015 - 17:57:52

from enum import Enum
from typing import NamedTuple

class Orientation(Enum):
    """
    Define the orientation a sensor has. Where the orientation is 
    kind of synonymous to an sensor ID.

    While this is currently only attributable to ``left`` or ``right`` 
    (originating from foot sensors), this 
    might be expandable in the future.

    The ``name`` should always match its 'identification' on the 
    corresponding filename. The assigned values are currently arbitrary.
    """
    left  = 1
    right = 2

Sourcefile = NamedTuple('Sourcefile', [
          ('path', str)
        , ('filename', str)
        , ('session', str)
        , ('exercise', int)
        , ('orientation', Orientation)
        ])
"""Files found by the filesystem crawler and ready for 
further processing

:param path: full path to the file
:param filename: filename with extension of the file
:param session: session ID of the file
:param exercise: the exercise ID of the file
:param orientation: the orientation (ID) of the associated sensor
:type path: str
:type filename: str
:type session: str
:type exercise: int
:type orientation: :class:`Orientation <sedater.lib.shared.Orientation>`

"""

UninitializedSensor = NamedTuple('UninitializedSensor', [
          ('orientation', Orientation)
        , ('calibrationFile', str)
        ])
"""Uninitialized sensors are simple objects, ready for calibration

To become initialized sensors, the sensors need to be calibrated by
:class:`Sensor <sedater.rawvalidation.Sensor>`. For the calibration
process, the sensors need a (specific) calibration file 
(usually provided by command-line)

:param orientation: the orientation (ID) of the sensor
:type orientation: :class:`Orientation <sedater.lib.shared.Orientation>`
:param str calibrationFile: fullpath to the sensor specific calibration file
"""

SensorCalibration = NamedTuple('SensorCalibration', [
          ('accelX_plusG', float)
        , ('accelY_plusG', float)
        , ('accelZ_plusG', float)

        , ('accelX_minusG', float)
        , ('accelY_minusG', float)
        , ('accelZ_minusG', float)

        , ('gyroX_restMean', float)
        , ('gyroY_restMean', float)
        , ('gyroZ_restMean', float)
        ])

Sensorsegment = NamedTuple('Sensorsegment', [
          ('accelX', float)
        , ('accelY', float)
        , ('accelZ', float)
        , ('gyroX',  float)
        , ('gyroY',  float)
        , ('gyroZ',  float)
        ])
"""
The sensor segment is storing an atomic movement, recorded by a sensor

The segment might by normalized or not. It's usually extracted by the
:class:`RawConverter <sedater.rawvalidation.RawConverter>`.

:param float accelX: acceleration on the X-axis
:param float accelY: acceleration on the Y-axis
:param float accelZ: acceleration on the Z-axis
:param float gyroX: rotation on the X-axis
:param float gyroY: rotation on the Y-axis
:param float gyroZ: rotation on the Z-axis
"""

def indentXML(elem, level=0):
	"""
	Helper Method to provide indention in .xml files
	from: http://effbot.org/zone/element-lib.htm#prettyprint
	"""
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

