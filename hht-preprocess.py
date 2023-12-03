# Usage:
# python hht-preprocess file1.txt [--num-splits NUM_SPLITS]

# https://brainflow.readthedocs.io/en/stable/DataFormatDesc.html
# https://docs.openbci.com/Ganglion/GanglionDataFormat/


import os
import pyhht
import argparse
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scipy.signal import hilbert

from brainflow.data_filter import DataFilter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='The path to the directory containing EEG data to be pre-processed')
    parser.add_argument('--num-splits', '-n', type=int, help='The number of segments to split the EEG data into before performing EMD', required=False, default=0)
    parser.add_argument('--no-photos', '-p', type=bool, help='Add this argument if you don\'t want to save photos of EMD graphs', required=False, default=False)
    args = parser.parse_args()

    filePath = Path(args.path)
    numSplits = args.num_splits
    noPhotos = args.no_photos

    for file in filePath.iterdir():
        filename, file_extension = os.path.splitext(file)
        outputPath = filename + '_Pre-Processed'
        eeg_data = DataFilter.read_file(str(file)) # Returns 2D numpy array
        
        # print(BoardShim.get_board_descr(BoardIds.GANGLION_BOARD))
        # Output: {'accel_channels': [5, 6, 7], 'ecg_channels': [1, 2, 3, 4], 'eeg_channels': [1, 2, 3, 4], 'emg_channels': [1, 2, 3, 4], 'eog_channels': [1, 2, 3, 4], 'marker_channel': 14, 'name': 'Ganglion', 'num_rows': 15, 'package_num_channel': 0, 'resistance_channels': [8, 9, 10, 11, 12], 'sampling_rate': 200, 'timestamp_channel': 13}
        eeg_data = [eeg_data[1], eeg_data[13]]

        # Fix duplicate timestamps
        prevTimestamp = 0
        for i, timestamp in enumerate(eeg_data[1]):
            if (prevTimestamp == timestamp and i < len(eeg_data[1]) - 1):
                eeg_data[1][i] = (eeg_data[1][i] + eeg_data[1][i+1])/2
            elif (i == len(eeg_data[1]) - 1):
                eeg_data[1][i] = eeg_data[1][i] + (eeg_data[1][i-1] - eeg_data[1][i-2]) # This assumes we have more than 2 elements in the list
            prevTimestamp = timestamp

        # Split file
        splitArray = []
        if (numSplits > 0):
            splitArray = splitData(numSplits, eeg_data)
        else:
            splitArray.append(eeg_data)

        # Useful for Debugging
        # printData(splitArray)

        # https://pyhht.readthedocs.io/en/latest/apiref/pyhht.html#pyhht.emd.EmpiricalModeDecomposition.__init__
        for i, array in enumerate(splitArray):
            # Weird numpy hack
            array0_np = np.array(array[0])
            array1_np = np.array(array[1])

            decomposer = pyhht.EMD(array0_np, array1_np) # Perform Empirical Mode Decomposition
            imfList = decomposer.decompose() # Generate IMFs
            if (not noPhotos):
                savePlot(imfList, outputPath, i)

            spectralEntropies = []
            hilbertTransforms = []
            for imf in imfList: # Apply Hilbert Transform
                hilbertTransform = hilbert(imf)
                hilbertTransforms.append(hilbertTransform)
                hhtIntegral = np.cumsum(hilbertTransform) # Integrate the HHT result
                hHatF = hhtIntegral / np.sum(hhtIntegral)
                spectralEntropy = computeSpectralEntropy(hHatF)
                spectralEntropies.append(spectralEntropy)

            saveDataToFile(spectralEntropies, outputPath, i)
            # if (i == 1):
            #     saveHilbertPlot(hilbertTransforms, outputPath)

def splitData(numSplits, array):
    dataLength = array[1][len(array[1]) - 1] - array[1][0]
    # print("Data Length: " + str(dataLength))
    splitInterval = dataLength / numSplits
    # print("Split Interval: " + str(splitInterval))

    splitArray = []
    currentIndex = 0
    for i in range(numSplits):
        newArr = [[], []]
        currentSplitEnd = array[1][0] + ((i + 1) * splitInterval)
        # print("Split End for split " + str(i) + ": " + str(currentSplitEnd))

        while (array[1][currentIndex] < currentSplitEnd):
            newArr[0].append(array[0][currentIndex])
            newArr[1].append(array[1][currentIndex])
            currentIndex += 1

        splitArray.append(newArr)
    
    return splitArray


def savePlot(imfs, outputPath, splitNum):
    fig, axes = plt.subplots(len(imfs), 1, figsize=(8, 4 * len(imfs)))
    
    for i, (imf, ax) in enumerate(zip(imfs, axes)):
        ax.plot(imf)
        ax.set_title(f'IMF {i + 1}')
        ax.set_xlabel('Time')

    plt.tight_layout()
    
    imf_output_path = f'{outputPath}_Split-{splitNum}.png'
    plt.savefig(imf_output_path, dpi=300, bbox_inches='tight')
    plt.close()


def saveHilbertPlot(hilbert_data, outputPath):
    fig, axes = plt.subplots(len(hilbert_data), 1, figsize=(8, 4 * len(hilbert_data)))

    for i, hilbert_result in enumerate(hilbert_data):
        axes[i].plot(hilbert_result.imag, label='Imaginary', color='orange')
        axes[i].set_title(f'Hilbert Transformed Data {i + 1} - Imaginary')
        axes[i].set_xlabel('Time')
        axes[i].legend()

    plt.tight_layout()

    plt.savefig(outputPath, dpi=300, bbox_inches='tight')
    plt.close()

def saveDataToFile(data, outputPath, splitNum):
    np.save(f'{outputPath}_Split-{splitNum}.npy', data)

def computeSpectralEntropy(hhtResults):
    m = len(hhtResults)
    spectral_entropy = -np.sum(hhtResults * np.log2(hhtResults + 1e-10)) / np.log2(m)
    
    return spectral_entropy

if __name__ == "__main__":
    main()