#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <stdexcept>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>

#include "Chromagram.h"
#include "ChordDetector.h"
#include "interface.h"

// function declarations

std::vector< std::vector <double>> importMusicFile(std::string fileName);
std::vector < std::vector <double>> splitChannels(std::vector <std::vector<double>> input);
std::vector<std::string> getDir (std::string dir);
std::vector<std::vector<std::vector<double>>> splitFrames(std::vector<std::vector<double>> data, int frameSize);
std::vector<std::vector<std::vector<double>>> preprocessFile(std::string path, std::string fileName, int frameSize);
std::vector< std::vector<std::string>> analyse(std::vector<std::vector<std::vector<double>>> frames, int frameSize);
void analyseDirectory(std::string directory, int frameSize);

// templates (have to be placed in .h file)
template <class type>
void print_1dvector(std::vector<type> vec) {
	//prints a 1d vector
	for (typename std::vector<type>::const_iterator i = vec.begin(); i != vec.end(); ++i)
		std::cout << *i << ' ';
	std::cout << std::endl;
}

template <class type>
void print_2dvector(std::vector< std::vector<type> > large_vec) {
	//prints a 2d vector
	for (typename std::vector< std::vector<type> >::const_iterator i = large_vec.begin();
		i != large_vec.end(); ++i) {
		print_1dvector<type>(*i);
	}
	std::cout << std::endl;
}
