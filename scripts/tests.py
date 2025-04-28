import interface
import os
from utilities import extractChordLabels

def test_chord_samples():
    # retrieve file names from directory
    path = "../custom_recs/textfiles/"
    files = os.listdir(path)
    print(files)
    # get chord labels
    labels = extractChordLabels(files)
    print(labels)

    numFiles = len(files)
    correctExamples = 0

    for i,file in enumerate(files):
        # pass the file name to be processed to the dataTransfer.py script as an argument
        cmd = str('python3 dataTransfer.py ' + file + ' | ../src/inter')
        # open a pipline with linux
        with os.popen(cmd) as pipe:
            chords = interface.listener("chord", pipe)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(file)
        print(labels[i])
        # print(chords)

        # assess result for each frame
        correctRoot = 0 # correct root note detected (regardless of quality)
        falseRoot=0
        correctQual = 0 # correct chord quality detected (regardless of root)
        falseQual=0
        correctRQ=0 # correct root AND quality detected
        falseRQ = 0 # false root OR quality detected
        for chord in chords[:-1]: # must not check the last entry in chords, because that is the final classification of the chord by majority vote
            if (chord[0] == labels[i][0]):
                correctRoot +=1
            else:
                falseRoot +=1
            if (chord[1] == labels[i][1]):
                correctQual+=1
            else:
                falseQual +=1
            if ((chord[0] == labels[i][0]) and (chord[1] == labels[i][1])):
                correctRQ += 1
            else:
                falseRQ +=1

        # Calculate accuracies for whole file
        accRoot = (correctRoot/(correctRoot + falseRoot))*100
        accQual = (correctQual/(correctQual+falseQual))*100
        accTot = (correctRQ/(correctRQ+falseRQ))*100
        print("Correct root %", accRoot)
        print("Correct quality %", accQual)
        print("Correct overall %", accTot)

        # The last entry in the chords data structure contains the final classification
        finalClassification = False
        if ((chords[-1][0] == labels[i][0]) and (chords[-1][1] == labels[i][1])):
            finalClassification = True
            correctExamples +=1
        if (finalClassification == True):
            print("Final Classification: CORRECT")
        else:
            print("Final Classification: FALSE")

    print("-----------------------------------------------")
    accOverall = correctExamples/numFiles*100
    print("Total number of files: ", numFiles)
    print("Correct classifications count: ", correctExamples)
    print("Incorrect classifciations count: ", (numFiles - correctExamples))
    print("Overall accuracy over dataset: ", accOverall, "%")
