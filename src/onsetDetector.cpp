/*
* File containing functions related to onset detection
* Mainly functions performing basic signal processing tasks (energy calculation, filtering etc)
*/

#include "onsetDetector.h"

/*
* Calculates the energy of the input signal
*/
double calcEnergy(std::vector<double> signal){
  double energy = 0;
  for (unsigned int i=0; i<signal.size(); i++){
    energy += pow(signal[i],2);
  }
  energy = pow(energy,0.5);
  return energy;
}

/*
* Calculates the energy contained in each channel for each frame.
* Input: frames[frame][samples][channel]
* Output: energies[frame][channel]
*/
std::vector<std::vector<double>> getFrameEnergies(std::vector<std::vector<std::vector<double>>> frames){

  // energies is of the form: energies[frame][channel]
  std::vector<std::vector<double>> energies;

  for (unsigned int i = 0; i<frames.size(); i++){
    //Access each individual frame

    std::vector<double> frameEnergies;
    std::vector<std::vector<double>> channels = splitChannels(frames[i]);
    for (unsigned int j= 0; j<channels.size(); j++){
      // Perform energy calculation on each individual channel
      frameEnergies.push_back(calcEnergy(channels[j]));
    }
    energies.push_back(frameEnergies);
    frameEnergies.clear();

  }
  return energies;
}

/*
* Evaluates the gaussian function at the specified value with the specified sigma and mu = 0
*/
double gaussianFn(double value, double sigma){
  return (1/(sigma*pow((2*M_PI),0.5))) * exp(-0.5*pow((value/sigma),2));
}

/*
* Generates a 1D gaussian kernel with the specified sigma and mu=0
* Accuracy: the kernel is truncated when its value is 1/1000 of its peak value
*/
std::vector<double> gaussKernel1d(double sigma){
  int n = std::floor(sigma* pow((2*log1p(1000)),0.5));
  int kernelLength = 2*n + 1;
  std::vector<double> kernel(kernelLength);

  // fill the kernel with the gaussain function values:

  // middle value
  kernel[n] = gaussianFn(0,sigma);
  // rest of the kernel
  for (int i=0; i<n; i++){
    double val = gaussianFn(i -n, sigma);
    kernel[i] = val;
    kernel[kernelLength -1 -i] = val;
  }

  return kernel;
}

/*
* Performs 1D convolution of the signal and the kernel. The algorithm deals with
* end effects by mirroring the signal.
*/
std::vector<double> convolution(std::vector<double> signal, std::vector<double> kernel){
  // Check if kernel has odd number of elements
  if ((kernel.size()%2)!=1){
    throw std::runtime_error("Kernel should have odd number of elements");
  }

  int n = (kernel.size()-1)/2;
  int sizeSignal = signal.size();

  // Deal with case of kernel size being too big compared to the signal size
  if (n >= sizeSignal){
    int excessKernel = n - sizeSignal + 1;

    // Remove excess kernel elements
    kernel.erase((kernel.end()-excessKernel) ,kernel.end());
    kernel.erase(kernel.begin(), (kernel.begin() + excessKernel));

    n = sizeSignal -1;
  }

  // Mirror the input signal to deal with end effects
  std::vector<double> mirroredSignal((sizeSignal + (2*n)));
  for (int i = 0; i<n; i++){
    mirroredSignal[i] = signal[n - i];
  }
  for (int i = (n + sizeSignal); i<(2*n + sizeSignal); i++){
    mirroredSignal[i] = signal[ 2*sizeSignal - 2 + n - i];
  }
  for (int i = n; i<(sizeSignal + n); i++){
    mirroredSignal[i] = signal[i - n];
  }

  // Perform the actual convolution
  std::vector<double> output(sizeSignal);
  for (int i = 0; i< sizeSignal; i++){
    double sum = 0;
    for (int j = -n ; j< (n+1); j++){
      sum += mirroredSignal[i + n + j]*kernel[n-j];
    }
    output[i] = sum;
  }

  return output;
}

/*
* Smooths the given signal with a gaussian kernel of the given sigma
*/
std::vector<double> gaussianSmoothing(std::vector<double> signal, double sigma){
  std::vector<double> kernel = gaussKernel1d(sigma);
  return convolution(signal, kernel);
}

/*
* First order derivative (FOD) kernel
*/
std::vector<double> FODKernel(){
  std::vector<double> kernel = {0.5, 0, -0.5};
  return kernel;
}

/*
* calculate first order derivative of signal
*/
std::vector<double> calcFOD(std::vector<double> signal){
  std::vector <double> fodKernel = FODKernel();
  std::vector<double> output = convolution(signal, fodKernel);

  // deal with edge effects:
  int sizeSignal = signal.size();
  output[0] = (signal[1]-signal[0]);
  output[sizeSignal-1] = (signal[sizeSignal - 1] - signal[sizeSignal - 2]);

  return output;
}

/*
* returns the indices of the yvals where there is a change of sign (i.e. zero crossing occurs)
*/
std::vector<int> getZeroCrossings(std::vector<double> yvals){
  if (yvals.size() < 3){
    throw std::runtime_error("yvals vector should have a size of at least 3");
  }

  std::vector<int> crossings;
  double lastVal = yvals[0];
  for (unsigned int i = 1; i<yvals.size(); i++){

    double val = yvals[i];

    if ((lastVal*val)<= 0){
      crossings.push_back(i);
    }
    lastVal = val;
  }

  return crossings;
}

