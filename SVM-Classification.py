import joblib
import argparse
import numpy as np
from pathlib import Path
from sklearn.svm import SVC
from brainflow.data_filter import DataFilter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('modelPath', type=str, help='The path to the .pkl file containing the model created from SVM-CreateModel.py')
    parser.add_argument('testFile', type=str, help='The path to the Preprocessed EEG file to test for classification')
    args = parser.parse_args()

    modelPath = Path(args.modelPath)
    testFilePath = Path(args.testFile)

    funData = joblib.load(modelPath)
    smallestIMF = funData[0]
    imfRange = funData[1]
    model = funData[2]
    classDict = funData[3]
    reverse_dict = {value: key for key, value in classDict.items()}

    imfs = DataFilter.read_file(str(testFilePath))

    # Only include IMFs that were included in the model
    filteredImfs = []
    for i, imf in enumerate(imfs):
        if (i in imfRange):
            filteredImfs.append(imf[:smallestIMF])

    arr = model.predict(filteredImfs)

    finalGuesses = []

    for elem in arr:
        finalGuesses.append(reverse_dict[elem])

    print(finalGuesses)


if __name__ == "__main__":
    main()