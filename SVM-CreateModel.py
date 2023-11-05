import joblib
import argparse
import numpy as np
from pathlib import Path
from sklearn.svm import SVC
from brainflow.data_filter import DataFilter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trainingDataPath', type=str, help='The path to the directory containing the data which the SVM model will be trained on')
    parser.add_argument('--outputName', type=str, help='The name of the file to which the SVM model will be saved', required=False, default='SVM-Model')
    args = parser.parse_args()

    trainingDataPath = Path(args.trainingDataPath)
    outputPath = Path(args.trainingDataPath + '/' + args.outputName + '.pkl')

    if (not trainingDataPath.is_dir()):
        print("Path does not exist: " + str(trainingDataPath))
        return
    
    # https://scikit-learn.org/stable/modules/svm.html#multi-class-classification
    # trainingData is X array
    # classificationArray is Y
    # classDict is used for converting numerical classification to participant's names.
    trainingData = []
    classificationArray = []
    classDict = dict()
    smallestIMF = 9999999999

    for dir in trainingDataPath.iterdir():
        if (dir.is_dir()):
            classDict[dir.name] = len(classDict)
            for file in dir.iterdir():
                imfs = DataFilter.read_file(str(file))
                for imf in imfs:
                    if (len(imf) < smallestIMF):
                        smallestIMF = len(imf)
                    trainingData.append(np.array(imf))
                    classificationArray.append(classDict[dir.name])

    # Get data in proper format for SVC
    classificationArray = np.array(classificationArray)
    for i, el in enumerate(trainingData):
        trainingData[i] = el[:smallestIMF]

    # print(str(classificationArray))

    model = SVC(kernel='linear')
    model.fit(trainingData, classificationArray)

    joblib.dump(model, outputPath)

if __name__ == "__main__":
    main()