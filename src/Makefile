# all:
# 	g++ Chromagram.cpp run.cpp ChordDetector.cpp -DUSE_FFTW -lfftw3 -lm -o go

# Variables to control Makefile operation
CXX = g++
CXXFLAGS = -DUSE_FFTW -lfftw3 -lm -Wall -g -O3

# ****************************************************
# Targets needed to bring the executable up to date
# libfoo.so: Chromagram.o ChordDetector.o run.o musicData.o
# 	$(CXX) -shared -o libfoo.so Chromagram.o ChordDetector.o run.o musicData.o
all: go inter

go: Chromagram.o ChordDetector.o run.o musicData.o onsetDetector.o
	$(CXX) ChordDetector.o Chromagram.o run.o musicData.o onsetDetector.o $(CXXFLAGS) -o go
inter: runInter.o interface.o musicData.o Chromagram.o ChordDetector.o
	$(CXX) runInter.o interface.o musicData.o Chromagram.o ChordDetector.o $(CXXFLAGS) -o inter

runInter.o: runInter.cpp interface.h musicData.h
	$(CXX) $(CXXFLAGS) -c runInter.cpp
run.o: run.cpp musicData.h
	$(CXX) $(CXXFLAGS) -c run.cpp
onsetDetector.o: onsetDetector.cpp onsetDetector.h musicData.h
	$(CXX) $(CXXFLAGS) -c onsetDetector.cpp
musicData.o: musicData.cpp musicData.h ChordDetector.h Chromagram.h interface.h
	$(CXX) $(CXXFLAGS) -c musicData.cpp
interface.o: interface.cpp interface.h
	$(CXX) $(CXXFLAGS) -c interface.cpp
Chromagram.o: Chromagram.cpp Chromagram.h
	$(CXX) $(CXXFLAGS) -c Chromagram.cpp
ChordDetector.o: ChordDetector.cpp ChordDetector.h
	$(CXX) $(CXXFLAGS) -c ChordDetector.cpp

clean:
	rm run.o Chromagram.o ChordDetector.o musicData.o interface.o runInter.o onsetDetector.o
