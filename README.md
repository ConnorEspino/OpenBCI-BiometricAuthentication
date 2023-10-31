# OpenBCI-BiometricAuthentication
A study of modern Biometric Authentication techniques and how the environment that participants are recorded in affects the collection and reliability of readings.

# Team
Emerson Konkol</br>
Connor Espino

# Mentors
Dr. Marion Scheepers</br>
Dr. Liljana Babinkostova

# Steps to build
The project runs on python, you'll need it installed on your machine.</br></br>

You'll need to install the dependencies using the python package manager</br>
Simply run the InstallDdependencies.bat file on a Windows machine</br></br>

These scripts are specific to the OpenBCI Ganglion board. Once the dongle is connected to your machine and the Ganglion board is on, you can run the script to collect data.</br></br>

usage:</br>
```python CollectData.py [-h] [--timeout TIMEOUT] [--serial-port SERIAL_PORT] [--session-name SESSION_NAME] [--output-file OUTPUT_FILE] [--run-time RUN_TIME]```</br></br>

options:</br>
  -h, --help            show this help message and exit</br>
  --timeout TIMEOUT     timeout for device discovery or connection</br>
  --serial-port SERIAL_PORT</br>
                        The serial port that the Ganglion dongle is plugged into (Default: COM3)</br>
  --session-name SESSION_NAME</br>
                        The name of the directory to output the file to</br>
  --output-file OUTPUT_FILE</br>
                        The file to output the data to (Will create if it
                        doesn't exist)</br>
  --run-time RUN_TIME   The amount of time to run the brain scan for</br></br>

Once data is collected, you can Preprocess using a Hilbert-Huang Transform. To do this, run the hht-preprocess.py script.</br>

usage:</br>
```python hht-preprocess filePath [--num-splits NUM_SPLITS]```</br></br>

options:</br>
  filePath         The path to the Brainflow file of EEG data to be pre-processed</br>
  --num-splits     The number of segments to split the EEG data into before performing EMD</br>
