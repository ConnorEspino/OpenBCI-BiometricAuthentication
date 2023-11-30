import joblib
import argparse
import numpy as np
from pathlib import Path
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from brainflow.data_filter import DataFilter
from sklearn.inspection import DecisionBoundaryDisplay

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trainingDataPath', type=str, help='The path to the directory containing the data which the SVM model will be trained on')
    parser.add_argument('--outputName', type=str, help='The name of the file to which the SVM model will be saved', required=False, default='SVM-Model')
    parser.add_argument('--imfRange', type=str, help='The range of IMFs to use for creating the model, Ex: \'2-5\' for inclusive range or \'2\' for a single IMF or don\'t include argument for all IMFs', required=False, default='-1')
    parser.add_argument('--cValue', type=float, help='SVM regularization parameter', required=False, default=1.0)
    args = parser.parse_args()

    cValue = args.cValue
    mKernel = 'linear'
    trainingDataPath = Path(args.trainingDataPath)
    outputPath = Path(args.trainingDataPath + '/' + args.outputName + '-C' + str(cValue) + '.pkl')
    imfRange = validateRange(args.imfRange)

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

    for dir in trainingDataPath.iterdir():
        if (dir.is_dir()):
            classDict[dir.name] = len(classDict)
            for file in dir.iterdir():
                instantFreqs = np.load(str(file))
                freqsToInclude = []
                for i, freq in enumerate(instantFreqs):
                    if (-1 in imfRange or i in imfRange):
                        freqsToInclude.append(freq)
                trainingData.append(freqsToInclude)
                classificationArray.append(classDict[dir.name])

    # Get data in proper format for SVC
    classificationArray = np.array(classificationArray)
    # for i, el in enumerate(trainingData):
    #     trainingData[i] = el[:smallestIMF]

    # print(str(classificationArray))

    model = SVC(C=cValue, kernel=mKernel, verbose=0)
    print('Building Model with C Value: ' + str(cValue) + ', Kernel: ' + str(mKernel))
    try:
        model.fit(trainingData, classificationArray)
    except Exception as e:
        print("\n\nError:\n" + str(e))
        return


    funData = [imfRange, model, classDict]

    joblib.dump(funData, outputPath)

def validateRange(rangeArg):
    if rangeArg == '-1':
        return [-1]

    if '-' in rangeArg:
        start, end = map(int, rangeArg.split('-'))
        return list(range(start, end + 1))  # Adding 1 to include the end value
    else:
        return [int(rangeArg)]

if __name__ == "__main__":
    main()