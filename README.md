# sedater - A Sensor-Validation Converter

Sedater is a **Se**nsor-Vali**dat**ion Convert**er** for inertial based sensor 
systems like the Shimmer R2 or Vicon sensors. It converts the ValidationData to 
a more machine processable format and groups individual session data together.

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

# Install
Just clone the repository and install the dependencies:
```
pip install -r requirements.txt
```

## Dependencies
- Python3.5

# Testing
Run `nosetests` in the code directory
