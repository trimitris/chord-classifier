import tests
from notepro import get_frames
from plotting import plotCustom
from detectOnset import onsets
import numpy as np
import os
import interface

if __name__ == "__main__":
    # tests.test_chord_samples()

    path = "custom_recs/textfiles/"
    # file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_t"
    file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_intenseStrummingt"
    # file = "guitar_Am_Dm_Am_Gmaj_Amt"
    # file = "guitar_Dmaj_Gsus_Amaj_Gmaj_Amajt"
    # file = "guitar_G7_G#dim7_Adim7_G7_G#dim7_Adim7_Gmajt"
    fs = 44100

    myrecording = np.loadtxt(str("../" + path+file))
    numSamples, numChannels = myrecording.shape
    frames = get_frames(myrecording, 512)
    chordGroups = onsets(frames,6)
    print(chordGroups)

    firstTime = True
    for chordGroup in chordGroups:
        cmd = str('python3 dataTransfer2.py ' + file + " "+ str(chordGroup[0]) + " "+ str(chordGroup[1]) + ' | ../src/inter')
        # open a pipline with linux
        with os.popen(cmd) as pipe:
            chords = interface.listener("chord", pipe)
        if firstTime:
            print(chords[-1], "starting sec: ", chordGroup[0]/fs*512)
            firstTime = False
        else:
            if (lastChord != chords[-1]):
                print(chords[-1], "starting sec: ", chordGroup[0]/fs*512)

        lastChord = chords[-1]
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
