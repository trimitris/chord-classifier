import numpy as np
import math
import matplotlib.pyplot as plt
from notepro import get_fft_freq

def plotAmpl(path,file,fs):
    """
    plots the amplitude of a sound file against time
    """
    myrecording = np.loadtxt(str('../' + path+file))
    numSamples = len(myrecording)
    duration = numSamples/fs

    time = np.linspace(0,duration,numSamples)

    plt.plot(time,myrecording[:,0])
    plt.title(file)
    plt.show()

def plotFreq(path,file, fs, maxFreq=3000):
    """
    plots the frequency domain against time
    """
    myrecording = np.loadtxt(str('../' + path + file))

    #Fourier transform
    signal = myrecording[:,0]
    magn_fourier, freq = get_fft_freq(signal,fs)

    #plot
    plt.plot(freq,magn_fourier)
    plt.title(file)
    plt.xlim(0,maxFreq)
    plt.show()

def plotCustom(xvals,yvals):
    plt.plot(xvals,yvals)
    plt.show()

# if __name__== "__main__":
    # plotAmpl("custom_recs/textfiles/", "guitar_Dsus2_s1t", 44100)
    # plotFreq("custom_recs/textfiles/", "guitar_Dsus2_s1t", 44100)
    # plotAmpl("custom_recs/textfiles/","guitar_manha_rifft",44100)
