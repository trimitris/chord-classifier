# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 01:12:51 2018

@author: Demetris
"""

import numpy as np
from notepro import get_frames
from plotting import plotCustom

if __name__ == "__main__":
    path = "custom_recs/textfiles/"
    file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_t"
    # file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_intenseStrummingt"
    # file = "guitar_manha_rifft"
    fs = 44100

    myrecording = np.loadtxt(str("../" + path+file))
    frames = get_frames(myrecording, 512)

    numFrames = frames.shape[0]

    #calculate each frame's energy
    energies = []
    for frame in frames:
        energy = ((frame**2).sum(axis=0))**0.5
        energies.append(energy)

    energies = np.array(energies)
    frameNums = np.arange(0,numFrames,1)
    plotCustom(frameNums,energies)
