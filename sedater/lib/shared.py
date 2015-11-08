# ./sedater/lib/shared.py
# Author:   Ulli Goschler <ulligoschler@gmail.com>
# Created:  Thu, 29.10.2015 - 19:05:20 
# Modified: Sat, 07.11.2015 - 18:20:54

from enum import Enum
from typing import NamedTuple

class Orientation(Enum):
    """
    Define the orientation a sensor can have

    While this is currently only attributable to a left or right (foot), this 
    might be expandable in the future.
    You might consider the 'orientation' as kind of a sensor id.
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

UninitializedSensor = NamedTuple('UninitializedSensor', [
          ('orientation', Orientation)
        , ('calibrationFile', str)
        ])

SensorCalibration = NamedTuple('SensorCalibration', [
        ('accelX_plusG', float),('accelY_plusG', float),('accelZ_plusG', float),
        ('accelX_minusG', float),('accelY_minusG', float),('accelZ_minusG', float),
        ('gyroX_restMean', float),('gyroY_restMean', float),('gyroZ_restMean', float),
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
A sensor segment
"""
