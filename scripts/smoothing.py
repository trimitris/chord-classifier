import numpy as np
from notepro import get_frames
from plotting import plotCustom
from scipy.ndimage import gaussian_filter

if __name__ == "__main__":
    path = "custom_recs/textfiles/"
    # file = "guitar_C#m_s1t"
    # file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_t"
    file = "guitar_Cmaj_Fmaj_Gmaj_Cmaj_intenseStrummingt"
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

    # filter the energies function
    sigmas = [2,3,4,5,6,7,8,9,10]
    smoothEner = []
    for sigma in sigmas:
        smoothEner.append(gaussian_filter(energies, sigma)) #sigma = 2.5
        print(sigma)
        plotCustom(frameNums,smoothEner[-1])
