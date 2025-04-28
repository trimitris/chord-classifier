#include <iostream>
#include <math.h>
#include <vector>
#include "musicData.h"

double calcEnergy(std::vector<double> signal);
std::vector<std::vector<double>> getFrameEnergies(std::vector<std::vector<std::vector<double>>> frames);

double gaussianFn(double value, double sigma);
std::vector<double> gaussKernel1d(double sigma);
std::vector<double> convolution(std::vector<double> signal, std::vector<double> kernel);
std::vector<double> gaussianSmoothing(std::vector<double> signal, double sigma);
std::vector<double> FODKernel();
std::vector<double> calcFOD(std::vector<double> signal);
std::vector<int> getZeroCrossings(std::vector<double> yvals);
std::vector<int> getMaxPoints(std::vector<double> yvals);
std::vector<int> detectSteps(std::vector<double> yvals);

std::vector<std::vector<int>> extractChordGroups(std::vector<std::vector<std::vector<double>>> frames, double sigma);