/*
* returns the indices of the max points of the curve given by yvals
*/
std::vector<int> getMaxPoints(std::vector<double> yvals){
  // calculate first and second derivative
  std::vector<double> dy = calcFOD(yvals);
  std::vector<double> d2y = calcFOD(dy);

  // get xvals for which dy/dx = 0  a.k.a stationaryPoints
  std::vector<int> stationaryPoints = getZeroCrossings(dy);

  // find maxPoints from stationaryPoints. A point is max if its second derivative is negative
  std::vector<int> idxMaxPoints;
  for (unsigned int i=0; i<stationaryPoints.size(); i++){
    int idx = stationaryPoints[i];
    if (d2y[idx] <=0){
      idxMaxPoints.push_back(idx);
    }
  }

  return idxMaxPoints;
}

/*
* returns the indices of the yvals at which there is a step detected
*/
std::vector<int> detectSteps(std::vector<double> yvals){
  // calculate first derivative
  std::vector<double> dy = calcFOD(yvals);

  // steps are found at locations where the first derivative has maxPoints and it is also positive
  std::vector<int> idxMaxPoints = getMaxPoints(dy);

  std::vector<int> idxSteps;
  for (unsigned int i = 0; i< idxMaxPoints.size(); i++){
    int idx = idxMaxPoints[i];
    if (dy[idx] > 0){
      idxSteps.push_back(idx);
    }
  }

  return idxSteps;
}

/*
* Returns the frame ranges of the signal, in which events happened (e.g. notes or chords where played).
* The value of sigma affects the detail with which the algorithm looks for events in the signal.
*/
std::vector<std::vector<int>> extractChordGroups(std::vector<std::vector<std::vector<double>>> frames, double sigma){
  int numFrames = frames.size();

  // extract energy of the signal
  std::vector<std::vector<double>> energies = getFrameEnergies(frames);
  std::vector<std::vector<double>> energiesByChannel = splitChannels(energies);

  // by default only look at channel 0
  int channel = 0;

  // Perform filtering and get max points and steps
  std::vector<int> maxPoints, steps;
  std::vector<double> smoothedEnergy;

  // we need to make sure that we get at least one step point after the filtering. If not, this might
  // be because we filtered very severely.
  double filteringFactor = 1/1.2;
  while (steps.size() < 1){
    smoothedEnergy = gaussianSmoothing(energiesByChannel[channel], sigma);
    maxPoints = getMaxPoints(smoothedEnergy);
    steps = detectSteps(smoothedEnergy);

    sigma = sigma * filteringFactor;
    // make sure that sigma doesn't fall too low, to avoid consideration of noise from the recording
    if (sigma < 0.5){
      break;
    }
  }

  // Divide the filtered energy signal into chord groups
  std::vector<std::vector<int>> chordGroups;
  std::vector<int> chordGroup;

  /*
  Think about many cases:
  - No steps, no max points: no note played --> don't analyze
  - 1 step, no max: note climax not reached --> ChordGroup: from step to end of file
  - many steps, no max: note climax not reached, possible different notes played -->
  ChordGroup: from first step to end of file (might have to tweak this later).
  - Multiple max points and steps (normal situation): Mark chordGroups with range equal or smaller
  to the distance between each max point
  */

  // No max points:
  if (maxPoints.size() == 0){

    // 1 or more steps detected:
    if (steps.size() != 0){
      chordGroup.push_back(steps[0]);
      chordGroup.push_back(numFrames-1);
      chordGroups.push_back(chordGroup);
      chordGroup.clear();
    }

  }
  // One or more max points:
  else {

    double decayFactor = 0.2;

    int noteOnset, noteEnd;
    int numMaxPoints = maxPoints.size();

    // from first to second to last entry in maxPoints
    for (int i = 0; i<numMaxPoints; i++){
      noteOnset = maxPoints[i];

      // Make sure that we are not on the last max point
      if (i == (numMaxPoints -1)){
        noteEnd = numFrames - 1;
      }
      else {
        noteEnd = maxPoints[i+1] - 1;
      }

      // update noteEnd to be equal to the frame number of the next step (which signifies the beginning of another event)
      for (unsigned int j = 0; j<steps.size(); j++){
        int val = steps[j];
        if ((noteOnset<val) && (noteEnd > val)){
          noteEnd = val;
          break;
        }
      }

      // When the energy of the signal falls below the threshold, then terminate the chordGroup range
      // to prevent the chordDetector from detecting noise
      double threshold = decayFactor * smoothedEnergy[noteOnset];
      for (int j = noteOnset; j<(noteEnd + 1); j++){
        if (smoothedEnergy[j] < threshold){
          noteEnd = j;
          break;
        }
      }

      // We don't want any chord groups with the same onset and end
      if (noteOnset != noteEnd){
        chordGroup.push_back(noteOnset);
        chordGroup.push_back(noteEnd);
        chordGroups.push_back(chordGroup);
        chordGroup.clear();
      }
    }

  }

  return chordGroups;
}
