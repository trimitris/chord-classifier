#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>

std::vector<std::vector<double>> receiveFrame();
std::vector<std::vector<std::vector<double>>> listener();
void postStdout(std::vector<std::string> data ,std::string tag);
