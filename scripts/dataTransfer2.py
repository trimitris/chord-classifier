'''
This script processes the file passed as an argument from the terminal.
It should be called this way:
$ python3 dataTransfer.py [fileName] | ../src/inter
So, this script works by piping data to ../src/inter
'''

import numpy as np
from notepro import get_frames
from detectOnset import onsets
import interface
import sys

if __name__ == "__main__":
    path = "custom_recs/textfiles/"
    fs = 44100

    # gets the file name passed as an argument from the terminal
    try:
        file = sys.argv[1]
        noteOnset = int(sys.argv[2])
        noteEnd = int(sys.argv[3])
    except:
        raise ValueError("Provide a file name and starting and ending frame as an argument")

    myrecording = np.loadtxt(str("../" + path+file))
    frames = get_frames(myrecording, 512)
    interface.sendFrames(frames[noteOnset:noteEnd])
