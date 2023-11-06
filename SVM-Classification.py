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
    model = funData[0]
    classDict = funData[1]
    reverse_dict = {value: key for key, value in classDict.items()}

    imfs = DataFilter.read_file(str(testFilePath))

    arr = model.predict(imfs)

    finalGuesses = []

    for i, elem in enumerate(arr):
        finalGuesses.append(reverse_dict[elem])

    print(finalGuesses)


if __name__ == "__main__":
    main()