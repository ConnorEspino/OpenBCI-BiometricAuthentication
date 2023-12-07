# OpenBCI-BiometricAuthentication

A study of modern Biometric Authentication techniques and how the environment that participants are recorded in affects the collection and reliability of readings.

# Team

Connor Espino

Emerson Konkol



# Mentors

Dr. Marion Scheepers
Dr. Liljana Babinkostova



# How to Use

The project runs on python, you'll need it installed on your machine

You'll need to install the dependencies using pip, the python package manager.
Simply run the InstallDdependencies.bat file on a Windows machine.



These scripts are specific to the OpenBCI Ganglion board and only utilizes one electrode. Turn the other channels on in the CollectData.py script. Once the dongle is connected to your machine and the Ganglion board is on, you can run the script to collect data.

usage:
`python CollectData.py [--timeout TIMEOUT] [--serialPort SERIAL_PORT] [--sessionName SESSION_NAME] [--outputFile OUTPUT_FILE] [--runTime RUN_TIME]`

options:

- `--timeout` (type: `int`, required: `False`, default: `0`): Timeout for device discovery or connection. 
- `--serialPort` (type: `str`, required: `False`, default: `"COM3"`): The serial port that the Ganglion dongle is plugged into. 
- `--sessionName` (type: `str`, required: `False`, default: `''`): The name of the directory to output the file to. 
- `--outputFile` (type: `str`, required: `False`, default: `''`): The file to output the data to (Will create if it doesn't exist). 
- `--runTime` (type: `int`, required: `False`, default: `15`): The amount of time to run the brain scan for.





Once data is collected, you can Pre-process to find Sectral Entropy using a Hilbert-Huang Transform. To do this, run the hht-preprocess.py script with `path` describing a directory containing one or multiple EEG readings. The preprocessing will be done to all files in that directory automatically.

usage:
`python hht-preprocess.py path [--num-splits NUM_SPLITS] [--no-photos NO_PHOTOS]`

options:

- `path` (type: `str`, required): The path to the directory containing EEG data to be pre-processed. 
- `--num-splits` (type: `int`, required: `False`, default: `0`): The number of segments to split the EEG data into before performing Empirical Mode Decomposition (EMD). 
- `--no-photos` (type: `bool`, required: `False`, default: `False`): Set to `True` to not save graphs of each split's EMD. Defaults to `False`.





Once the data is pre-processed, you can now create a model from it. To do this, create a directory that contains labeled subdirectories containing **only** pre-processed (.npy) files. For an example, look in [./EEG Data/Initial](./EEG%20Data/Initial). You can then run the SVM-CreateModel.py script using this directory as the trainingDataPath option. 

usage:

`python SVM-CreateModel.py trainingDataPath [--outputName OUTPUTNAME] [--imfRange IMFRANGE] [--cValue CVALUE]`

options:

- `trainingDataPath` (type: `str`, required): A directory containing one or more labeled directories of pre-processed EEG readings. The SVM model will be trained on this data. 
- `--outputName` (type: `str`, required: `False`, default: `'SVM-Model'`): The name of the file to which the SVM model will be saved. 
- `--imfRange` (type: `str`, required: `False`, default: `'-1'`): The range of Intrinsic Mode Functions (IMFs) to use for creating the model. Example: `'2-5'` for an inclusive range, `'2'` for a single IMF, or don't include the argument for all IMFs. 
- `--cValue` (type: `float`, required: `False`, default: `1.0`): SVM regularization parameter.</br>





Once the model is created, it will be stored in a .pkl file in the trainingDataPath directory. You can now use this model in Classification. To do this, run the SVM-Classification.py script with the first argument being the path of the .pkl file and the second argument being a directory that contains labeled subdirectories containing **only** pre-processed (.npy) files.

usage:
`SVM-Classification.py modelPath testFile`

options:

- `modelPath` (type: `str`, required): The path to the `.pkl` file containing the model created from `SVM-CreateModel.py`. 
- `testData` (type: `str`, required): The path to the directory containing labeled directories of pre-processed EEG data to test for classification.tions:
  

# Future Work

The classification algorithm or SVM tuning is most likely incorrect. 

Input: `python SVM-Classification.py './EEG Data/Initial/SVM-Model-C10.0.pkl' './EEG Data/Initial'`

Output: `Model Accuracy: 0.25`



I'm fairly confident that Pre-Processing is correct, but the Hilbert transform returns an array with complex numbers which the SVM doesn't like. Dealing with this could take different forms, I didn't have time to research which solution would be best, so I just got the SVM to stop throwing errors using this line in `SVM-CreateModel.py`:

`SpecEntrReal = [np.real(entry), np.imag(entry)]`

 
