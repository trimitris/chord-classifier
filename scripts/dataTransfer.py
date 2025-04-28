'''
This script processes the file passed as an argument from the terminal.
Used with test_chord_samples()
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
    except:
        raise ValueError("Provide a file name as an argument")

    myrecording = np.loadtxt(str("../" + path+file))
    frames = get_frames(myrecording, 512)
    onset = onsets(frames, 10)[0][0]
    interface.sendFrames(frames[onset:])
