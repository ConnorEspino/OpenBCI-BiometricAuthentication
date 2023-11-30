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
    imfRange = funData[0]
    model = funData[1]
    classDict = funData[2]
    reverse_dict = {value: key for key, value in classDict.items()}

    imfs = np.load(str(testFilePath))

    # Only include IMFs that were included in the model
    filteredFreqs = []
    for i, imf in enumerate(imfs):
        if (-1 in imfRange or i in imfRange):
            filteredFreqs.append(imf)

    try:
        arr = model.predict(filteredFreqs)
    except Exception as e:
        print("\n\nError:\n" + str(e))
        return

    finalGuesses = []

    for elem in arr:
        finalGuesses.append(reverse_dict[elem])

    print(finalGuesses)


if __name__ == "__main__":
    main()