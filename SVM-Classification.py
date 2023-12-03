import joblib
import argparse
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('modelPath', type=str, help='The path to the .pkl file containing the model created from SVM-CreateModel.py')
    parser.add_argument('testData', type=str, help='The path to the directory containing labeled directories of preprocessed EEG data to test for classification')
    args = parser.parse_args()

    modelPath = Path(args.modelPath)
    testPath = Path(args.testData)

    funData = joblib.load(modelPath)
    scaler = funData[0]
    imfRange = funData[1]
    model = funData[2]
    classDict = funData[3]
    reverse_dict = {value: key for key, value in classDict.items()}

    testData = []
    classificationArray = []

    for dir in testPath.iterdir():
        if (dir.is_dir()):
            for file in dir.iterdir():
                data = np.load(str(file))
                for i, entry in enumerate(data):
                    if (-1 in imfRange or i in imfRange):
                        SpecEntrReal = [np.real(entry), np.imag(entry)]

                        testData.append(SpecEntrReal)
                        classificationArray.append(classDict[dir.name])

    testDataScaled = scaler.transform(testData)
    try:
        testPredictions = model.predict(testDataScaled)
        # print(f'Test Data: {str(testDataScaled)}')
        # print(f'Test Prediction: {str(testPredictions)}')
        accuracy = accuracy_score(classificationArray, testPredictions)
        print(f'Model Accuracy: {accuracy}')
    except Exception as e:
        print("\n\nError:\n" + str(e))
        return

    # finalGuesses = []

    # for elem in arr:
    #     finalGuesses.append(reverse_dict[elem])

    # print(finalGuesses)


if __name__ == "__main__":
    main()