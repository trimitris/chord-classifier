import numpy as np
import math
from scipy.ndimage import gaussian_filter

import matplotlib.pyplot as plt
from notepro import get_frames
from plotting import plotCustom

def zero_crossings(xvals, yvals):
    """
    returns the xvals of the zero crossings in yvals
    """
    if (len(yvals) <= 2):
        raise ValueError("length of array should be larger than 2")

    crossings = []
    lastVal = yvals[0]
    for i in range(1,len(yvals)):
        val = yvals[i]
        if ((lastVal*val) <=0):
            crossings.append(xvals[i])
        lastVal = val
    return crossings

def max_points(xvals, yvals):
    """
    returns the maximum points of the yvals function
    """
    dy = np.gradient(yvals)
    d2y = np.gradient(dy)

    # get xvals for which dy/dx = 0
    crossings = zero_crossings(xvals, dy)

    # verify those xvals are max points
    xoutput = []
    for i in range(len(crossings)):
        val = crossings[i]
        if (d2y[val] <= 0):
            xoutput.append(val)

    youtput = [yvals[val] for val in xoutput]

    return xoutput, youtput

def detect_steps(xvals, yvals):
    """
    detects steps in the signal given by yvals
    """
    dy = np.gradient(yvals)
    d2y = np.gradient(dy)
    d3y = np.gradient(d2y)

    crossings = zero_crossings(xvals, d2y)

    xoutput = []
    for i in range(len(crossings)):
        val = crossings[i]
        if (dy[val] >=0):
            xoutput.append(val)

    youtput = [yvals[val] for val in xoutput]

    return xoutput, youtput

def onsets(frames, sigma = 4):
    """
    returns the frame number at which the note has started (i.e. where we have an increase in the energy of the signal)
    """
    numFrames = frames.shape[0]

    #calculate each frame's energy
    energies = []
    for frame in frames:
        energy = ((frame**2).sum(axis=0))**0.5
        energies.append(energy)

    energies = np.array(energies)
    frameNums = np.arange(0,numFrames,1)
    # plotCustom(frameNums,energies)

    # In case no max points where detected in the while loop, the process is repeated with a smaller sigma during smoothing
    maxPointsX = []
    while (len(maxPointsX) == 0):
        # filter the energies function
        smoothEner = gaussian_filter(energies, sigma)
        # plotCustom(frameNums,smoothEner)

        maxPointsX, maxPointsY = max_points(frameNums,smoothEner[:,0])
        xsteps, ysteps = detect_steps(frameNums, smoothEner[:,0])
        sigma = sigma/1.2


    # Note end detection
    # For each max point (which signifies a burst of energy in the signal, and so a new note being played),
    # identify its end point. This happens at the location of the signal where one of the following situations
    # happens first:
    #   i) the next note onset happens, or the end of the music file is reached
    #   ii) the energy of the frame decays to a number given by the decayFactor*maxPointsY

    chordGroups = []
    numMaxPoints = len(maxPointsX)
    decayFactor = 0.2
    for i in range(numMaxPoints):
        noteOnset = maxPointsX[i]
        # assume note end is the next onset happens, or at the end of file
        if (i == (numMaxPoints - 1)): # check if it is the last maxPoint, if it is, then noteEnd is the last frame of the music file
            noteEnd = (numFrames -1)
        else:
            noteEnd = maxPointsX[i+1]-1 # assume noteEnd is the next onset

        for x in xsteps:
            if (noteOnset < x < noteEnd):
                noteEnd = x
                break

        threshold = decayFactor*maxPointsY[i]
        for j,val in enumerate(smoothEner[noteOnset:noteEnd,0]):
            if (val < threshold):
                noteEnd = noteOnset + j
                break
        chordGroups.append((noteOnset,noteEnd))

    # # print("yvals of max/min points: ", maxPointsY)
    # # plot the smoothed energy against frame numbers
    # plt.plot(frameNums,smoothEner)
    # plt.scatter(maxPointsX,maxPointsY)
    # plt.scatter(xsteps,ysteps)
    # plt.show()

    # return pairs of frame numbers (for the start and end of each chord frame collection)
    return chordGroups

if __name__ == "__main__":
    path = "custom_recs/textfiles/"
    # file = "guitar_Emaj_s1t"
    # file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_t"
    file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_intenseStrummingt"
    fs = 44100

    myrecording = np.loadtxt(str("../" + path+file))
    numSamples, numChannels = myrecording.shape
    frames = get_frames(myrecording, 512)
    print(onsets(frames,6))
