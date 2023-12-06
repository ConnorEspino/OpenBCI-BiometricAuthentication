import joblib
import argparse
import numpy as np
from pathlib import Path
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trainingDataPath', type=str, help='A directory containing one or more labeled directories of one or more pre-processed EEG readings which the SVM model will be trained on')
    parser.add_argument('--outputName', type=str, help='The name of the file to which the SVM model will be saved', required=False, default='SVM-Model')
    parser.add_argument('--imfRange', type=str, help='The range of Intrinsic Mode Functions (IMFs) to use for creating the model. For example, use \'2-5\' for an inclusive range, \'2\' for a single IMF, or don\'t include the argument for all IMFs.', required=False, default='-1')
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
                data = np.load(str(file))
                for i, entry in enumerate(data):
                    if (-1 in imfRange or i in imfRange):

                        SpecEntrReal = [np.real(entry), np.imag(entry)]

                        trainingData.append(SpecEntrReal)
                        classificationArray.append(classDict[dir.name])

    # Get data in proper format for SVC
    classificationArray = np.array(classificationArray)

    scaler = StandardScaler()
    trainingDataScaled = scaler.fit_transform(trainingData)

    # Perform hyperparameter tuning
    # param_grid = {'C': [0.1, 1, 10, 100]}
    # gridSearch = GridSearchCV(SVC(kernel='linear'), param_grid, cv=5)
    # gridSearch.fit(trainingDataScaled, classificationArray)
    # bestParams = gridSearch.best_params_
    # bestModel = gridSearch.best_estimator_

    # print(f'Best Model: {str(bestModel)}')
    # print(f'Best Params: {str(bestParams)}')

    model = SVC(C=cValue, kernel=mKernel, verbose=0, decision_function_shape='ovr')
    print('Building Model with C Value: ' + str(cValue) + ', Kernel: ' + str(mKernel))
    try:
        # print(f'Training Data: {str(trainingDataScaled)}')
        # print(f'\n\nClassification Array: {str(classificationArray)}')
        model.fit(trainingDataScaled, classificationArray)
    except Exception as e:
        print("\n\nError:\n" + str(e))
        return

    funData = [scaler, imfRange, model, classDict]

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