# OpenBCI-BiometricAuthentication
A study of modern Biometric Authentication techniques and how the environment that participants are recorded in affects the collection and reliability of readings.

# Team
Emerson Konkol
Connor Espino

# Mentors
Dr. Marion Scheepers
Dr. Liljana Babinkostova

# Steps to build
The project runs on python, you'll need it installed on your machine.

You'll need to install the dependencies using the python package manager
```pip install brainflow```

This script is specific to the OpenBCI Ganglion board. Once the dongle is connected to your machine and the Ganglion board is on, you can run the script to collect data.

usage:
```python Test.py [-h] [--timeout TIMEOUT] [--serial-port SERIAL_PORT] [--session-name SESSION_NAME] [--output-file OUTPUT_FILE] [--run-time RUN_TIME]```

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     timeout for device discovery or connection
  --serial-port SERIAL_PORT
                        The serial port that the Ganglion dongle is plugged into (Default: COM3)
  --session-name SESSION_NAME
                        The name of the directory to output the file to
  --output-file OUTPUT_FILE
                        The file to output the data to (Will create if it
                        doesn't exist)
  --run-time RUN_TIME   The amount of time to run the brain scan for