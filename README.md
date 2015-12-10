# sedater - A Sensor-Validation Converter
[![Build Status](https://travis-ci.org/nce/sedater.svg?branch=master)](https://travis-ci.org/nce/sedater)
[![Documentation Status](https://readthedocs.org/projects/sedater/badge/?version=latest)](http://sedater.readthedocs.org/en/latest/?badge=latest)

**This Project is under development**

Sedater is a **Se**nsor-Vali**dat**ion Convert**er** for motion based sensor 
systems like the Shimmer R2 or Vicon sensors. It converts the ValidationData to 
a more machine processable format and groups individual session data together.

# Basic Functionality

## TextValidation Processing

## RawValidation Data Processing

RAW data will be detected based on the `.dat` filename extension.
Matching binary files will be parsed as a stream of six `2B`-sized tuples 
according to the following pattern:

	Binary File Format
	              1 11
	 12 34 56 78 90 12 Bytes
	,----------------------
	|  |  |  |  |  |  | ...
	`----------------------
	  ^  ^  ^  ^  ^  ^
	  |  |  |  |  |  `- Gyro Z
	  |  |  |  |  `---- Gyro Y
	  |  |  |  `------- Gyro X
	  |  |  `---------- Accel Z
	  |  `------------- Accel Y
	  `---------------- Accel X
	  With each single datum as uint16 (unsigned short)
		Which composes one dataset to an 12B Array

## Usage Examples

# Install
Cloning the repository should be enough
## Requirements
The tool has the following python [requirements](requirements.txt) 
which are easily resolved by executing:
```
pip install -r requirements.txt
```
The heaviest dependencies are `matplotlib` and `numpy` which are 
exclusivly used for the optional [plotting](#Plotting) of the 
Rawvalidation files. The main functionality is given without them.

If you choose to not rely on plotting simply don't install them by 
commenting them out in the [dependency file](requirements.txt) 
(prefix with: `#`).
## Easy Install

## Python Version
The testcases are automatically running against multiple python versions:
- Python3.5.0
- Python3.4.2
- Python3.3.5

Rendering a green [build status](https://travis-ci.org/nce/sedater) 
is therefore a good indicator that the listed python versions are
likely to be working.

`Python2.7.10 & Python3.2` are currently not supported. 
This might change in the future.

# Developer Documentation
The code is annotated by [docstrings](https://en.wikipedia.org/wiki/Docstring), 
which are automatically parsed by [Sphinx](http://sphinx-doc.org/) and therefore 
online available at [readthedocs.org](readthedocs.org):

Refer to the [Developer documentation](http://sedater.readthedocs.org/en/latest/)
for implementation specific details.

# Testing
Run `nosetests` in the code directory (`sedater`). 

All tests are automatcially executed by [Travis CI](travis-ci.org)
on each code update.
