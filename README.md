# sedater - A Sensor-Validation Converter

Sedater is a **Se**nsor-Vali**dat**ion Convert**er** for inertial based sensor 
systems like the Shimmer R2 or Viconsensors. It converts the Validationdata to 
a more machine processable format and groups individual session data together.

## RawValidation Data Processing

RAW data will be detected based on the filename `.dat` extension.
Matching binary files will be processed as 6-`2B`-sized datasets according to 
the following pattern:

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
		Which makes one dataset to a 12B Array

