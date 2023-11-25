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
```python hht-preprocess.py filePath [--num-splits NUM_SPLITS]```</br></br>

options:</br>
  filePath         The path to the Brainflow file of EEG data to be pre-processed</br>
  --num-splits     The number of segments to split the EEG data into before performing EMD</br></br>

  Once the data is pre-processed, you can now create a model from it. To do this, create a directory that contains subdirectories containing only pre-processed files. For an example, look in [./Test 1 Data/Initial Readings](./Test%201%20Data/Initial%20Readings). You can then run the SVM-CreateModel.py script using this directory as the trainingDataPath option. </br>

  usage:</br>
  ```python SVM-CreateModel.py [-h] [--outputName OUTPUTNAME] [--imfRange IMFRANGE] trainingDataPath```</br></br>

  options:</br>
    -h, --help            show this help message and exit</br>
  --outputName OUTPUTNAME The name of the file to which the SVM model will be saved</br>
    --imfRange IMFRANGE   The range of IMFs to use for creating the model, Ex: '2-5' for inclusive range or '2' for a single IMF or don't include argument for all IMFs</br></br>

  Once the model is created, it will be stored in a .pkl file in the trainingDataPath directory. You can now use this model in Classification. To do this, run the SVM-Classification.py script with the first argument being the location of the .pkl file and the second argument being the Pre-Processed file to classify.</br>

usage:</br>
```SVM-Classification.py [-h] modelPath testFile```</br></br>

options:</br>
  modelPath   The path to the .pkl file containing the model created from SVM-CreateModel.py</br>
  testFile    The path to the Preprocessed EEG file to test for classification</br>

The output will display an array of guesses. One guess for each IMF included in the original model for classification. 

  
