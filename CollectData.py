import argparse
import time
import os
from pathlib import Path
from brainflow.data_filter import DataFilter
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


def main():
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, help='Timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--serialPort', type=str, help='The serial port that the Ganglion dongle is plugged into (Default: COM3)', required=False, default="COM3")
    parser.add_argument('--sessionName', type=str, help='The name of the directory to output the file to', required=False, default='')
    parser.add_argument('--outputFile', type=str, help='The file to output the data to (Will create if it doesn\'t exist)', required=False, default='')
    parser.add_argument('--runTime', type=int, help='The amount of time to run the brain scan for', required=False, default=15)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    # 30 Seconds until it stops looking for a board
    params.timeout = args.timeout
    params.serial_port = args.serialPort
    sessionName = args.sessionName
    outputFile = args.outputFile

    path = Path('./' + sessionName + '/' + outputFile)
    if (os.path.isfile(path)):
        print('File ' + path + ' already exists\n')
        answer = input('Would you like to override this file? (Y/N): ')
        if (answer.lower() == 'n'):
            outputFile = ''

    board = BoardShim(BoardIds.GANGLION_BOARD, params)
    board.prepare_session()
    
    # https://docs.openbci.com/Ganglion/GanglionSDK/#turn-channels-off
    # Remove these to turn on the corresponding channel
    board.config_board("2")
    board.config_board("3")
    board.config_board("4")

    board.start_stream()
    time.sleep(args.runTime)
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    
    board.release_session()

    if (sessionName == '') :
        print(os.listdir())
        sessionName = sessionName + str(len(os.listdir()))

    if (os.path.exists(Path('./' + sessionName))) :
        writeFile(sessionName, outputFile, data)
    else:
        os.makedirs(Path('./' + sessionName))
        writeFile(sessionName, outputFile, data)
    
    print('Exported Data to ./' + sessionName + '/' + outputFile)

def writeFile(sessionName, outputFile, data):
    if (outputFile == '') :
        outputFile = outputFile + str(len(os.listdir(Path('./' + sessionName))))
    DataFilter.write_file(data, './' + sessionName + '/' + outputFile, 'w')

if __name__ == "__main__":
    main()