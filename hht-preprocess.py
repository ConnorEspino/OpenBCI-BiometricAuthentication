# Usage:
# python hht-preprocess file1.txt

# https://brainflow.readthedocs.io/en/stable/DataFormatDesc.html


import os
import pyhht
import argparse
from brainflow.data_filter import DataFilter

# import pyqtgraph as pg
# from pyqtgraph.Qt import QtGui, QtCore
# from PyQt6.QtWidgets import QApplication


# class Graph:
#     def __init__(self, data_file):
#         self.data_file = data_file
#         self.app = QApplication([])
#         self.win = pg.GraphicsLayoutWidget(title='EEG Data Plot', size=(800, 600))
#         self.eeg_data = DataFilter.read_file(self.data_file)
#         #self.eeg_channel = BrainFlow.get_eeg_channels(BrainFlow.GANGLION_BOARD)

#         self._init_timeseries()

#         timer = pg.QtCore.QTimer()
#         timer.timeout.connect(self.update)
#         timer.start(50)

#         self.app.exec()

#     def _init_timeseries(self):
#         self.plots = list()
#         self.curves = list()

#         p = self.win.addPlot(row=0, col=0)  # Use row=0 for the first channel
#         p.showAxis('left', False)
#         p.setMenuEnabled('left', False)
#         p.showAxis('bottom', False)
#         p.setMenuEnabled('bottom', False)
#         p.setTitle('TimeSeries Plot')
#         self.plots.append(p)
#         curve = p.plot()
#         self.curves.append(curve)

#     def update(self):
#         self.curves[0].setData(self.eeg_data[:, self.eeg_channel])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='The path to the Brainflow file of EEG data to be pre-processed')
    filePath = parser.parse_args().path
    filename, file_extension = os.path.splitext(filePath)
    outputPath = filename + '_Pre-Processed' + file_extension
    if (os.path.isfile(outputPath)):
        print('File ' + outputPath + ' already exists\n')
        answer = input('Would you like to override this file? (Y/N): ')
        if (lower(answer) == 'n'):
            return
        
    # print(BoardShim.get_board_descr(BoardIds.GANGLION_BOARD))
    #Output: {'accel_channels': [5, 6, 7], 'ecg_channels': [1, 2, 3, 4], 'eeg_channels': [1, 2, 3, 4], 'emg_channels': [1, 2, 3, 4], 'eog_channels': [1, 2, 3, 4], 'marker_channel': 14, 'name': 'Ganglion', 'num_rows': 15, 'package_num_channel': 0, 'resistance_channels': [8, 9, 10, 11, 12], 'sampling_rate': 200, 'timestamp_channel': 13}

    # graph = Graph(filePath)
    # timer = QtCore.QTimer()
    # timer.timeout.connect(graph.update)
    # timer.start(50)
    # QtGui.QApplication.instance().exec_()

    eeg_data = DataFilter.read_file(filePath) # Returns 2D numpy array
    newArr = [eeg_data[1], eeg_data[13]]

    prevNum = 0
    for i, num in enumerate(newArr[1]):
        if (prevNum == num and i < len(newArr[1]) - 1):
            newArr[1][i] = (newArr[1][i] + newArr[1][i+1])/2
        elif (i == len(newArr[1]) - 1):
            newArr[1][i] = newArr[1][i] + (newArr[1][i-1] - newArr[1][i-2]) # This assumes we have more than 2 elements in the list
        prevNum = num

    printData(newArr)
        

    # plt.plot(eeg_data)
    # imf_output_path = f'{outputPath}_IMF_{1}.png'
    # plt.savefig(imf_output_path, dpi=300, bbox_inches='tight')
    # plt.plot(eeg_data[:, 0])
    # imf_output_path = f'{outputPath}_IMF_{2}.png'
    # plt.savefig(imf_output_path, dpi=300, bbox_inches='tight')

    # eeg_data = eeg_data[:, 0]  # Extract the first channel's information (1D array)
    # decomposer = pyhht.EMD(eeg_data) # Perform Empirical Mode Decomposition
    # imfs = decomposer.decompose() # Generate IMFs
    # savePlot(imfs, outputPath)
def printData(array):
    for i, elem in enumerate(array[0]):
        print(str(elem) + ' ' + str(array[1][i]))
# def savePlot(imfs, outputPath):
#     for i, imf in enumerate(imfs):
#         plt.figure(figsize=(8, 4))
#         plt.plot(imf)
#         plt.title(f'IMF {i + 1}')
#         plt.xlabel('Time')
#         plt.tight_layout()

#         imf_output_path = f'{outputPath}.png'
#         plt.savefig(imf_output_path, dpi=300, bbox_inches='tight')
#         plt.close()

if __name__ == "__main__":
    main()